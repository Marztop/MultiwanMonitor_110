import router
import ether
import account
import schedule
import time
import login_ontime

need_monitor = 1

gocloud = router.device(hostname='192.168.1.1', port=22, username='root', password='admin')



wan = ether.port(bind_router=gocloud,soft_name='wan',hardware='eth0.5',bind_account=account.account0)
wan2 = ether.port(bind_router=gocloud,soft_name='wan2',hardware='eth0.4',bind_account=account.account0)
wan3 = ether.port(bind_router=gocloud,soft_name='wan3',hardware='eth0.3',bind_account=account.account1)
wan7 = ether.port(bind_router=gocloud,soft_name='wan7',hardware='apclii0',bind_account=account.account2)

wan_list = [wan,wan2,wan3,wan7]

def monitoring(wan_list):
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    if need_monitor == 1:
        for port in wan_list:
            if port.is_reliable() == False:
                port.login()
    else:
        print('Monitoring is DISABLED')
    print()

def stop_while_router_reset(device):
    device.close()
    global need_monitor
    need_monitor = 0



def start_if_router_boot(device):
    device.connect()
    global need_monitor
    need_monitor = 1


schedule.every(1).minutes.do(monitoring,wan_list)
schedule.every().day.at('05:00').do(login_ontime.main_function_ontime,gocloud,wan_list)
schedule.every().wednesday.at('04:44').do(stop_while_router_reset,gocloud)
schedule.every().wednesday.at('05:44').do(start_if_router_boot,gocloud)
schedule.every().saturday.at('04:44').do(stop_while_router_reset,gocloud)
schedule.every().saturday.at('05:44').do(start_if_router_boot,gocloud)


if __name__ == '__main__':
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(e)