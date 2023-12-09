# 根据输入“Boss+分数”算总力战用时的插件，输入示例：“寿司12345678”
# 支持用W/w/万跟在数字后表单位，以便查询，输入示例：“寿司1234w”

import re
import datetime


# 从消息匹配分数并返回分数(int)的函数
def tsf_score(msg):
    lmsg = msg.replace('万', 'w').lower()
    # 匹配用万/W/w简写的分数匹配
    if 'w' in lmsg:
        smsg = lmsg.replace('w', '')
        match = re.search(r'-?\d+\.\d*|-?\d+', smsg)
        if match:
            score = float(match.group()) * 10000
            return int(score)
        else:
            return '未匹配到分数'
    # 匹配全数字分数
    else:
        match = re.search(r'\d+', lmsg)
        if match:
            score = int(match.group())
            return score
        else:
            return '未匹配到分数'


# 从消息匹配Boss名称并转换Boss时间类型(str)的函数
def tsf_boss_s(msg):
    bmsg = msg.lower().replace('hod', '霍德').replace('goz', '戈兹')
    match1 = re.search(r'[\u4e00-\u9fa5]{1,5}', bmsg)
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
        mapped_boss = mapping.get(match1.group(), None)
        if mapped_boss == 'ba3' or mapped_boss == 'ba4':
            return mapped_boss
        else:
            return '输入Boss名称有误'
    else:
        return '未匹配到Boss名称'


# 使用Boss时间类型(str)和总力战分数(int)来推算难度指数(int)的函数
def score_level(boss, score):
    if boss == 'ba3':
        # 3分钟Boss
        if score < 623000:
            return '分数低于下限！'
        elif score >= 623000 and score < 911000:
            return 0
        elif score >= 1246000 and score < 1822000:
            return 1
        elif score >= 2492000 and score < 3644000:
            return 2
        elif score >= 4984000 and score < 7288000:
            return 3
        elif score >= 9968000 and score < 14576000:
            return 4
        elif score >= 19936000 and score <= 29152000:
            return 5
        elif score >= 39872000 and score <= 58304000:
            return 6
        elif score > 58304000:
            return '分数高于上限！'
        else:
            return '分数不存在！'
    elif boss == 'ba4':
        # 4分钟Boss
        if score < 575000:
            return '分数低于下限！'
        elif score >= 575000 and score < 959000:
            return 0
        elif score >= 1150000 and score < 1918000:
            return 1
        elif score >= 2300000 and score < 3836000:
            return 2
        elif score >= 4600000 and score < 7672000:
            return 3
        elif score >= 9200000 and score < 15344000:
            return 4
        elif score >= 18400000 and score <= 30688000:
            return 5
        elif score >= 36800000 and score <= 61376000:
            return 6
        elif score > 61376000:
            return '分数高于上限！'
        else:
            return '分数不存在！'
    else:
        return '未知Boss时间类型'


# 使用Boss时间类型(str)、总力战分数(int)、难度指数(int)来计算总力战用时的函数
def score_time(boss, score, level):
    if boss == 'ba3':
        batime3 = (911000 - score * 2 ** (-level)) / 400
        return batime3
    elif boss == 'ba4':
        batime4 = (959000 - score * 2 ** (-level)) / 400
        return batime4
    else:
        return '未知Boss时间类型'


# 输入消息计算总力战用时并提示难度的函数
def bata_time(msg):
    bs = tsf_boss_s(msg)
    sc = tsf_score(msg)
    lv = score_level(bs, sc)

    err_msg = []
    if bs == '输入Boss名称有误' or bs == '未匹配到Boss名称':
        err_msg.append('请检查输入的Boss名称')
    if sc == '未匹配到分数':
        err_msg.append(sc)
    mapped_level = '预定义防报错'
    if lv in [0, 1, 2, 3, 4, 5, 6]:
        mapping = {
            0: 'Normal',
            1: 'Hard',
            2: 'VeryHard',
            3: 'HardCore',
            4: 'Extreme',
            5: 'Insane',
            6: 'Torment',
        }
        mapped_level = mapping.get(lv, '预定义防报错')
    else:
        err_msg.append(lv)
    if err_msg == []:
        tm = int(score_time(bs, sc, lv) * 1000) / 1000
        dt = datetime.datetime.fromtimestamp(tm)
        return mapped_level + '用时' + dt.strftime("%M:%S.%f")[:-3]
    else:
        return '\n'.join(err_msg)
