# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import  re
import random
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

def data_cleaning(data):#这是清洗数据的
    if ' ' in data:
        data = re.sub(' ', '', data)
    if "'" in data:
        data = re.sub("'", '', data)
    if r'\n' in data:
        data = re.sub(r'\\n', '', data)
    return data

def common_click(driver,web_element,sleep_time=3):
    actions = ActionChains(driver)
    actions.move_to_element(web_element)
    actions.click(web_element)
    actions.perform()
    time.sleep(sleep_time
)

def register():#这是登录的函数，主要
    while True: #因为淘宝能够识别出selenium，有时我们会登录失败，会重新登录
        chrome_options = webdriver.ChromeOptions()#FirefoxOptions()
        chrome_options.add_argument('--headless') #无头浏览器,无界面模式这样爬取的时候不会弹出浏览器
        chrome_options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
        browser = webdriver.Chrome(chrome_options=chrome_options)#Firefox(firefox_options=chrome_options)
        #是在Chrome webdriver中，如果待操作元素不在视图显示范围内，则会报错
        browser.get('https://login.taobao.com/member/login.jhtml')#进入登录页面
        try:
            input = WebDriverWait(browser, 10).until(
                #presence_of_element_located验证元素是否出现
                EC.presence_of_element_located((By.CLASS_NAME, 'login-switch'))) #因为登录页面有时候是扫码登录，使用需要我们点击切换到密码登录
            common_click(browser, input)
        except Exception as e: #因为页面有时是直接密码登录，使用如果直接是密码登录就不需要点击
            print(e)
        time.sleep(random.random() * 2)
        wait = WebDriverWait(browser, 30)
        # user = browser.find_element(By.ID, 'TPL_username_1')
        user = wait.until(EC.presence_of_element_located((By.ID, 'TPL_username_1')))#visibility_of_all_elements_located验证元素是否可见
        #password = browser.find_element(By.ID, 'TPL_password_1')
        password = wait.until(EC.presence_of_element_located((By.ID, 'TPL_password_1')))#密码输入框
        #print(type(user))
        #time.sleep(random.random() * 2)
        user.clear()
        password.clear()
        user.send_keys('xxx') #输入账号并等待一下
        time.sleep(random.random() * 2)
        password.send_keys('xx')#输入密码并等待一下
        time.sleep(random.random() * 1)
        # 淘宝对selenium的识别主要是通过navigator.webdriver,使用selenium的浏览器api显示的是True，所有我们改成fALSE就可以过淘宝的检测
        browser.execute_script("Object.defineProperties(navigator,{webdriver:{get:() => false}})")
        action = ActionChains(browser)
        time.sleep(random.random() * 1)
        butt = browser.find_element(By.ID, 'nc_1_n1z')
        browser.switch_to.frame(browser.find_element(By.ID, '_oid_ifr_'))
        browser.switch_to.default_content()
        action.click_and_hold(butt).perform()
        action.reset_actions()
        action.move_by_offset(285, 0).perform()#输入账号密码后会有一个滑动验证
        time.sleep(random.random() * 1)
        button = browser.find_element(By.ID, 'J_SubmitStatic')#登录按钮
        time.sleep(random.random() * 2)
        common_click(browser, button)
        time.sleep(random.random() * 2)
        # browser.get('https://www.taobao.com/')
        cookie = browser.get_cookies()#获取cookies，原本想selenium实现登录，其他使用scrapy来，但是淘宝的商品搜索页的js找不到加上时间不够就没写了。
        cookies = {}#scrapy携带的cookies需要字典类型的
        for cookiez in cookie:
            name = cookiez['name']
            value = cookiez['value']
            cookies[name] = value
        #登录成功就退出
        ''''''
        if len(cookies) > 0:
            break
        else:
            browser.close()
    return browser,cookies
#register()