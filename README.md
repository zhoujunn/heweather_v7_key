# 🌦️ HeWeather V7 for Home Assistant

`heweather_v7_key` 是一个用于接入 [和风天气 V7 API](https://dev.qweather.com/) 的 Home Assistant 自定义集成插件，支持实时天气、空气质量、生活指数、灾害预警等多种气象服务。

> ✅ 支持通过 HACS 安装，也支持手动安装。  
> 🔑 使用前请在和风天气官网申请 API Key（免费开发版即可）。

---

## ✨ 特性一览

- ✅ 支持以下和风天气接口：
  - `/v7/weather/now`：实时天气
  - `/v7/weather/7d`：天气预报
  - `/v7/air/now`：实时空气质量
  - `/v7/warning/now`：气象灾害预警
  - `/v7/indices/1d`：生活指数（运动、紫外线等）

- ✅ 提供以下实体类型：
  - `weather.nanjing_城市名`（天气卡片组件）
  - `sensor.nanjing_*`（温度、湿度、空气质量、各类指数、预警等）
- ✅ 中文 `friendly_name` + 天气图标支持
- ✅ 多城市支持（可添加多个集成实例）

---

## 🧩 安装方法

### 📦 方法一：通过 HACS 安装（推荐）

1. 打开 Home Assistant → HACS → 集成 → 三点菜单 → 自定义仓库。
2. 添加仓库地址：

```
https://github.com/zhoujunn/heweather_v7_key
```

类型选择为：**Integration**

3. 安装后重启 Home Assistant。
4. 在 “设备与服务” → “添加集成” 中搜索 `HeWeather` 进行配置。

### 📁 方法二：手动安装

```bash
cd config/custom_components
git clone https://github.com/zhoujunn/heweather_v7_key.git heweather_v7_key
重启 Home Assistant 后添加集成。
```

## ⚙️ 配置参数说明
在添加集成时，你需要填写以下参数：

参数字段	说明
API Key	从 和风天气控制台 获取的 key
Location	城市代码，例如：101010100 表示北京市（可参考下方城市代码示例）
城市名称	任意命名，仅用于实体命名后缀（如 nanjing）建议使用拼音或英文

示例：

API Key：1234567890abcdef

Location：101190101（南京）

城市名称：nanjing

📄 License
本项目遵循 MIT License。

🙏 致谢
和风天气 提供的高质量天气数据 API。

感谢 Home Assistant 社区的启发与支持。

🧊 欢迎提交 Issue 或 PR 一起完善功能！如需更多定制化支持，可通过 GitHub 联系作者。
