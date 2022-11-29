import json
import time
import requests
from datetime import datetime
from selenium import webdriver

jquery = open("jquery.min.js", "r").read()

with open('config.json', 'r') as reader:
    json_data = json.loads(reader.read())

course_no = json_data['course_no']
student_no = json_data['student_no']
password = json_data['password']


chrome_path = "./chromedriver"
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')

web = webdriver.Chrome(chrome_path)
web.get('https://courseselection.ntust.edu.tw/Account/Login')
web.find_element_by_name("UserName").send_keys(student_no)
web.find_element_by_name("Password").send_keys(password)
web.find_element_by_id("VerifyCode").send_keys(input("請輸入驗證碼："))
web.find_element_by_class_name("btn.btn-raised.btn-warning").click()

time.sleep(3)
web.find_element_by_name("UserName").send_keys(student_no)
web.find_element_by_name("Password").send_keys(password)
web.find_element_by_id("VerifyCode").send_keys(input("請輸入驗證碼："))
web.find_element_by_class_name("btn.btn-raised.btn-warning").click()


web.get('https://courseselection.ntust.edu.tw/First/A06/A06')
time_pre = time.time()
while True:
    time_now = time.time()
    if time_now - time_pre >= 10:
        time_pre = time_now
        web.get('https://courseselection.ntust.edu.tw/First/A06/A06')

    r = requests.get(
        'https://querycourse.ntust.edu.tw/QueryCourse/api/coursedetials?semester=1082&course_no=' + course_no + '&language=zh')

    data = r.json()[0]
    choose_student = int(data['ChooseStudent'])
    restrict = int(data['Restrict2'])


# https://courseselection.ntust.edu.tw/First/A06/ExtraJoin
# /AddAndSub/B01/ExtraJoin',

    if choose_student < restrict:
        ajax_query = '''
                    $.ajax({
                        url: '/First/A06/ExtraJoin',
                        type: "POST",
                        dataType: "html",
                        data: {
                            CourseNo: '%s',
                            type: 3
                        },
                        success: function (response) {
                            $(location).attr('href', 'A06');

                        },
                        error: function (xhr, ajaxOptions, thrownError) {
                            alert("系統錯誤!");
                            $(location).attr('href', 'A06');
                        }
                    });
                    ''' % (course_no)
        ajax_query = ajax_query.replace(" ", "").replace("\n", "")
        web.execute_script(jquery)
        resp = web.execute_script('return ' + ajax_query)
        '''
        web.find_element_by_name('CourseText').send_keys(course_no)
        web.find_element_by_id('SingleAdd').click()
        '''
        print(resp)
        print('OK')
        break


    print(datetime.now())
    print('限制：' + str(restrict) + '人')
    print('目前：' + str(choose_student) + '人')
