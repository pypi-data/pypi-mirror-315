from sqlalchemy import create_engine, Column, Integer, String, and_, Date, Numeric, UniqueConstraint, DateTime, Float, \
    Index, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库连接
engine = create_engine('mysql+pymysql://root:XBJmysql126%40@192.168.1.22:3306/test_data?charset=utf8mb4')
Base = declarative_base()
Session = sessionmaker(bind=engine)
data_session = Session()


# 店铺
class TmPromotion(Base):
    __tablename__ = 'data_tm_promotion'

    shop_id = Column(Integer, nullable=False)
    baby_id = Column(String(20), nullable=False)
    charge = Column(Numeric(15, 2), nullable=False)
    pro_type = Column(String(10), nullable=False)
    date = Column(Date, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('baby_id', 'pro_type', 'date', name='unique_key'),
    )


class Order(Base):
    """
    订单
    """
    __tablename__ = 'data_order'

    internal_order_id = Column(Integer, nullable=False, comment="ERP内部订单号，聚水潭生成的订单号")
    internal_sub_order_id = Column(Integer, nullable=True, comment="ERP内部子订单号，最长不超过20")
    baby_id = Column(String(255), nullable=True, comment="宝贝ID")
    count = Column(Integer, nullable=True, comment="销售数量")
    amount = Column(Float, nullable=True, comment="销售金额")
    shop_name = Column(String(255), nullable=True, comment="店铺名称")
    platform = Column(String(10), nullable=True, comment="店铺站点信息")
    pay_date = Column(Date, nullable=True, comment="付款日期")
    is_refund = Column(Integer, nullable=True, comment="是否退款")

    __table_args__ = (
        PrimaryKeyConstraint('internal_order_id', 'internal_sub_order_id', 'is_refund', name='unique_key'),
    )


class Budan(Base):
    """
    订单
    """
    __tablename__ = 'data_budan'

    internal_order_id = Column(Integer, nullable=False, comment="ERP内部订单号，聚水潭生成的订单号")
    sub_order_id = Column(Integer, nullable=False, comment="子订单编号，聚水潭生成的子订单编号")
    baby_id = Column(String(255), nullable=True, comment="宝贝ID")
    count = Column(Integer, nullable=True, comment="补单数量")
    amount = Column(Float, nullable=True, comment="补单金额")
    shop_name = Column(String(255), nullable=True, comment="店铺名称")
    platform = Column(String(10), nullable=True, comment="店铺站点信息")
    pay_date = Column(Date, nullable=True, comment="付款日期")

    __table_args__ = (
        PrimaryKeyConstraint('internal_order_id', 'sub_order_id', name='unique_key'),
    )


class Refund(Base):
    """
    退款单
    """
    __tablename__ = 'data_refund'

    internal_order_id = Column(Integer, nullable=False, comment="ERP内部订单号，聚水潭生成的订单号")
    as_id = Column(Integer, nullable=True, comment="售后单号")
    as_sub_id = Column(Integer, nullable=True, comment="售后子单号")
    baby_id = Column(String(255), nullable=True, comment="宝贝ID")
    origin_order_type = Column(String(255), nullable=True, comment="原订单类型")
    count = Column(Integer, comment="退款数量")
    amount = Column(Float, comment="退款总额")
    shop_name = Column(String(255), nullable=True, comment="店铺名称")
    platform = Column(String(10), nullable=True, comment="店铺站点信息")
    confirm_date = Column(Date, nullable=True, comment="确认日期")

    __table_args__ = (
        PrimaryKeyConstraint('as_id', 'as_sub_id', name='unique_key'),
    )


class TmCTB(Base):
    __tablename__ = 'data_ctb'
    baby_id = Column(String(20), nullable=False, comment='宝贝ID')
    shop_id = Column(Integer, nullable=False, comment='店铺ID')
    amount = Column(Numeric(15, 2), nullable=False, comment='销售金额')
    refund_amount = Column(Numeric(15, 2), nullable=False, comment='退款金额')
    budan_amount = Column(Numeric(15, 2), nullable=False, comment='补单金额')
    budan_order_count = Column(Integer, nullable=False, comment='补单数量')
    date = Column(Date, nullable=False, comment='日期')

    __table_args__ = (
        PrimaryKeyConstraint('baby_id', 'date', name='unique_key'),
    )


class PddPlatform(Base):
    __tablename__ = 'data_pdd_platform'

    shop_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    deal_amount = Column(Numeric(10, 2), nullable=False, comment='成交金额')
    refund_amount = Column(Numeric(10, 2), nullable=False, comment='退款金额')
    qztg = Column(Numeric(10, 2), nullable=False, comment='全站推广')
    bztg = Column(Numeric(10, 2), nullable=False, comment='标准推广')
    sptg = Column(Numeric(10, 2), nullable=False, comment='商品推广')

    __table_args__ = (
        PrimaryKeyConstraint("shop_id", "date", name='unique_key'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class JdPlatform(Base):
    __tablename__ = 'data_jd_platform'

    shop_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    jbkk = Column(Numeric(10, 2), default=0, nullable=False, comment='价保扣款')
    htkc = Column(Numeric(10, 2), default=0, nullable=False, comment='海投快车')
    xedk = Column(Numeric(10, 2), default=0, nullable=False, comment='小额打款')

    __table_args__ = (
        PrimaryKeyConstraint("shop_id", "date", name='unique_key'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
