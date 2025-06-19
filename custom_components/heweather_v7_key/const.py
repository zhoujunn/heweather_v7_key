"""Constants for HeWeather V7 Key integration."""
DOMAIN = "heweather_v7_key"

CONF_API_HOST = "api_host"
CONF_API_KEY = "api_key"
CONF_LOCATION = "location"
CONF_NAME = "name"
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_API_HOST = "devapi.qweather.com"
DEFAULT_UPDATE_INTERVAL = 900  # 15分钟 = 900秒

API_ENDPOINTS = {
    "current": "/v7/weather/now",
    "forecast": "/v7/weather/7d",
    "warning": "/v7/warning/now",
    "air": "/v7/air/now",
    "indices": "/v7/indices/1d"
}

ATTR_LAST_UPDATE = "last_update"
ATTR_SOURCE = "data_source"

SENSOR_TYPES = {
    #now接口
    "temperature": {
        "name": "气温",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "data_type": "current"
   },
    "wind_direction": {
        "name": "风向",
        "unit": None,
        "icon": "mdi:weather-windy-variant",
        "data_type": "current"
   },
    "feels_like": {
        "name": "体感温度",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "data_type": "current"
    },
    "humidity": {
        "name": "湿度",
        "unit": "%",
        "icon": "mdi:water-percent",
        "data_type": "current"
    },
    "wind_scale": {
        "name": "风力等级",
        "unit": "级",
        "icon": "mdi:wind-power",
        "data_type": "current"
    },
    "wind_speed": {
        "name": "风速",
        "unit": "km/h",
        "icon": "mdi:weather-windy",
        "data_type": "current"
    },
    "precip": {
        "name": "过去1小时降水量",
        "unit": "mm",
        "icon": "mdi:weather-rainy",
        "data_type": "current"
    },
    "pressure": {
        "name": "大气压强",
        "unit": "hPa",
        "icon": "mdi:gauge",
        "data_type": "current"
    },
    "vis": {
        "name": "能见度",
        "unit": "km",
        "icon": "mdi:eye",
        "data_type": "current"
    },
    "cloud": {
        "name": "云量",
        "unit": "%",
        "icon": "mdi:weather-cloudy",
        "data_type": "current"
    },
    "dew": {
        "name": "露点温度",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "data_type": "current"
    },
    "weather_tomorrow": {
        "name": "明天天气",
        "unit": None,
        "icon": "mdi:weather-sunny-alert",
        "data_type": "forecast"
    },
    "weather_day_after": {
        "name": "后天天气",
        "unit": None,
        "icon": "mdi:weather-cloudy-clock",
        "data_type": "forecast"
    },

    #warning接口
    "warning_status": {
        "name": "天气预警",
        "unit": None,
        "icon": "mdi:alert-circle-outline",
        "data_type":"warning"
    },
    "warning_count": {
        "name": "预警数量",
        "unit": None,
        "icon": "mdi:alert",
        "data_type": "warning"
    },

    #air

    "aqi": {
        "name": "空气质量指数",
        "unit": "",
        "icon": "mdi:air-filter",
        "data_type": "air"
    },
    "pm25": {
        "name": "PM2.5",
        "unit": "μg/m³",
        "icon": "mdi:air-filter",
        "data_type": "air"
    },
    "pm10": {
        "name": "PM10",
        "unit": "μg/m³",
        "icon": "mdi:air-filter",
        "data_type": "air"
    },
    "primary_pollutant": {
        "name": "主要污染物",
        "unit": None,
        "icon": "mdi:alert-circle",
        "data_type": "air"
    },
    "air_quality_level": {
        "name": "空气质量等级",
        "unit": None,
        "icon": "mdi:numeric-1-circle",
        "data_type": "air"
    },
    "air_quality_category": {
        "name": "空气质量类别",
        "unit": None,
        "icon": "mdi:emoticon-happy-outline",
        "data_type": "air"
    },
    "no2": {
        "name": "二氧化氮",
        "unit": "μg/m³",
        "icon": "mdi:chemical-weapon",
        "data_type": "air"
    },
    "so2": {
        "name": "二氧化硫",
        "unit": "μg/m³",
        "icon": "mdi:cloud-outline",
        "data_type": "air"
    },
    "co": {
        "name": "一氧化碳",
        "unit": "mg/m³",
        "icon": "mdi:molecule-co",
        "data_type": "air"
    },
    "o3": {
        "name": "臭氧",
        "unit": "μg/m³",
        "icon": "mdi:weather-sunny-alert",
        "data_type": "air"
    },
    #生活指数
    "sport_index": {
        "name": "运动指数",
        "unit": None,
        "icon": "mdi:run",
        "data_type": "indices"
    },
    "car_washing_index": {
        "name": "洗车指数",
        "unit": None,
        "icon": "mdi:car-wash",
        "data_type": "indices"
    },
    "dressing_index": {
        "name": "穿衣指数",
        "unit": None,
        "icon": "mdi:tshirt-crew",
        "data_type": "indices"
    },
    "fishing_index": {
        "name": "钓鱼指数",
        "unit": None,
        "icon": "mdi:fish",
        "data_type": "indices"
    },
    "uv_index": {
        "name": "紫外线指数",
        "unit": None,
        "icon": "mdi:weather-sunny-alert",
        "data_type": "indices"
    },
    "tourism_index": {
        "name": "旅游指数",
        "unit": None,
        "icon": "mdi:map-marker-radius",
        "data_type": "indices"
    },
    "allergy_index": {
        "name": "过敏指数",
        "unit": None,
        "icon": "mdi:emoticon-sick",
        "data_type": "indices"
    },
    "comfort_index": {
        "name": "舒适度指数",
        "unit": None,
        "icon": "mdi:emoticon-happy-outline",
        "data_type": "indices"
    },
    "cold_index": {
        "name": "感冒指数",
        "unit": None,
        "icon": "mdi:face-mask",
        "data_type": "indices"
    },
    "air_dispersion_index": {
        "name": "空气污染扩散条件指数",
        "unit": None,
        "icon": "mdi:weather-windy",
        "data_type": "indices"
    },
    "aircon_index": {
        "name": "空调开启指数",
        "unit": None,
        "icon": "mdi:air-conditioner",
        "data_type": "indices"
    },
    "sunglass_index": {
        "name": "太阳镜指数",
        "unit": None,
        "icon": "mdi:sunglasses",
        "data_type": "indices"
    },
    "makeup_index": {
        "name": "化妆指数",
        "unit": None,
        "icon": "mdi:lipstick",
        "data_type": "indices"
    },
    "drying_index": {
        "name": "晾晒指数",
        "unit": None,
        "icon": "mdi:tumble-dryer",
        "data_type": "indices"
    },
    "traffic_index": {
        "name": "交通指数",
        "unit": None,
        "icon": "mdi:car",
        "data_type": "indices"
    },
    "sunscreen_index": {
        "name": "防晒指数",
        "unit": None,
        "icon": "mdi:weather-sunny-off",
        "data_type": "indices"
    }
}