"""Sensor platform for HeWeather integration."""
import logging
from datetime import datetime
from homeassistant.components.sensor import SensorEntity

from .const import (
    DOMAIN,
    CONF_LOCATION,
    CONF_NAME,
    SENSOR_TYPES,
    ATTR_LAST_UPDATE,
    ATTR_SOURCE
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the HeWeather sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    location = config_entry.data[CONF_LOCATION]
    name = config_entry.data.get(CONF_NAME) or f"HeWeather {location}"
    
    for sensor_type, sensor_config in SENSOR_TYPES.items():
        entities.append(HeWeatherSensor(
            coordinator=coordinator,
            config_entry=config_entry,
            sensor_type=sensor_type,
            sensor_config=sensor_config,
            name=name
        ))
    
    async_add_entities(entities)

class HeWeatherSensor(SensorEntity):
    """Representation of a HeWeather sensor."""
    
    _attr_has_entity_name = True
    
    def __init__(self, coordinator, config_entry, sensor_type, sensor_config, name):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.config_entry = config_entry
        self._sensor_type = sensor_type
        self._attr_name = sensor_config["name"]
        self._attr_native_unit_of_measurement = sensor_config["unit"]
        self._attr_icon = sensor_config["icon"]
        self._data_type = sensor_config["data_type"]
        self._attr_device_class = sensor_config.get("device_class")
        self._attr_state_class = sensor_config.get("state_class")
        
        location = config_entry.data[CONF_LOCATION]
        self._attr_unique_id = f"heweather_{location}_{sensor_type}"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, location)},
            "name": name,
            "manufacturer": "HeWeather",
        }
    
    @property
    def available(self):
        """Return if entity is available."""
        # 修改为：meta类型始终可用（只要协调器成功更新）
        return self.coordinator.last_update_success and (
            self._data_type in self.coordinator.data or 
            self._data_type == "meta"
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        try:
            # 处理信息传感器
            if self._sensor_type == "info":
                return "正常"
                
            if self._sensor_type == "last_update":
                return self.coordinator.data.get("last_update", "N/A")
                        
            # Handle weather data sensors
            endpoint_data = self.coordinator.data.get(self._data_type, {})
            #当前天气
            if self._data_type == "current":
                now_data = endpoint_data.get("now", {})

                if self._sensor_type == "temperature":
                    return now_data.get("temp", 0)
                elif self._sensor_type == "feels_like":
                    return now_data.get("feelsLike", 0)
                
                elif self._sensor_type == "humidity":
                    return now_data.get("humidity", 0)
                
                elif self._sensor_type == "wind_scale":
                    return now_data.get("windScale", 0)
                
                elif self._sensor_type == "wind_speed":
                    return now_data.get("windSpeed", 0)
                
                elif self._sensor_type == "wind_direction":
                    return now_data.get("windDir", "N/A") 
                
                elif self._sensor_type == "precip":
                    return now_data.get("precip", 0.0)
                
                elif self._sensor_type == "pressure":
                    return now_data.get("pressure", 0)
                
                elif self._sensor_type == "vis":
                    return now_data.get("vis", 0)
                
                elif self._sensor_type == "cloud":
                    return now_data.get("cloud", 0)
                
                elif self._sensor_type == "dew":
                    return now_data.get("dew", 0)
                else:
                    return now_data.get(self._sensor_type, 0)

            #天气预警
            elif self._data_type == "warning":
                warnings = endpoint_data.get("warning", [])
                count = len(warnings)
                if self._sensor_type == "warning_count":
                    if count != 0:
                        return count
                    else:
                        return 0
                elif self._sensor_type == "warning_status":
                    if count != 0:
                        return "on"
                    else:
                        return "off"
            #空气质量
            elif self._data_type == "air":
                now_data = endpoint_data.get("now", {})
            
                if self._sensor_type == "aqi":
                    return now_data.get("aqi", 0)
            
                elif self._sensor_type == "air_quality_level":
                    return now_data.get("level", 0)
            
                elif self._sensor_type == "air_quality_category":
                    return now_data.get("category", "未知")
            
                elif self._sensor_type == "pm25":
                    return now_data.get("pm2p5", 0)
            
                elif self._sensor_type == "pm10":
                    return now_data.get("pm10", 0)
            
                elif self._sensor_type == "primary_pollutant":
                    return now_data.get("primary", "NA")
            
                elif self._sensor_type == "no2":
                    return now_data.get("no2", "NA")
            
                elif self._sensor_type == "so2":
                    return now_data.get("so2", "NA")
            
                elif self._sensor_type == "co":
                    return now_data.get("co", "NA")
            
                elif self._sensor_type == "o3":
                    return now_data.get("o3", "NA")

            #明天、后天天气 weather_today
            elif self._data_type == "forecast":
                daily_data = endpoint_data.get("daily", [])
                if self._sensor_type == "weather_today" and len(daily_data) > 0:
                    return daily_data[0].get("textDay", "N/A")
                if self._sensor_type == "weather_tomorrow" and len(daily_data) > 1:
                    return daily_data[1].get("textDay", "N/A")
                if self._sensor_type == "weather_day_after" and len(daily_data) > 2:
                    return daily_data[2].get("textDay", "N/A")

            #生活指数  
            elif self._data_type == "indices":
                daily_data = endpoint_data.get("daily", [])
                type_mapping = {
                    "sport_index": "1",
                    "car_washing_index": "2",
                    "dressing_index": "3",
                    "fishing_index": "4",
                    "uv_index": "5",
                    "tourism_index": "6",
                    "allergy_index": "7",
                    "comfort_index": "8",
                    "cold_index": "9",
                    "air_dispersion_index": "10",
                    "aircon_index": "11",
                    "sunglass_index": "12",
                    "makeup_index": "13",
                    "drying_index": "14",
                    "traffic_index": "15",
                    "sunscreen_index": "16"
                }
                target_type = type_mapping.get(self._sensor_type)
                if target_type:
                    for item in daily_data:
                        if item.get("type") == target_type:
                            return item.get("category", "N/A")
            
            return None
            
        except Exception as e:
            _LOGGER.error("Error getting sensor value for %s: %s", self._sensor_type, str(e))
            return None
    
    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        attrs = {
            ATTR_SOURCE: "HeWeather API V7",
            ATTR_LAST_UPDATE: self.coordinator.data.get("last_update", ""),
        }
        
        # 添加信息传感器的详细属性
        if self._sensor_type == "info":
            attrs.update({
                "api_calls": self.coordinator._total_api_calls,
                "successful_calls": self.coordinator._successful_api_calls,
                "last_update": self.coordinator._last_update_time.isoformat() if self.coordinator._last_update_time else "N/A",
                "next_update": self.coordinator._next_update_time.isoformat() if self.coordinator._next_update_time else "N/A",
                "update_duration": self.coordinator.data.get("update_duration", 0),
                "update_interval": self.coordinator.update_interval_seconds
            })
        
        # Add endpoint-specific attributes
        endpoint_data = self.coordinator.data.get(self._data_type, {})
        #当前天气属性
        if self._sensor_type == "wind_speed":
            now_data = endpoint_data.get("now", {})
            wind_dir = now_data.get("windDir", "")
            wind_scale = now_data.get("windScale", "")
            
            if wind_dir:
                attrs["wind_direction"] = wind_dir
            
            if wind_scale:
                attrs["wind_scale"] = wind_scale

        #告警状态属性
        elif self._sensor_type == "warning_status":
            warnings = endpoint_data.get("warning", [])
            count=len(warnings)
            if count==1:
                attrs["text"] = f"请注意：当前有1个天气预警！"
                attrs["title"]=warnings[0].get("title", "")
                attrs["level"]=warnings[0].get("level", "")
                attrs["typeName"]=warnings[0].get("typeName", "")
                attrs["description"]=warnings[0].get("text", "")
            elif count>=2:
                attrs["text"] = f"请注意：当前有 {count} 个天气预警！"
                for i, warning in enumerate(warnings, 1):
                    attrs[f"title{i}"] = warning.get("title", "")
                    attrs[f"level{i}"] = warning.get("level", "")
                    attrs[f"typeName{i}"] = warning.get("typeName", "")
                    attrs[f"description{i}"] = warning.get("text", "")
            else:
                attrs["text"] = "当前无任何天气预警！"

        #明天、后天天气属性 weather_today
        elif self._sensor_type == "weather_today":
            daily_data = endpoint_data.get("daily", [])
            if len(daily_data) > 0:
                day = daily_data[0]
                attrs.update({
                    "textDay": day.get("textDay", ""),
                    "textNight": day.get("textNight", ""),
                    "tempMax": day.get("tempMax", ""),
                    "tempMin": day.get("tempMin", ""),
                    "humidity": day.get("humidity", ""),
                    "text": f'白天：{day.get("textDay", "")}，晚上：{day.get("textNight", "")}。最高气温：{day.get("tempMax", "")}度，最低气温：{day.get("tempMin", "")}度。湿度：{day.get("humidity", "")}%。'
                })
        elif self._sensor_type == "weather_tomorrow":
            daily_data = endpoint_data.get("daily", [])
            if len(daily_data) > 1:
                day = daily_data[1]
                attrs.update({
                    "textDay": day.get("textDay", ""),
                    "textNight": day.get("textNight", ""),
                    "tempMax": day.get("tempMax", ""),
                    "tempMin": day.get("tempMin", ""),
                    "humidity": day.get("humidity", ""),
                    "text": f'白天：{day.get("textDay", "")}，晚上：{day.get("textNight", "")}。最高气温：{day.get("tempMax", "")}度，最低气温：{day.get("tempMin", "")}度。湿度：{day.get("humidity", "")}%。'
                })
        
        elif self._sensor_type == "weather_day_after":
            daily_data = endpoint_data.get("daily", [])
            if len(daily_data) > 2:
                day = daily_data[2]
                attrs.update({
                    "textDay": day.get("textDay", ""),
                    "textNight": day.get("textNight", ""),
                    "tempMax": day.get("tempMax", ""),
                    "tempMin": day.get("tempMin", ""),
                    "humidity": day.get("humidity", ""),
                    "text": f'白天：{day.get("textDay", "")}，晚上：{day.get("textNight", "")}。最高气温：{day.get("tempMax", "")}度，最低气温：{day.get("tempMin", "")}度。湿度：{day.get("humidity", "")}%。'
                })
        #生活指数  
        if self._data_type == "indices":
            daily_data = endpoint_data.get("daily", [])
            type_mapping = {
                "sport_index": "1",
                "car_washing_index": "2",
                "dressing_index": "3",
                "fishing_index": "4",
                "uv_index": "5",
                "tourism_index": "6",
                "allergy_index": "7",
                "comfort_index": "8",
                "cold_index": "9",
                "air_dispersion_index": "10",
                "aircon_index": "11",
                "sunglass_index": "12",
                "makeup_index": "13",
                "drying_index": "14",
                "traffic_index": "15",
                "sunscreen_index": "16"
            }
            target_type = type_mapping.get(self._sensor_type)
            if target_type:
                for item in daily_data:
                    if item.get("type") == target_type:
                        attrs.update({
                            "name": item.get("name", ""),
                            "level": item.get("level", ""),
                            "text": item.get("text", "")
                        })
                        break
        
        return attrs
    
    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(
                self.async_write_ha_state
            )
        )
    
    async def async_update(self):
        """Update the entity."""
        await self.coordinator.async_request_refresh()
    
    @property
    def should_poll(self):
        """No need to poll, coordinator notifies of updates."""
        return False