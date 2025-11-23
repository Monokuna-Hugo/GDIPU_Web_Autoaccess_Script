#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广东轻工网络准入认证自动登录脚本
Author: Monokuna-hugo
Date: 2025-11-23
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class GDIPUAutoLogin:
    """广东轻工网络准入认证自动登录类"""
    
    def __init__(self, username: str, password: str, headless: bool = False):
        """
        初始化登录类
        
        Args:
            username (str): 用户名
            password (str): 密码
            headless (bool): 是否无头模式，默认False
        """
        self.username = username
        self.password = password
        self.headless = headless
        self.driver = None
        self.target_url = "http://10.0.5.112/"
        
        # 配置日志
        self._setup_logging()
        
    def _setup_logging(self):
        """配置日志系统"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gdiu_login.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """设置WebDriver"""
        try:
            chrome_options = Options()
            
            # 无头模式设置
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # 其他浏览器选项
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # 使用webdriver-manager自动管理ChromeDriver
            service = Service(executable_path="./chromedriver.exe")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            self.logger.info("WebDriver初始化成功")
            return True
            
        except Exception as e:
            self.logger.error(f"WebDriver初始化失败: {str(e)}")
            return False
    
    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        """
        等待元素出现
        
        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间（秒）
            
        Returns:
            WebElement or None
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.warning(f"元素定位超时: {by}={value}")
            return None
    
    def open_target_website(self):
        """打开目标网站"""
        try:
            self.logger.info(f"正在打开目标网站: {self.target_url}")
            self.driver.get(self.target_url)
            
            # 等待页面加载完成
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 处理网络连接错误的确认对话框
            if self.handle_network_error_dialog():
                self.logger.info("网络连接错误对话框已处理")
            else:
                self.logger.info("未检测到网络连接错误对话框")
            
            self.logger.info("网站打开成功")
            return True
            
        except TimeoutException:
            self.logger.error("页面加载超时")
            return False
        except WebDriverException as e:
            self.logger.error(f"打开网站失败: {str(e)}")
            return False
    
    def handle_network_error_dialog(self):
        """处理网络连接错误的确认对话框"""
        try:
            # 等待对话框出现
            dialog = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dialog.confirm.active"))
            )
            
            self.logger.info("检测到网络连接错误对话框")
            
            # 定位确认按钮
            confirm_button = dialog.find_element(By.CLASS_NAME, "btn-confirm")
            
            # 点击确认按钮
            confirm_button.click()
            self.logger.info("已点击确认按钮")
            
            # 等待对话框消失
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "dialog.confirm.active"))
            )
            
            # 短暂等待确保页面稳定
            time.sleep(2)
            
            self.logger.info("网络连接错误对话框处理完成")
            return True
            
        except TimeoutException:
            # 对话框未出现，属于正常情况
            return False
        except Exception as e:
            self.logger.error(f"处理网络连接错误对话框失败: {str(e)}")
            return False
    
    def locate_login_elements(self):
        """定位登录相关元素"""
        elements = {}
        
        # 定位用户名输入框
        username_field = self.wait_for_element(By.ID, "username")
        if username_field:
            elements['username'] = username_field
            self.logger.info("用户名输入框定位成功")
        else:
            self.logger.error("用户名输入框定位失败")
            return None
        
        # 定位密码输入框
        password_field = self.wait_for_element(By.ID, "password")
        if password_field:
            elements['password'] = password_field
            self.logger.info("密码输入框定位成功")
        else:
            self.logger.error("密码输入框定位失败")
            return None
        
        # 定位登录按钮
        login_button = self.wait_for_element(By.ID, "login-account")
        if login_button:
            elements['login_button'] = login_button
            self.logger.info("登录按钮定位成功")
        else:
            self.logger.error("登录按钮定位失败")
            return None
        
        return elements
    
    def fill_login_credentials(self, elements: dict):
        """填写登录凭证"""
        try:
            # 清空并填写用户名
            elements['username'].clear()
            elements['username'].send_keys(self.username)
            self.logger.info("用户名填写完成")
            
            # 清空并填写密码
            elements['password'].clear()
            elements['password'].send_keys(self.password)
            self.logger.info("密码填写完成")
            
            # 短暂等待确保输入完成
            time.sleep(1)
            return True
            
        except Exception as e:
            self.logger.error(f"填写登录凭证失败: {str(e)}")
            return False
    
    def click_login_button(self, elements: dict):
        """点击登录按钮"""
        try:
            elements['login_button'].click()
            self.logger.info("登录按钮点击成功")
            
            # 等待登录操作完成
            time.sleep(5)
            return True
            
        except Exception as e:
            self.logger.error(f"点击登录按钮失败: {str(e)}")
            return False
    
    def verify_login_status(self):
        """验证登录状态"""
        try:
            # 等待页面稳定
            time.sleep(2)
            
            # 检查登录按钮是否还存在
            login_button_exists = False
            try:
                self.driver.find_element(By.ID, "login-account")
                login_button_exists = True
            except NoSuchElementException:
                login_button_exists = False
            
            # 根据登录按钮是否存在判断登录状态
            if not login_button_exists:
                self.logger.info("登录状态验证: 登录成功")
                return True
            else:
                self.logger.warning("登录状态验证: 登录按钮仍然存在，可能登录失败")
                
                # 检查是否有错误信息
                try:
                    error_elements = self.driver.find_elements(By.CLASS_NAME, "error")
                    for error in error_elements:
                        self.logger.error(f"页面错误信息: {error.text}")
                except:
                    pass
                
                return False
                
        except Exception as e:
            self.logger.error(f"登录状态验证失败: {str(e)}")
            return False
    
    def take_screenshot(self, filename: str = None):
        """截取屏幕截图"""
        try:
            if not filename:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            self.driver.save_screenshot(filename)
            self.logger.info(f"截图已保存: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"截图失败: {str(e)}")
            return None
    
    def login(self):
        """执行完整的登录流程"""
        self.logger.info("开始执行自动登录流程")
        
        try:
            # 1. 初始化WebDriver
            if not self.setup_driver():
                return False
            
            # 2. 打开目标网站
            if not self.open_target_website():
                self.cleanup()
                return False
            
            # 3. 定位登录元素
            elements = self.locate_login_elements()
            if not elements:
                self.take_screenshot("element_locate_failed.png")
                self.cleanup()
                return False
            
            # 4. 填写登录凭证
            if not self.fill_login_credentials(elements):
                self.take_screenshot("credential_fill_failed.png")
                self.cleanup()
                return False
            
            # 5. 点击登录按钮
            if not self.click_login_button(elements):
                self.take_screenshot("login_click_failed.png")
                self.cleanup()
                return False
            
            # 6. 验证登录状态
            login_success = self.verify_login_status()
            
            if login_success:
                self.logger.info("=== 登录成功 ===")
                self.take_screenshot("login_success.png")
                return True
            else:
                self.logger.error("=== 登录失败 ===")
                self.take_screenshot("login_failed.png")
                return False
                
        except Exception as e:
            self.logger.error(f"登录流程执行异常: {str(e)}")
            self.take_screenshot("login_exception.png")
            return False
    
    def cleanup(self):
        """清理资源"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver已关闭")
            except:
                pass


def main():
    """主函数"""
    # 从配置文件导入设置
    try:
        from config import USERNAME, PASSWORD, HEADLESS, TIMEOUT
    except ImportError:
        print("⚠️  配置文件未找到，使用默认设置")
        # 默认配置
        USERNAME = "2023233203314"  # 替换为您的用户名
        PASSWORD = "hugolee310.."  # 替换为您的密码
        HEADLESS = False
        TIMEOUT = 30
    
    # 创建登录实例
    login = GDIPUAutoLogin(username=USERNAME, password=PASSWORD, headless=HEADLESS)
    
    try:
        # 执行登录
        success = login.login()
        
        if success:
            print("\n✅ 登录成功！")
            print("登录日志已保存到: gdipu_login.log")
            print("截图已保存到当前目录")
        else:
            print("\n❌ 登录失败！")
            print("请查看日志文件 gdipu_login.log 获取详细错误信息")
        
        return success
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
        login.cleanup()
        return False
    
    finally:
        # 确保资源被清理
        login.cleanup()


if __name__ == "__main__":
    main()