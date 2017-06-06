# coding=utf-8
# 导入:
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class NKTime(Base):
    # 表的名字:
    __tablename__ = 'nktime'

    # 表的结构:
    mdate = Column(String(20), nullable=False, primary_key=True)
    starttime = Column(String(20), nullable=False)
    endtime = Column(String(20), nullable=False)
    totaltime = Column(String(20), nullable=False)


