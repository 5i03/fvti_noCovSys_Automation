# Generated by Selenium IDE
import ping3
import argparse
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import sys
import requests
import base64
# import importlib
# importlib.reload(sys)
# sys.setdefaultencoding('utf-8')
def ping_host(dest_addr):
  '''
  获取节点的延迟的作用
  :param node:
  :return:
  '''
  response = ping3.ping(dest_addr,unit='ms')
  print(response)
  if response is not None:
    delay = int(response)
    print(delay, '毫秒延迟')
    # 下面两行新增的 
def begain_selenium(b,uid,pwd):
  msg='正在初始化'
  print(msg)
  if b == 'chrome':
    driver = webdriver.Chrome()
  elif b == 'firefox':
    driver = webdriver.Firefox()
  elif b == 'edge':
    driver = webdriver.Edge()
  elif b == 'ie':
    driver == webdriver.Ie()
  elif b == 'safari':
    driver == webdriver.Safari()
  else:
    print('未知浏览器')
    exit()
  msg='正在启动浏览器'
  print(msg)
  driver.get('http://health.fvti.linyisong.top/')
  msg='正在设置窗口大小'
  print(msg)
  driver.set_window_size(540, 420)
  msg='正在定位账号输入框位'
  print(msg)
  driver.find_element(By.ID, 'userCode').click()
  msg='正在模拟输入账号'
  print(msg)
  driver.find_element(By.ID, 'userCode').send_keys(uid)
  msg='正在定位密码输入框位'
  print(msg)
  driver.find_element(By.ID, 'userPwd').click()
  msg='正在输入密码'
  print(msg)
  driver.find_element(By.ID, 'userPwd').send_keys(pwd)
  msg='正在定位验证码图像位置'
  print(msg)
  imgelement = driver.find_element(By.ID,'loginCaptchaImage')
  msg='正在截取验证码图像'
  print(msg)
  imgelement.screenshot('captcha.jpg')
  msg='正在唤起OCR识别验证码'
  print(msg)
  # img=requests.get('http://health.fvti.linyisong.top/style/v1/images/login/img.jsp?='+str(Date))
  msg='正在读取保存的验证码图像'
  print(msg)
  with open('captcha.jpg', 'rb') as f:
      img_bytes = f.read()
  api_host='api.5i03.cn'
  msg='正在请求接口识别图像'+str(ping_host(api_host))
  print(msg)

  requests.packages.urllib3.disable_warnings()
  cap_ocr_res=requests.post('https://'+api_host+'/api/ocr/ddddocr/ocr/b64/text',data=base64.b64encode(img_bytes).decode(),verify=False).text
  msg='正在等待接口识别并返回验证码，OCR接口返回的验证码文本是'+str(cap_ocr_res)
  print(msg)
  time.sleep(3)
  msg='正在定位验证码输入框'
  print(msg)
  driver.find_element(By.ID, 'loginCaptcha').click()
  msg='正在开始输入验证码'
  print(msg)
  driver.find_element(By.ID, 'loginCaptcha').send_keys(cap_ocr_res)
  time.sleep(3)
  # driver.find_element(By.CSS_SELECTOR, 'tr:nth-child(5) > td:nth-child(2)').click()
  msg='正在定位记住密码选框'
  print(msg)
  driver.find_element(By.ID, 'mindpwd').click()
  msg='正在定位登录按钮'
  print(msg)
  driver.find_element(By.ID, 'loginBtn').click()
  msg='正在等待登录结果'
  print(msg)
  titlle_text='/html/body/div[1]/div/div/div[1]/span'
  if driver.find_element(By.XPATH, titlle_text).text == '福州职业技术学院疫情防控管理系统':
    msg='登陆成功正在取得cookie'
    print(msg)
    cookie_res=driver.get_cookie('JSESSIONID') #JSESSIONID 是电脑版登录时使用的鉴权方式
    print('你的cookie是:\n'+str(cookie_res)+'\nCookie一般2小时内有效')
    # 把cookie_res写入cookie.json
    with open(os.path.normpath(sys.path[0]+'/cookie.json'),'w') as f:
      json.dump(cookie_res,f)
    f.close()
    msg='正在关闭浏览器'
    print(msg)
    driver.close()
    msg='正在退出驱动'
    print(msg)
    driver.quit()
    pass
  else:
    msg='登录失败,可能是账户密码错误或者验证码错误'
    msg+= '请检查后重新运行'
    print(msg)
    driver.close()
    driver.quit()
    exit()

parse = argparse.ArgumentParser(prog='Login as fvti\'s Get JSESSION' ,description = '拟人登录福州职业技术学院疫情防控管理系统')
parse.add_argument('-d', '--driver', help='指定的浏览器驱动器,可选值为chrome,edge,firefox,safari默认为edge', default='edge')
parse.add_argument('-u','--user', help='用户', required=True)
parse.add_argument('-p','--password', help='密码', required=True)
parse.parse_args()
parse.print_help()
args = parse.parse_args()
begain_selenium(args.driver,args.user,args.password)
