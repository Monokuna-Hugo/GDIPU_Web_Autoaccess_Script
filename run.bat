@echo off
chcp 65001 >nul
echo ========================================
echo   广东轻工网络准入认证自动登录脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo ✅ Python环境检测正常
echo.

REM 检查依赖是否安装
if not exist "requirements.txt" (
    echo ❌ 依赖文件不存在
    pause
    exit /b 1
)

echo 📦 正在检查依赖包...
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  依赖包未安装，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
) else (
    echo ✅ 依赖包已安装
)

echo.
echo 🚀 启动自动登录脚本...
echo.

REM 运行主脚本
python gdiu_auto_login.py

if errorlevel 1 (
    echo.
    echo ❌ 脚本执行失败
) else (
    echo.
    echo ✅ 脚本执行完成
)

echo.
pause