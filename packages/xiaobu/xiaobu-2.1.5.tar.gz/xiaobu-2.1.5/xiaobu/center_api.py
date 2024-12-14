from datetime import datetime

from xiaobu.api.shop import get_shop_list
from xiaobu.xiaobu_center import erp_session, Shop, center_session


def create_shop(shop_name, account, password):
    # 查询erp_shop_id
    shop_list = erp_session.erp_send(get_shop_list(shop_name=shop_name))
    if not shop_list:
        raise Exception('shop not found: %s' % shop_name)
    erp_id = shop_list[0]['shopId']
    platform = shop_list[0]['shopSite']
    shop = Shop(shop_name=shop_name,
                platform=platform,
                erp_id=erp_id,
                account=account,
                password=password,
                update_time=datetime.now())
    center_session.add(shop)
    center_session.commit()


def refresh_cookie(shop_id, cookie):
    shop = center_session.query(Shop).filter(Shop.id == shop_id).first()
    shop.cookie = cookie
    shop.update_time = datetime.now()
    center_session.commit()
