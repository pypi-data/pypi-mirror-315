from erp_as.apis.user import login
from erp_as.erpRequest import *

from xiaobu.api.wave_check import check_out, package_entries

session_current = Session()


# 获取商品信息
def wave_check_out(lid):
    items = session_current.erp321Send(check_out(lid))
    print(items)


def wave_entries(wave_id, packer_id, action_type):
    package_req = package_entries(wave_id, packer_id, action_type)
    resp = session_current.erp321Send(package_req)
    print(resp)

# 登录
def login_erp(username, pwd):
    session_current.erpSend(login(username=username, password=pwd))


login_erp('17671271393', 'Wh1761393@')
wave_entries(2156664, 18683738, 13)
