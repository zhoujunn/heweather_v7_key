from homeassistant.components.weather import (
    WeatherEntity,
    WeatherEntityFeature,
    Forecast,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_NATIVE_TEMP,
    ATTR_FORECAST_NATIVE_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_TEMPERATURE,
    ATTR_WEATHER_WIND_BEARING,
    ATTR_WEATHER_WIND_SPEED,
    ATTR_WEATHER_VISIBILITY,
)

from .const import (
    DOMAIN,
    CONF_LOCATION,
    CONF_NAME,
    ATTR_LAST_UPDATE
)

HEWEATHER_CONDITION_MAP = {
    "晴": "sunny",
    "少云": "partlycloudy",
    "晴间多云": "partlycloudy",
    "多云": "cloudy",
    "阴": "cloudy",
    "有风": "windy",
    "平静": "windy",
    "微风": "windy",
    "和风": "windy",
    "清风": "windy",
    "强风/劲风": "windy",
    "疾风": "windy",
    "大风": "windy",
    "烈风": "windy",
    "风暴": "windy",
    "狂爆风": "windy",
    "飓风": "windy",
    "热带风暴": "windy",
    "阵雨": "rainy",
    "雷阵雨": "lightning-rainy",
    "雷阵雨伴有冰雹": "lightning-rainy",
    "小雨": "rainy",
    "中雨": "rainy",
    "大雨": "pouring",
    "暴雨": "pouring",
    "大暴雨": "pouring",
    "特大暴雨": "pouring",
    "强阵雨": "pouring",
    "强雷阵雨": "lightning-rainy",
    "雨夹雪": "snowy-rainy",
    "阵雨夹雪": "snowy-rainy",
    "冻雨": "snowy-rainy",
    "小雪": "snowy",
    "中雪": "snowy",
    "大雪": "snowy",
    "暴雪": "snowy",
    "浮尘": "fog",
    "扬沙": "fog",
    "沙尘暴": "fog",
    "强沙尘暴": "fog",
    "雾": "fog",
    "霾": "fog",
    "浓雾": "fog",
    "强浓雾": "fog",
    "中度霾": "fog",
    "重度霾": "fog",
    "严重霾": "fog",
    "热": "sunny",
    "冷": "snowy",
    "未知": "exceptional"
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the weather platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    location = config_entry.data[CONF_LOCATION]
    name = config_entry.data.get(CONF_NAME) or f"HeWeather {location}"
    
    async_add_entities([HeWeatherEntity(coordinator, config_entry, name)])

class HeWeatherEntity(WeatherEntity):
    """Representation of HeWeather data."""
    
    _attr_has_entity_name = True
    _attr_supported_features = (
        WeatherEntityFeature.FORECAST_DAILY
    )
    
    def __init__(self, coordinator, config_entry, name):
        self.coordinator = coordinator
        self.config_entry = config_entry
        self._attr_name = name
        self._attr_unique_id = f"heweather_{config_entry.data[CONF_LOCATION]}_weather"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.data[CONF_LOCATION])},
            "name": name,
            "manufacturer": "HeWeather",
        }
    
    @property
    def available(self):
        """Return if entity is available."""
        # 添加对"current"键的检查
        return self.coordinator.last_update_success and "current" in self.coordinator.data
    
    @property
    def condition(self):
        """Return the current condition."""
        current_data = self.coordinator.data.get("current", {})
        condition_text = current_data.get("now", {}).get("text", "")
        return HEWEATHER_CONDITION_MAP.get(condition_text, "exceptional")
    
    @property
    def native_temperature(self):
        """Return the temperature."""
        current_data = self.coordinator.data.get("current", {})
        temp = current_data.get("now", {}).get("temp", 0)
        try:
            return float(temp)
        except (TypeError, ValueError):
            return 0
    
    @property
    def native_temperature_unit(self):
        return "°C"
    
    @property
    def humidity(self):
        current_data = self.coordinator.data.get("current", {})
        humidity = current_data.get("now", {}).get("humidity", 0)
        try:
            return float(humidity)
        except (TypeError, ValueError):
            return 0
    
    @property
    def native_wind_speed(self):
        current_data = self.coordinator.data.get("current", {})
        wind_speed = current_data.get("now", {}).get("windSpeed", 0)
        try:
            return float(wind_speed)
        except (TypeError, ValueError):
            return 0
    
    @property
    def wind_bearing(self):
        current_data = self.coordinator.data.get("current", {})
        return current_data.get("now", {}).get("windDir", "")
    
    @property
    def native_pressure(self):
        current_data = self.coordinator.data.get("current", {})
        pressure = current_data.get("now", {}).get("pressure", 0)
        try:
            return float(pressure)
        except (TypeError, ValueError):
            return 0
    
    @property
    def native_visibility(self):
        current_data = self.coordinator.data.get("current", {})
        vis = current_data.get("now", {}).get("vis", 0)
        try:
            return float(vis)
        except (TypeError, ValueError):
            return 0
    
    @property
    def attribution(self):
        """Return the attribution."""
        current_data = self.coordinator.data.get("current", {})
        sources = current_data.get("refer", {}).get("sources", [])
        return f"Data from: {', '.join(sources)}" if sources else "HeWeather API V7"
    
    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        attrs = {
            ATTR_LAST_UPDATE: self.coordinator.data.get("last_update", "")
        }
        
        # 添加对"current"键的检查
        current_data = self.coordinator.data.get("current", {})
        wind_scale = current_data.get("now", {}).get("windScale", "")
        if wind_scale:
            attrs["wind_scale"] = wind_scale
        
        return attrs
    
    async def async_forecast_daily(self):
        """Return the daily forecast."""
        forecasts = []
        # 添加对"forecast"键的检查
        forecast_data = self.coordinator.data.get("forecast", {})
        daily_data = forecast_data.get("daily", [])
        
        for day in daily_data[:7]:
            try:
                condition_text = day.get("textDay", "")
                forecast = {
                    ATTR_FORECAST_TIME: day.get("fxDate", ""),
                    ATTR_FORECAST_CONDITION: HEWEATHER_CONDITION_MAP.get(condition_text, "exceptional"),
                    ATTR_FORECAST_NATIVE_TEMP: float(day.get("tempMax", 0)),
                    ATTR_FORECAST_NATIVE_TEMP_LOW: float(day.get("tempMin", 0))
                }
                forecasts.append(forecast)
            except (TypeError, ValueError) as e:
                _LOGGER.error("Error parsing daily forecast data: %s", e)
                continue
        
        return forecasts
    
    async def async_update(self):
        await self.coordinator.async_request_refresh()
    
    @property
    def should_poll(self):
        return False