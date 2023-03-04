import requests
import ddddocr
import re
import time

ocr_handler = ddddocr.DdddOcr()


def login(port):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
    }
    session=requests.Session()


    #get_args
    res = session.get(r'https://u.njtech.edu.cn/cas/login?service=https%3A%2F%2Fu.njtech.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3DOe7wtp9CAMW0FVygUasZ%26response_type%3Dcode%26state%3Dnjtech%26s%3Df682b396da8eb53db80bb072f5745232')
    text = res.text
    lt=re.findall('(?<=name="lt" value=").*',text)[0].split('"')[0]
    execution=re.findall('(?<=name="execution" value=").*',text)[0].split('"')[0]
    url_param = re.findall('(?<=action=").*', text)[0].split('"')[0]
    post_url = 'https://u.njtech.edu.cn'+url_param


    #get_captcha
    from http import client
    client.HTTPConnection._http_vsn=10
    client.HTTPConnection._http_vsn_str='HTTP/1.0'
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'u.njtech.edu.cn'
    }
    res = session.get('https://u.njtech.edu.cn/cas/captcha.jpg',headers=headers)
    result=ocr_handler.classification(res.content)


    #login
    params = {
        'username': port.bind_account['username'],
        'password': port.bind_account['password'],
        'captcha': result,
        'channelshow': '中国移动',
        'channel': '@cmcc',
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
        'login': '登录'
    }
    login_response = session.post(url=r'https://u.njtech.edu.cn/cas/login?service=https%3A%2F%2Fu.njtech.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3DOe7wtp9CAMW0FVygUasZ%26response_type%3Dcode%26state%3Dnjtech%26s%3Df682b396da8eb53db80bb072f5745232', params=params, headers=headers)
    session.close()
    return 0


def main_function_ontime(device,wan_list):
    for port in wan_list:
        device.send_command('/sbin/ifdown %s'%(port.soft_name))

    time.sleep(600)

    for index in len(wan_list):
        if index == 0:
            device.send_command('/sbin/ifup %s'%(wan_list[index].soft_name))
            time.sleep(10)
            login(wan_list[index])
        else:
            device.send_command('/sbin/ifup %s'%(wan_list[index].soft_name))
            device.send_command('/sbin/ifdown %s'%(wan_list[index-1].soft_name))
            time.sleep(10)
            login(wan_list[index])


    for port in wan_list:
        device.send_command('/sbin/ifup %s'%(port.soft_name))
