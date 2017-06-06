# coding=utf-8
# 导入:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from item import Base

# 初始化数据库连接:  3个/是相对路径
engine = create_engine('sqlite:///netkeeper.db')
Base.metadata.create_all(engine)
# 创建DBSession类型:
Session = sessionmaker(bind=engine)
# Sesson实例
session = Session()
