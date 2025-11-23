# 广东轻工网络准入认证自动登录脚本

## 项目简介

这是一个针对广东轻工职业技术大学网络准入认证系统（`http://10.0.5.112/`）的自动登录脚本，使用Selenium WebDriver和BeautifulSoup开发。

## 功能特性

- ✅ 自动打开目标网站
- ✅ 智能定位登录表单元素
- ✅ 安全的凭证填写机制
- ✅ 登录状态自动验证
- ✅ 完善的异常处理
- ✅ 详细的日志记录
- ✅ 自动截图功能
- ✅ 无头模式支持

## 环境要求

- Python 3.7+
- Chrome浏览器
- 稳定的网络连接

## 安装步骤

### 1. 克隆或下载项目

```bash
# 如果使用git
git clone <repository-url>
cd GDIPU_web_autoaccess_script

# 或者直接下载项目文件
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置登录凭证

编辑 `config.py` 文件，填写您的实际登录信息：

```python
# config.py
USERNAME = "2023233203314"  # 替换为您的用户名
PASSWORD = "your_password"  # 替换为您的密码
```

## 使用方法

### 基本使用

```bash
python gdiu_auto_login.py
```

### 使用配置文件

修改 `gdipu_auto_login.py` 中的主函数，使用配置文件：

```python
# 在主函数开头添加
from config import USERNAME, PASSWORD, HEADLESS

# 修改主函数中的变量
USERNAME = USERNAME
PASSWORD = PASSWORD
headless = HEADLESS
```

### 无头模式运行

在 `config.py` 中设置：

```python
HEADLESS = True  # 后台运行，不显示浏览器窗口
```

## 脚本功能详解

### 1. WebDriver初始化
- 自动下载和管理ChromeDriver
- 支持无头模式
- 设置合理的超时时间

### 2. 页面元素定位
- 使用ID定位用户名输入框（`username`）
- 使用ID定位密码输入框（`password`）
- 使用ID定位登录按钮（`login-account`）
- 智能等待元素加载

### 3. 登录流程
1. 打开目标网站
2. 等待页面加载完成
3. 定位登录表单元素
4. 填写用户名和密码
5. 点击登录按钮
6. 验证登录状态

### 4. 登录状态验证
- 检查登录按钮是否消失
- 捕获页面错误信息
- 提供详细的登录结果反馈

### 5. 异常处理
- 页面加载超时处理
- 元素定位失败处理
- 网络连接异常处理
- 浏览器异常处理

### 6. 日志系统
- 实时日志输出到控制台
- 日志文件保存到 `gdiu_login.log`
- 详细的错误信息记录

### 7. 截图功能
- 关键步骤自动截图
- 错误发生时保存截图
- 截图文件名包含时间戳

## 文件结构

```
GDIPU_web_autoaccess_script/
├── gdiu_auto_login.py    # 主脚本文件
├── config.py             # 配置文件模板
├── requirements.txt      # 依赖包列表
├── README.md            # 使用说明文档
└── gdiu_login.log       # 日志文件（运行后生成）
```

## 常见问题

### Q: 登录失败怎么办？
A: 检查以下内容：
1. 用户名和密码是否正确
2. 网络连接是否正常
3. 查看日志文件获取详细错误信息
4. 检查截图文件了解页面状态

### Q: 如何修改超时时间？
A: 在 `config.py` 中修改 `TIMEOUT` 参数。

### Q: 脚本运行太慢怎么办？
A: 可以适当减少等待时间，但要注意网络状况和页面加载速度。

## 安全提示

- 🔒 不要将包含真实密码的配置文件上传到公开仓库
- 🔒 定期更改密码
- 🔒 在安全的环境下运行脚本

## 技术支持

如果遇到问题，请：
1. 查看日志文件 `gdiu_login.log`
2. 检查截图文件了解页面状态
3. 确保依赖包已正确安装

## 更新日志

- v1.0.0 (2025-11-23): 初始版本发布
  - 实现基本登录功能
  - 添加异常处理和日志系统
  - 支持无头模式运行

---

*注意：本脚本仅供学习和合法使用，请遵守相关法律法规和网站使用条款。*