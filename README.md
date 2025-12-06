<div align="center">

# 📊 Subscription Tracker | 个人订阅管理助手

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap%205-purple)
![License](https://img.shields.io/badge/License-MIT-orange)

**一个极简、优雅的自托管订阅管理系统，帮助你掌控每一分数字支出。**

[功能特性](#-功能特性) • [安装部署](#-快速开始) • [截图展示](#-界面预览) • [技术栈](#-技术栈)

</div>

---

## 📖 项目简介

在这个“万物皆订阅”的时代，很容易忘记某个服务的续费时间或总支出。**Subscription Tracker** 是一个轻量级的 Web 应用，旨在解决这个问题。

它不仅能帮你记录 Netflix、Spotify、服务器 VPS 等服务的到期时间，还能自动将不同币种（USD, HKD, EUR...）按汇率折算为人民币进行统计，并提供精确到秒的倒计时和邮件提醒功能。

## ✨ 功能特性

- **⏳ 动态倒计时特效**：精确到秒的实时倒计时，到期前 7 天自动变红预警，视觉冲击力强。
- **💸 多币种自动折算**：支持 CNY, USD, HKD, EUR, JPY 等主流货币，自动汇率换算，总支出一目了然。
- **📧 智能邮件通知**：后台自动检测，距离到期日 7 天时自动发送邮件提醒，告别意外扣费。
- **🔐 安全后台管理**：内置登录拦截系统，保护您的隐私数据不外泄。
- **📱 响应式 UI 设计**：基于 Bootstrap 5 开发，在手机、平板和电脑上都能完美显示。
- **🚀 极速部署**：无需安装复杂数据库，基于 SQLite，开箱即用。

## 📸 界面预览

> *提示：此处建议上传您的运行截图*

| **仪表盘概览** | **添加订阅** |
|:---:|:---:|
| ![Dashboard](https://via.placeholder.com/600x400?text=Dashboard+Screenshot) | ![Add Modal](https://via.placeholder.com/600x400?text=Add+Subscription) |

## 🛠️ 技术栈

* **后端**: Python (Flask, SQLAlchemy, APScheduler, Flask-Mail)
* **前端**: HTML5, Bootstrap 5, JavaScript (ES6)
* **数据库**: SQLite (无需额外安装配置)

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone [https://github.com/weiruankeji2025/weiruan-sub.git](https://github.com/weiruankeji2025/weiruan-sub.git)
cd weiruan-sub
