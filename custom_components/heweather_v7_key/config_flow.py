import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME

from .const import (
    DOMAIN, 
    CONF_API_HOST, 
    CONF_API_KEY, 
    CONF_LOCATION,
    CONF_UPDATE_INTERVAL,
    DEFAULT_API_HOST,
    DEFAULT_UPDATE_INTERVAL
)

_LOGGER = logging.getLogger(__name__)

# 时间范围：5分钟(300秒)到24小时(86400秒)
MIN_UPDATE_INTERVAL = 300
MAX_UPDATE_INTERVAL = 86400

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_HOST, default=DEFAULT_API_HOST): str,
    vol.Required(CONF_API_KEY): str,
    vol.Required(CONF_LOCATION): str,
    vol.Optional(CONF_NAME): str,
    vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(
        vol.Coerce(int), vol.Range(min=MIN_UPDATE_INTERVAL, max=MAX_UPDATE_INTERVAL)
    )
})

class HeWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HeWeather V7 Key."""
    
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            if not user_input.get(CONF_API_HOST):
                user_input[CONF_API_HOST] = DEFAULT_API_HOST
            
            if not user_input[CONF_API_KEY].strip():
                errors["base"] = "api_key_required"
            elif not user_input[CONF_LOCATION].strip():
                errors["base"] = "location_required"
            else:
                await self.async_set_unique_id(
                    f"heweather_{user_input[CONF_LOCATION].strip()}"
                )
                self._abort_if_unique_id_configured()
                
                name = user_input.get(CONF_NAME) or f"HeWeather {user_input[CONF_LOCATION]}"
                
                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_API_HOST: user_input[CONF_API_HOST],
                        CONF_API_KEY: user_input[CONF_API_KEY],
                        CONF_LOCATION: user_input[CONF_LOCATION],
                        CONF_NAME: name,
                        CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL]
                    },
                )
        
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return HeWeatherOptionsFlow(config_entry)

class HeWeatherOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for HeWeather V7 Key."""
    
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
    
    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # 更新配置条目数据
            new_data = {**self.config_entry.data, **user_input}
            self.hass.config_entries.async_update_entry(
                self.config_entry,
                data=new_data
            )
            return self.async_create_entry(title="", data={})
        
        # 显示当前配置值的表单
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_API_HOST,
                    default=self.config_entry.data.get(CONF_API_HOST, DEFAULT_API_HOST)
                ): str,
                vol.Required(
                    CONF_API_KEY,
                    default=self.config_entry.data.get(CONF_API_KEY, "")
                ): str,
                vol.Required(
                    CONF_LOCATION,
                    default=self.config_entry.data.get(CONF_LOCATION, "")
                ): str,
                vol.Optional(
                    CONF_NAME,
                    default=self.config_entry.data.get(CONF_NAME, "")
                ): str,
                vol.Required(
                    CONF_UPDATE_INTERVAL,
                    default=self.config_entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
                ): vol.All(vol.Coerce(int), vol.Range(min=MIN_UPDATE_INTERVAL, max=MAX_UPDATE_INTERVAL))
            })
        )