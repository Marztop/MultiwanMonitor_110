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

'''if wan.is_reliable() == False:
    wan.login()'''

wan2.login()