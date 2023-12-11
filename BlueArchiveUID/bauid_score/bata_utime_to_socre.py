# 根据输入“难度+Boss+用x:xx.xxx”算总力战分数的插件，输入示例：“ex寿司用5:23.433”
# 请注意！分钟和秒用冒号分割！秒和毫秒用点分割！
# 支持多个时间计算，支持省略分钟，支持省略毫秒，只需空格+下一个用时，输入示例：“ex寿司用2:23.433 56.789 2:23”


from .bata_rtime_to_score import tsf_kntm, tsf_level, tsf_boss_t


# 使用Boss时间类型(str)、刀数(int)、用时总秒数(float)、难度指数(int)来计算总力战分数的函数
def utime_score(boss, kntm, level):
    utm = kntm[1]
    if boss == 'ba3':
        if utm < 720:
            score = (911000 - utm * 400) * 2**level
            return int(score)
        elif utm >= 720:
            score = 623000 * 2**level
            return int(score)
    elif boss == 'ba4':
        if utm < 960:
            score = (959000 - utm * 400) * 2**level
            return int(score)
        elif utm >= 960:
            score = 575000 * 2**level
            return int(score)
    else:
        return '未知Boss时间类型'


# 输入消息计算总力战分数的函数
def bata_utime_score(msg):
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
        score = utime_score(bs, kt, lv)
        return str(score)
    else:
        return '\n'.join(err_msg)
