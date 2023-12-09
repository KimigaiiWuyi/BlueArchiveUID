# 根据输入“难度+Boss+剩x:xx.xxx”算总力战分数的插件，输入示例：“ex寿司剩1:23.433”
# 请注意！分钟和秒用冒号分割！秒和毫秒用点分割！
# 支持多刀计算，支持省略分钟，支持省略毫秒，只需空格+下一刀剩余时间，输入示例：“ex寿司剩1:23.433 56.789 1:23”

import re
from datetime import datetime, timedelta


# 从消息匹配难度字母并转换难度指数(int)的函数
def tsf_level(msg):
    l1 = ['n', 'h']
    l2 = ['vh', 'hc', 'ex', 'is', 'in', 'tm']
    # 替换掉hod和goz这俩特别的英文名Boss
    lmsg = msg.lower().replace('hod', '霍德').replace('goz', '戈兹')
    # 匹配开头两个字母
    match1 = re.search(r'^[a-zA-Z]{2}', lmsg)
    if match1:
        matched_level = match1.group()
        # 双字母难度
        if matched_level in l2:
            mapping = {'vh': 2, 'hc': 3, 'ex': 4, 'is': 5, 'in': 5, 'tm': 6}
            mapped_level = mapping.get(matched_level, None)
            return mapped_level
        else:
            return '输入难度有误'
    else:
        match2 = re.search(r'^[a-zA-Z]{1}', lmsg)
        if match2:
            matched_level = match2.group()
            # 单字母难度
            if matched_level in l1:
                mapping = {'n': 0, 'h': 1}
                mapped_level = mapping.get(matched_level, None)
                return mapped_level
            else:
                return '输入难度有误'
        else:
            return '未匹配到难度等级'


# 从消息匹配Boss名称并转换Boss时间类型(str)的函数
def tsf_boss_t(msg):
    bmsg = msg.lower().replace('hod', '霍德').replace('goz', '戈兹')
    match1 = re.search(r'([\u4e00-\u9fa5]{1,5})+[/^剩]', bmsg)
    if match1:
        mapping = {
            '蛇': 'ba3',
            '大蛇': 'ba3',
            '比纳': 'ba3',
            '寿司': 'ba3',
            '寿司人': 'ba3',
            '回转': 'ba3',
            '回转者': 'ba3',
            '黑白': 'ba4',
            '白黑': 'ba4',
            '切赛德': 'ba4',
            '赫赛德': 'ba4',
            '眼球': 'ba4',
            '球': 'ba4',
            '霍德': 'ba4',
            '希罗尼穆斯': 'ba4',
            '主教': 'ba4',
            '佩洛洛斯拉': 'ba4',
            '鸡斯拉': 'ba4',
            '鸡': 'ba4',
            '气垫船': 'ba4',
            '水藻船': 'ba4',
            '若藻船': 'ba4',
            '戈兹': 'ba4',
            '高兹': 'ba4',
            '格里高利': 'ba4',
            '格里高': 'ba4',
            '葛利果': 'ba4',
            '黑影': 'ba4',
            '猫鬼': 'ba4',
            '夜猫': 'ba4',
        }
        mapped_boss = mapping.get(match1.group(1), None)
        if mapped_boss == 'ba3' or mapped_boss == 'ba4':
            return mapped_boss
        else:
            return '输入Boss名称有误'
    else:
        return '未匹配到Boss名称'


# 从消息匹配剩余时间并转换刀数(int)、剩余秒数(float)的函数
def tsf_kntm(msg):
    tmsg = (
        msg.replace('：', ':')
        .replace('；', ':')
        .replace(';', ':')
        .replace('，', '.')
        .replace(',', '.')
        .replace('。', '.')
    )
    match = re.findall(r'\d+\:\d+\.\d+|\d+\.\d+|\d+\:\d+', tmsg)
    if match:
        totalt = 0
        for matched_time in match:
            if ':' in matched_time and '.' in matched_time:
                matched_time = matched_time
            elif ':' in matched_time:
                matched_time = matched_time + ".0"
            elif '.' in matched_time:
                matched_time = "0:" + matched_time
            try:
                time_obj = datetime.strptime(matched_time, "%M:%S.%f")
                time_delta = timedelta(
                    minutes=time_obj.minute,
                    seconds=time_obj.second,
                    microseconds=time_obj.microsecond,
                )
                seconds = time_delta.total_seconds()
                totalt += seconds
            except:
                return '输入时间有误'
        # 返回刀数、剩余总秒数
        return len(match), totalt
    else:
        return '未匹配到剩余时间'


# 使用Boss时间类型(str)、刀数(int)、剩余秒数(float)、难度指数(int)来计算总力战分数的函数
def time_score(boss, kntm, level):
    kn = kntm[0]
    tm = kntm[1]
    if boss == 'ba3':
        if tm <= 720:
            batime3 = kn * 180 - tm
            score3 = (911000 - batime3 * 400) * 2**level
            return int(score3)
        elif tm > 720:
            return '9968000'
    elif boss == 'ba4':
        if tm <= 960:
            batime4 = kn * 240 - tm
            score4 = (959000 - batime4 * 400) * 2**level
            return int(score4)
        elif tm > 960:
            return '9,200,000'
    else:
        return '未知Boss时间类型'


# 输入消息计算总力战分数的函数
def bata_score(msg):
    bs = tsf_boss_t(msg)
    kt = tsf_kntm(msg)
    lv = tsf_level(msg)

    err_msg = []
    if lv == '输入难度有误' or lv == '未匹配到难度等级':
        err_msg.append('请检查输入的难度')
    if bs == '输入Boss名称有误' or bs == '未匹配到Boss名称':
        err_msg.append('请检查输入的Boss名称')
    if kt == '输入时间有误' or kt == '未匹配到剩余时间':
        err_msg.append('请检查输入的剩余时间')
    if err_msg == []:
        score = time_score(bs, kt, lv)
        return str(score)
    else:
        return '\n'.join(err_msg)
