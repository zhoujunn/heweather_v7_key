"""The HeWeather integration."""
import asyncio
import logging
import time
from datetime import datetime, timedelta

import aiohttp
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.event import async_track_time_interval

from .const import (
    DOMAIN, 
    CONF_API_HOST, 
    CONF_API_KEY, 
    CONF_LOCATION,
    CONF_UPDATE_INTERVAL,
    DEFAULT_API_HOST,
    DEFAULT_UPDATE_INTERVAL,
    API_ENDPOINTS  # 确保导入API_ENDPOINTS
)

_LOGGER = logging.getLogger(__name__)

class HeWeatherCoordinator(DataUpdateCoordinator):
    """Class to manage fetching HeWeather data."""
    
    def __init__(self, hass, api_host, api_key, location, update_interval):
        """Initialize global HeWeather updater."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=None,  # Disable built-in scheduler
        )
        self.api_host = api_host
        self.api_key = api_key
        self.location = location
        self.data = {}
        self._total_api_calls = 0
        self._successful_api_calls = 0
        self._update_lock = asyncio.Lock()
        self._unsub_schedule = None
        self._last_update_time = None
        self._next_update_time = None
        
        # 使用配置的更新间隔（秒）
        self.update_interval_seconds = update_interval
        self.scan_interval_seconds = update_interval  # 别名

    async def async_start(self):
        """Start periodic updates."""
        if self._unsub_schedule is None:
            self._unsub_schedule = async_track_time_interval(
                self.hass, 
                self._scheduled_update, 
                timedelta(seconds=self.update_interval_seconds)
            )
            minutes = self.update_interval_seconds // 60
            seconds = self.update_interval_seconds % 60
            _LOGGER.info("Scheduled updates every %d min %d sec", minutes, seconds)
        
        await self.async_refresh()

    async def async_shutdown(self):
        """Shutdown coordinator."""
        if self._unsub_schedule:
            self._unsub_schedule()
            self._unsub_schedule = None
            _LOGGER.debug("Cancelled scheduled updates")

    async def _scheduled_update(self, _now=None):
        """Scheduled update with lock."""
        async with self._update_lock:
            try:
                _LOGGER.debug("Executing scheduled update")
                await self.async_refresh()
            except Exception as err:
                _LOGGER.error("Error during scheduled update: %s", err, exc_info=True)

    async def _async_update_data(self):
        """Fetch data from API endpoints."""
        start_time = time.time()
        new_data = {}
        successful_calls = 0
        attempts = 0
        
        _LOGGER.info("Starting data update for HeWeather")
        
        # 确保使用从const导入的API_ENDPOINTS
        for endpoint_name, endpoint_path in API_ENDPOINTS.items():
            url = f"https://{self.api_host}{endpoint_path}?location={self.location}&key={self.api_key}"
            if endpoint_name == "indices":
                url += "&type=0"
            
            endpoint_data = None
            for attempt in range(3):
                attempts += 1
                try:
                    _LOGGER.debug("Requesting %s (attempt %d)", endpoint_name, attempt + 1)
                    async with async_timeout.timeout(15):
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as response:
                                response.raise_for_status()
                                result = await response.json()
                                
                                if result.get("code") != "200":
                                    raise UpdateFailed(f"API error: {result.get('message')}")
                                
                                if "updateTime" not in result:
                                    raise UpdateFailed("Missing updateTime in response")
                                
                                endpoint_data = result
                                successful_calls += 1
                                _LOGGER.debug("Successfully updated %s", endpoint_name)
                                break
                except Exception as err:
                    if attempt == 2:
                        _LOGGER.warning("Failed to update %s after 3 attempts: %s", 
                                      endpoint_name, str(err))
                        if endpoint_name in self.data:
                            endpoint_data = self.data[endpoint_name]
                            _LOGGER.debug("Using cached data for %s", endpoint_name)
                    continue
            
            if endpoint_data:
                new_data[endpoint_name] = endpoint_data

        # Update statistics
        self._total_api_calls += attempts
        self._successful_api_calls += successful_calls
        self._last_update_time = datetime.now()
        self._next_update_time = datetime.now() + timedelta(seconds=self.update_interval_seconds)
        
        # 仅保留必要信息
        new_data.update({
            "last_update": self._last_update_time.isoformat(),
            "next_update": self._next_update_time.isoformat(),
            "update_duration": time.time() - start_time,
        })
        
        minutes = self.update_interval_seconds // 60
        seconds = self.update_interval_seconds % 60
        _LOGGER.info(
            "Update completed. Success: %d/%d, Total API calls: %d, Duration: %.2fs, Next in %d min %d sec",
            successful_calls,
            len(API_ENDPOINTS),
            self._total_api_calls,
            new_data["update_duration"],
            minutes,
            seconds
        )
        
        return new_data

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up HeWeather from a config entry."""
    config = entry.data
    
    # 获取配置的更新间隔（秒），默认为900秒（15分钟）
    update_interval = config.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    
    coordinator = HeWeatherCoordinator(
        hass,
        config.get(CONF_API_HOST, DEFAULT_API_HOST),
        config[CONF_API_KEY],
        config[CONF_LOCATION],
        update_interval
    )
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    # Start the coordinator
    await coordinator.async_start()
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["weather", "sensor"])
    
    # Register unload callbacks
    entry.async_on_unload(coordinator.async_shutdown)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, ["weather", "sensor"]):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok