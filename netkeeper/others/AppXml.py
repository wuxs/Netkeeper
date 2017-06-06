# !/usr/bin/env python
# coding=utf-8
"""
XML操作封装
"""
import os.path
import logging
import xml.etree.ElementTree as ElementTree


class XmlNodeValue(object):
    STRING = 1
    INT = 2
    FLOAT = 3
    BOOL = 4


class XmlNodeMap(object):
    ATTR = 1
    TEXT = 2
    NODE = 3


class XmlNode(object):
    def __init__(self, currentNode=None, rootNode=None):
        self.currentNode = currentNode
        self.rootNode = rootNode

    # 加载XML文件
    def LoadFile(self, path):
        if os.path.isabs(path): path = os.path.abspath(path)
        flag = False
        try:
            self.rootNode = ElementTree.parse(path)
            if self.rootNode is not None: flag = True
            self.currentNode = self.rootNode
        except Exception, e:
            logging.error("XML文件加载失败")
            logging.error(e.__str__())
        return flag

    # 加载XML内容
    def LoadString(self, data):
        if data is None or len(data.strip()) == 0: return False
        flag = False
        try:
            self.rootNode = ElementTree.fromstring(data)
            if self.rootNode is not None: flag = True
            self.currentNode = self.rootNode
        except Exception, e:
            logging.error("XML内容加载失败")
            logging.error(e.__str__())
        return flag

    #  检查数据是否载入正确
    def IsLoad(self):
        return self.currentNode is not None and self.rootNode is not None

    # 返回根节点对象
    def GetRoot(self):
        return XmlNode(self.rootNode, self.rootNode)

    # 查找节点,开始为“/”从根节点开始查找,否则从当前节点查找
    def FindNode(self, path):
        if path is None or len(path.strip()) == 0: return XmlNode(None, self.rootNode)
        path = path.strip()
        node = None
        if path[0] == '/':
            node = self.rootNode.find(path[1:])
        else:
            node = self.currentNode.find(path)
        return XmlNode(node, self.rootNode)

    # 查找多节点
    def FindNodes(self, path):
        if path is None or len(path.strip()) == 0: return XmlNode(None, self.rootNode)
        if path[0] == '/':
            nodes = self.rootNode.findall(path[1:])
        else:
            nodes = self.currentNode.findall(path)
        return [XmlNode(node, self.rootNode) for node in nodes]

    # 获取子节点列表
    def GetChildrens(self, tag=None):
        return [XmlNode(node, self.rootNode) for node in self.currentNode.iter(tag=tag)]

    # 格式化数据
    def GetFormatData(self, node, type):
        if type == XmlNodeValue.STRING:
            v = node.GetStr()
        elif type == XmlNodeValue.INT:
            v = node.GetInt()
        elif type == XmlNodeValue.FLOAT:
            v = node.GetFloat()
        elif type == XmlNodeValue.BOOL:
            v = node.GetBool()
        else:
            v = node.GetData()
        return v

    # 获取子节点内容列表
    # valueFormat 值类型 1 字符串,2 整数,3 小数,4 布尔值
    def GetChildrenList(self, tag=None, valueFormat=XmlNodeValue.STRING):
        data = []
        for node in self.GetChildrens(tag=tag):
            data.append(self.GetFormatData(node, valueFormat))
        return data

    # 获取子节点Map表
    # keyType 1 使用属性值 2 使用子节点
    # keyName   属性值名称或子节点名称
    # valueType 1 使用属性值 2 使用子节点
    # ValueName 属性值名称或子节点名称
    def GetChildrenMap(self, tag=None, keyType=XmlNodeMap.ATTR, keyName="name", valueType=XmlNodeMap.TEXT,
                       valueName=None, valueFormat=XmlNodeValue.STRING):
        data = {}
        for node in self.GetChildrens(tag=tag):
            k, v = None, None
            if keyType == XmlNodeMap.ATTR:
                if keyName is None or len(keyName.strip()) == 0: continue
                k = node.GetAttrs().GetStr(keyName)
            elif keyType == XmlNodeMap.NODE:
                if keyName is None or len(keyName.strip()) == 0: continue
                t = node.FindNode(keyName)
                if not t.IsLoad(): continue
                k = t.GetStr()
            elif keyType == XmlNodeMap.TEXT:
                k = node.GetStr()
            else:
                continue
            if k is None or len(k.strip()) == 0: continue
            if valueType == XmlNodeMap.ATTR:
                if valueName is None or len(valueName.strip()) == 0: continue
                v = self.GetFormatData(node.GetAttrs(), valueFormat)
            elif valueType == XmlNodeMap.NODE:
                if valueName is None or len(valueName.strip()) == 0: continue
                t = node.FindNode(valueName)
                if t.IsLoad():
                    v = self.GetFormatData(t, valueFormat)
            elif valueType == XmlNodeMap.TEXT:
                v = self.GetFormatData(node, valueFormat)
            else:
                v = None
            data[k] = v
        return data

    # 获取节点名称
    def GetTag(self):
        if self.currentNode is None: return ""
        return self.currentNode.tag

    # 获取节点内容
    def GetData(self, default=None):
        if self.currentNode is None: return default
        return self.currentNode.text

    def GetStr(self, default="", strip=True):
        data = self.GetData()
        if data is None: return default
        try:
            data = str(data.encode("utf-8"))
            if data is None:
                data = default
            else:
                if strip:
                    data = data.strip()
        except Exception, e:
            print e
            data = default
        return data

    def GetInt(self, default=0):
        data = self.GetData()
        if data is None: return default
        try:
            data = int(data)
            if data is None: data = default
        except Exception:
            data = default
        return data

    def GetFloat(self, default=0.0):
        data = self.GetData()
        if data is None: return default
        try:
            data = float(data)
            if data is None: data = default
        except Exception:
            data = default
        return data

    def GetBool(self, default=False):
        data = self.GetData()
        if data is None: return default
        data = False
        if self.GetStr().lower() == "true" or self.GetInt() == 1: data = True
        return data

    # 获取节点属性
    def GetAttrs(self, default={}):
        return XmlAttr(self)


class XmlAttr(object):
    def __init__(self, node):
        self.node = node
        self.InitAttrs()

    # 获取Node
    def GetNode(self):
        return self.node

    # 设置Node
    def SetNode(self, node):
        self.node = node
        self.InitAttrs()

    # 初始化Node属性列表
    def InitAttrs(self):
        if self.node is None or self.node.currentNode is None:
            self.attrs = {}
        self.attrs = self.node.currentNode.attrib

    # 获取属性
    def GetAttrs(self):
        if self.attrs is None: self.InitAttrs()
        return self.attrs

    # 获取指定属性
    def GetData(self, key, default=None):
        data = self.attrs.get(key)
        if data is None: data = default
        return data

    def GetStr(self, key, default="", strip=True):
        data = self.GetData(key)
        if data is None: return default
        try:
            data = str(data.encode("utf-8"))
            if data is None:
                data = default
            else:
                if strip:
                    data = data.strip()
        except Exception:
            data = default
        return data

    def GetInt(self, key, default=0):
        data = self.GetData(key)
        if data is None: return default
        try:
            data = int(data)
            if data is None: data = default
        except Exception:
            data = default
        return data

    def GetFloat(self, key, default=0.0):
        data = self.GetData(key)
        if data is None: return default
        try:
            data = float(data)
            if data is None: data = default
        except Exception:
            data = default
        return data

    def GetBool(self, key, default=False):
        data = self.GetData(key)
        if data is None: return default
        data = False
        if self.GetStr(key).lower() == "true" or self.GetInt(key) == 1: data = True
        return data


# 测试
if __name__ == "__main__":
    node = XmlNode()
    print node.LoadFile(r"config.xml")
    print node.FindNode("engine/headers").GetChildrenMap("header", XmlNodeMap.ATTR, "name", XmlNodeMap.TEXT, None,
                                                         XmlNodeValue.STRING)
