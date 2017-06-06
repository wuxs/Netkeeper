# coding=utf-8
import sys

import time


def int2byte(n):
    if n <= 255:
        return (n)
    else:
        return (n - 256)


def trans(n):
    if n <= 255:
        return (n)
    else:
        return (n - 256)


# 强转为n个字节
def tran(value, n):
    # m是n位整形就返回m
    if value > -2 ** (n - 1) and value < (2 ** (n - 1) - 1):
        return value
    # 否则,获取m的补码，截取后n字节
    ybin = bin(value)  # m的原码
    binlist = list(ybin)
    # print ybin
    # 只截取后n位，先取反截n位和后取反截n位结果一样
    for i in range(len(binlist)):
        if binlist[i] == '0':
            binlist[i] = '1'
        else:
            binlist[i] = '0'
    fbin = "".join(binlist)  # m的反码

    if value > 0:
        fbin = binlist[len(binlist) - n:]
        fbin = "".join(fbin)
        # print fbin
        if fbin[0] == '0':  # 负数
            return int('-' + fbin, base=2) - 1
        elif fbin[0] == '1':  # 正数
            return int(fbin, base=2)
    else:
        fbin = fbin[3:]
        temp = int('-' + fbin, base=2)  # m反码对应的真值
        temp = temp - 1  # temp的原码就是m的补码
        temp = bin(temp)
        bbin = temp[len(temp) - n:]  # bbin 就是m补码的后n位，求其源码就是所求结果
        f = bbin[:1]  # 符号位
        if bbin[0] == '0':  # 正数
            return int(bbin, base=2)
        else:  # 是负数
            ffbin = list(bbin[1:])
            # 除符号位取反
            for i in range(len(ffbin)):
                if ffbin[i] == '0':
                    ffbin[i] = '1'
                else:
                    ffbin[i] = '0'
            ffbin = ''.join(ffbin)
            temp = int(ffbin, base=2) + 1
            temp = bin(temp)[2:]  # 原码的后31位
            return int('-' + temp, base=2)
    pass


# 将一个大于32字节的整形强转为32为整形
def int32(m):
    # m是32位整形就返回m
    if m > -sys.maxint - 1 and m < sys.maxint:
        return m
    # 否则,获取m的补码，截取后32字节
    ybin = bin(m)  # m的原码
    binlist = list(ybin)
    # print ybin
    # 只截取后32位，先取反截32位和后取反截32位结果一样
    for i in range(len(binlist)):
        if binlist[i] == '0':
            binlist[i] = '1'
        else:
            binlist[i] = '0'
    fbin = "".join(binlist)  # m的反码

    if m > 0:
        fbin = binlist[len(binlist) - 32:]
        fbin = "".join(fbin)
        # print fbin
        if fbin[0] == '0':  # 负数
            return int('-' + fbin, base=2) - 1
        elif fbin[0] == '1':  # 正数
            return int(fbin, base=2)
    else:
        fbin = fbin[3:]
        temp = int('-' + fbin, base=2)  # m反码对应的真值
        temp = temp - 1  # temp的原码就是m的补码
        temp = bin(temp)
        bbin = temp[len(temp) - 32:]  # bbin 就是m补码的后32位，求其源码就是所求结果
        f = bbin[:1]  # 符号位
        if bbin[0] == '0':  # 正数
            return int(bbin, base=2)
        else:  # 是负数
            ffbin = list(bbin[1:])
            # 除符号位取反
            for i in range(len(ffbin)):
                if ffbin[i] == '0':
                    ffbin[i] = '1'
                else:
                    ffbin[i] = '0'
            ffbin = ''.join(ffbin)
            temp = int(ffbin, base=2) + 1
            temp = bin(temp)[2:]  # 原码的后31位
            return int('-' + temp, base=2)


def getMD5():
    pass


def relaccount(u_username):
    RADIUS = 'hubtxinli01'
    now = time.time()
    tt = 1496310522927
    tt /= 1000
    tt *= 0x66666667
    tt >>= 0x20  # 右移32位
    tt >>= 0x01  # 右移1位
    m_time1c = tt  # 第一次加密结果
    m_lasttimec = m_time1c
    tt = m_time1c
    by2 = [0, 0, 0, 0]
    by2[3] = int2byte(tt & 0xff)
    by2[2] = int2byte((tt & 0xff00) / 0x100)
    by2[1] = int2byte((tt & 0xff0000) / 0x10000)
    by2[0] = int2byte((tt & 0xff000000) / 0x1000000)

    # 导致过程，m_time1convert 为结果
    t0 = m_time1c
    t1 = t2 = t3 = int(t0)
    t3 = int32(t3 << 0x10)
    t1 = int32(t1 & 0x0ff00)
    t1 = int32(t1 | t3)
    t3 = t0
    t3 = int32(t3 & 0x0ff0000)
    t2 = int32(t2 >> 0x10)
    t3 = int32(t3 | t2)
    t1 = int32(t1 << 0x08)
    t3 = int32(t3 >> 0x08)
    t1 = int32(t1 | t3)
    m_time1convert = t1  # 对时间操作后的结果，此为格式字串的原始数据

    # 源数据1,对m_time1convert进行计算得到格式符源数据

    tc = m_time1convert
    ss = [0, 0, 0, 0]
    ss[3] = trans(tc & 0xff)
    ss[2] = trans((tc & 0xff00) / 0x100)
    ss[1] = trans((tc & 0xff0000) / 0x10000)
    ss[0] = trans((tc & 0xff000000) / 0x1000000)

    # 格式符初加密

    pp = [0, 0, 0, 0]
    for i in range(0x20):
        j = i / 0x8
        k = 3 - (i % 0x4)
        pp[k] *= 0x2
        if ss[j] % 2 == 1:
            pp[k] += 1
        ss[j] /= 2

    # 格式符计算, m_formatsring为结果

    pf = [0, 0, 0, 0, 0, 0]
    st1 = pp[3]
    st1 /= 0x4
    pf[0] = trans(st1)
    st1 = pp[3]
    st1 = st1 & 0x3
    st1 *= 0x10
    pf[1] = trans(st1)
    st2 = pp[2]
    st2 /= 0x10
    st2 = st2 | st1
    pf[1] = trans(st2)
    st1 = pp[2]
    st1 = st1 & 0x0F
    st1 *= 0x04
    pf[2] = trans(st1)
    st2 = pp[1]
    st2 /= 0x40
    st2 = st2 | st1
    pf[2] = trans(st2)
    st1 = pp[1]
    st1 = st1 & 0x3F
    pf[3] = trans(st1)
    st2 = pp[0]
    st2 /= 0x04
    pf[4] = trans(st2)
    st1 = pp[0]
    st1 = st1 & 0x03
    st1 *= 0x10
    pf[5] = trans(st1)

    for n in range(6):
        pf[n] += 0x20
        if pf[n] >= 0x40:
            pf[n] += 1
    m_formatsring = ''
    for m in range(6):
        m_formatsring += str(pf[m])

    if '@' in u_username:
        strtem = u_username[0:u_username.index('@')]
    else:
        strtem = u_username
    strinput = strtem + RADIUS
    temp = []
    for i in by2:
        temp.append(unichr(i))
    temp.extend(list(strinput))
    import hashlib
    m2 = hashlib.md5()
    ssss = ''.join(temp)
    print unicode(ssss)
    m2.update(ssss)
    m_md5 = m2.hexdigest()
    m_md5use = m_md5[0:2]
    relname = m_formatsring + m_md5use + u_username
    relname = "\r\n" + relname
    return relname


