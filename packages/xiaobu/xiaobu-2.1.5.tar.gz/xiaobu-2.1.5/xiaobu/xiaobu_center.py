# coding=utf-8
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from xiaobu.xiaobu_erp import ErpSession

# 创建数据库连接
engine = create_engine('mysql+pymysql://root:XBJmysql126%40@192.168.1.22:3306/test_center?charset=utf8mb4')
Base = declarative_base()
Session = sessionmaker(bind=engine)
center_session = Session()
erp_session = ErpSession()


class Shop(Base):
    __tablename__ = 'center_shop'

    id = Column(Integer, primary_key=True)
    erp_id = Column(Integer, nullable=False, unique=True)
    shop_name = Column(String(50), nullable=False, unique=True)
    platform = Column(String(10), nullable=False)
    enable = Column(Integer, nullable=False, default=1)
    cookie = Column(Text(500), nullable=True)
    account = Column(String(20), nullable=True)
    password = Column(String(20), nullable=True)
    update_time = Column(DateTime, nullable=True)


# 链接绑定
class TmBinds(Base):
    __tablename__ = 'center_binds'

    user_id = Column(Integer, nullable=False)
    shop_id = Column(Integer, nullable=False)
    baby_id = Column(String(20), nullable=False, unique=True)

    __table_args__ = (
        PrimaryKeyConstraint('baby_id', 'user_id', name='unique_key'),
    )

# 链接绑定记录
class TmBindsLog(Base):
    __tablename__ = 'center_binds_log'

    user_id = Column(Integer, nullable=True)
    shop_id = Column(Integer, nullable=False)
    baby_id = Column(String(20), nullable=False, unique=False)
    date = Column(DateTime, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('baby_id', 'user_id', 'date', name='unique_key'),
    )

Base.metadata.create_all(engine)
