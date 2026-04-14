# 电视剧数据爬取与可视化分析系统

基于 Flask + Requests + BeautifulSoup + Chart.js 开发的电视剧数据采集与分析平台。

## ✨ 核心功能

- **数据采集**：爬取爱奇艺电视剧排行榜，解析排名、名称、年份、主演、热度、类型
- **反爬策略**：模拟 Cookie 和 User-Agent 绕过反爬
- **增量更新**：通过 aid 字段去重，避免重复数据
- **数据可视化**：类型分布、历年趋势、热度分布、主演作品数量四类图表
- **Top25 榜单**：支持按年份/类型筛选与关键词搜索

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Flask |
| 爬虫 | Requests + BeautifulSoup |
| 数据库 | MySQL + PyMySQL |
| 前端 | HTML + CSS + JavaScript + Chart.js |

## 📡 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 首页 |
| `/charts` | GET | 数据分析页 |
| `/top25` | GET | Top25 榜单 |
| `/api/movies` | GET | 电影数据 API |
| `/api/stats` | GET | 统计数据 API |

## 👤 作者

- 求职方向：Java 后端 / AI 应用开发
- 2027 届本科应届
