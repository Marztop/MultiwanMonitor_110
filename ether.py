import re
import requests
import ddddocr
import time

ocr_handler = ddddocr.DdddOcr()


class port:
    def __init__(self,bind_router,soft_name,hardware,bind_account):
        self.name = self
        self.soft_name = soft_name
        self.hardware = hardware
        self.bind_account = bind_account
        self.bind_router = bind_router
    


    def ping(self,target,count,timeout):
        return self.bind_router.send_command('ping %s -I %s -c %s -w %s'%(target,self.hardware,count,timeout),prompt_time=timeout+0.5)



    def is_reliable(self):
        result = self.ping(target='www.baidu.com',count='3',timeout=4)
        temp = result.split('--- www.baidu.com ping statistics ---')[1]
        if 'duplicates' in temp:
            packet_loss = eval(temp.split(',')[3].split('packet loss')[0].strip(' ').strip('%'))
        else:
            packet_loss = eval(temp.split(',')[2].split('packet loss')[0].strip(' ').strip('%'))
        print('%s packet loss: %s'%(self.soft_name,packet_loss)+r'%')
        if packet_loss == 0:
            return True
        else:
            return False
    


    def login(self):
        self.bind_router.send_command('''sed -i 6c"        option enabled '1'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 7c"        option index '0'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 8c"        option srcintf 'all'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 9c"        option srcipgrp 'centerm'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 10c"        option dstipgrp 'ALL'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 11c"        option protocol 'all'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 12c"        option loadbalancetype 'addrportlb'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 13c"        option wanintf '%s'" /etc/config/pbr'''%(self.soft_name))
        self.bind_router.send_command('''sed -i 14c"        option forceassign '1'" /etc/config/pbr''')
        self.bind_router.send_command('/etc/init.d/nwan restart')
        time.sleep(5)
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }
        session=requests.Session()

        def get_args(session):
            res = session.get(r'https://u.njtech.edu.cn/cas/login?service=https%3A%2F%2Fu.njtech.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3DOe7wtp9CAMW0FVygUasZ%26response_type%3Dcode%26state%3Dnjtech%26s%3Df682b396da8eb53db80bb072f5745232')
            text = res.text
            lt=re.findall('(?<=name="lt" value=").*',text)[0].split('"')[0]
            execution=re.findall('(?<=name="execution" value=").*',text)[0].split('"')[0]
            url_param = re.findall('(?<=action=").*', text)[0].split('"')[0]
            post_url = 'https://u.njtech.edu.cn'+url_param
            return lt,execution,post_url

        def get_captcha(session):
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
            return result
        
        lt,execution,post_url=get_args(session)
        captcha=get_captcha(session)
        params = {
            'username': self.bind_account['username'],
            'password': self.bind_account['password'],
            'captcha': captcha,
            'channelshow': '中国移动',
            'channel': '@cmcc',
            'lt': lt,
            'execution': execution,
            '_eventId': 'submit',
            'login': '登录'
        }
        login_response = session.post(url=r'https://u.njtech.edu.cn/cas/login?service=https%3A%2F%2Fu.njtech.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3DOe7wtp9CAMW0FVygUasZ%26response_type%3Dcode%26state%3Dnjtech%26s%3Df682b396da8eb53db80bb072f5745232', params=params, headers=headers)
        session.close()
        self.bind_router.send_command('''sed -i 6c"        option enabled '0'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 7c"        option index '0'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 8c"        option srcintf 'all'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 9c"        option srcipgrp 'centerm'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 10c"        option dstipgrp 'ALL'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 11c"        option protocol 'all'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 12c"        option loadbalancetype 'addrportlb'" /etc/config/pbr''')
        self.bind_router.send_command('''sed -i 13c"        option wanintf '%s'" /etc/config/pbr'''%(self.soft_name))
        self.bind_router.send_command('''sed -i 14c"        option forceassign '1'" /etc/config/pbr''')
        self.bind_router.send_command('/etc/init.d/nwan restart')
        time.sleep(5)
        return 0