# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Escape Unescape 加密
value_fromstation = '%u5317%u6234%u6cb3%2CIOQ'  # 始发站
value_tostation = '%u5317%u4eac%2CIXQ'  # 终点站
value_date = '2017-09-30'  # 出发时间


def login_proc(username, password):
    # 打开登录页面
    sel = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    # sel=webdriver.Firefox()
    sel.implicitly_wait(30)
    login_url = 'https://kyfw.12306.cn/otn/login/init'
    sel.get(login_url)
    # 登录用户名
    try:
        user_input = sel.find_element_by_id("username")
        user_input.clear()
        user_input.send_keys(username)
        print 'user-id write success!'
    except:
        print 'user-id write error!'
    # 登录密码
    try:
        pwd_input = sel.find_element_by_id("password")
        pwd_input.clear()
        pwd_input.send_keys(password)
        print 'pw write success!'
    except:
        print 'pw write error!'

    # 检测是否登录成功
    while True:
        curpage_url = sel.current_url
        if curpage_url != login_url:
            if curpage_url[:-1] != login_url:  # 选择验证图片
                print 'Login finished!'
                break
        else:
            time.sleep(5)
            print u'------------>等待用户图片验证'
    return sel


def search_proc(sel, train_type='', timer=False):
    print u'--------->选择车次类型', train_type
    # 定时抢票时间点
    if timer == True:
        while True:
            current_time = time.localtime()
            if ((current_time.tm_hour >= 00) and (current_time.tm_min >= 00) and (
                        current_time.tm_sec >= 00)):
                print u'开始刷票...'
                break
            else:
                time.sleep(5)
                if current_time.tm_sec % 30 == 0:
                    print time.strftime('%H:%M:%S', current_time)

    # 打开订票网页
    book_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    sel.get(book_url)
    # 始发站
    sel.find_element_by_id('fromStationText').click()
    from_station = sel.find_element_by_xpath('//*[@id="ul_list1"]/li[32]')
    from_station.click()
    time.sleep(3000)
    sel.add_cookie({"name": "_jc_save_fromStation", "value": value_fromstation})
    # 终点站
    sel.find_element_by_id('toStationText').click()
    sel.find_element_by_id('nav_list3').click()#点击事件
    tation = sel.find_element_by_xpath('//*[@id="ul_list1"]/li[9]')
    to_station.click()
    time.sleep(3000)
    sel.add_cookie({"name": "_jc_save_toStation", "value": value_tostation})
    # 出发日期
    date_sel = sel.find_element_by_id('train_date')
    js = "document.getElementById('train_date').removeAttribute('readonly')" # del train_date readonly property
    sel.execute_script(js)
    date_sel.clear()
    date_sel.send_keys(leave_date)
    time.sleep(3000)
    sel.add_cookie({"name": "_jc_save_fromDate", "value": value_date})
    sel.refresh()
    # 车次类型选择
    train_type_dict = {'T': '//input[@name="cc_type" and @value="T"]',  # 特快
                       'G': '//input[@name="cc_type" and @value="G"]',  # 高铁
                       'D': '//input[@name="cc_type" and @value="D"]',  # 动车
                       'Z': '//input[@name="cc_type" and @value="Z"]',  # 直达
                       'K': '//input[@name="cc_type" and @value="K"]'}  # 普快
    if train_type == 'T' or train_type == 'G' or train_type == 'D' or train_type == 'Z' or train_type == 'K':
        # time.sleep(3000)
        sel.find_element_by_xpath(train_type_dict[train_type]).click()
    else:
        print u"车次类型异常或未选择!(train_type=%s)" % train_type


def book_proc(sel, refresh_interval=0):
    # 等待状态查询
    query_times = 0
    time_begin = time.time()
    while True:
        # 循环查询
        time.sleep(refresh_interval)
        # 开始查询 @id="ZE_6c000D281201"
        search_btn = WebDriverWait(sel, 2).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="query_ticket"]')))
        search_btn.click()
        sel.find_element_by_xpath('//*[@id="ticket_020000K3400Z"]/td[13]/a').click()
        print 1111111
        break
        # 扫描查询结果
        
        try:
            tic_tb_item = WebDriverWait(sel, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ZE_6i000G291204"]')))
            tic_ava_num = tic_tb_item.text
            break
        except:  # 应对查询按钮一次点击后,网站未返回查询结果
            search_btn.click()
            tic_tb_item = WebDriverWait(sel, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ZE_6i000G291204"]')))
            tic_ava_num = tic_tb_item.text
        

    # 判断页面跳是否转至乘客选择页面
    cust_sel_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    while True:
        if (sel.current_url == cust_sel_url):
            print u'页面跳转成功!'
            break
        else:
            print u'等待页面跳转...'
    # 乘车人选择
    while True:
        try:
            sel.find_element_by_xpath('//*[@id="normalPassenger_0"]').click()
            break
        except:
            print u'等待常用联系人列表...'

    # 席别选择
    # 提交订票
    sel.find_element_by_xpath('//*[@id="submitOrder_id"]').click()
    # 确认订票信息
    while True:
        try:
            sel.find_element_by_xpath('//*[@id="qr_submit_id"]').click()
            print 'Pass!'
            break
        except:
            print u'请手动通过图片验证码'
            time.sleep(5)
            break
    return 'yeah'


if __name__ == '__main__':
    # 变量定义
    leave_date = '2017-09-30'
    train_type = 'K'
    refresh_interval = 0.1
    timer = False

    sel = login_proc('***********', '*******')
    search_proc(sel, train_type, timer)
    book_proc(sel, refresh_interval)


