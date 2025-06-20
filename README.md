# HeWeather V7 Key - 和风天气多城市集成

基于和风天气V7 API开发的多城市Home Assistant集成，完美解决原插件无法添加多个城市的问题。

## 功能亮点

- 🏙️ **真正多城市支持** - 可同时添加多个城市天气数据
- 📅 **增强预报功能** - 新增明天、后天天气专用传感器
- 🔄 **优化更新机制** - 智能API调用避免超额限制
- 🛠️ **配置简化** - 自动识别API Host，减少配置项

## 安装指南

### 通过HACS安装
1. 在HACS中搜索"heweather_v7_key"
2. 点击安装并重启HA

### 手动安装
```bash
cd /config/custom_components
git clone https://github.com/zhoujunn/heweather_v7_key.git
重启Home Assistant
