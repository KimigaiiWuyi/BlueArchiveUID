# 根据输入“赛季n 最高n”（可省略汉字，两个名次间保留空格）计算竞技场挖矿剩余青辉石的插件，输入示例：“赛季12 最高3”或“12 3”
# 可省略最高名次，默认历史第一挖完\n 输入示例：“赛季12”或“12”
import re


# 将大于1000的名次格式化处理为'xx01'的函数
def rank_format(rank):
    if rank > 10001:
        rank = 1 + (rank // 1000) * 1000
    elif rank < 10000 and rank > 1001:
        rank = 1 + (rank // 100) * 100
    else:
        pass
    return rank


# 从消息匹配名次并返回名次(list)的函数
def tsf_rank(msg):
    smsg = msg.split()
    # 判断列表长度，=2未省略最高名次
    if len(smsg) == 2:
        match1 = re.search(r'\d+', smsg[0])
        match2 = re.search(r'\d+', smsg[1])
        if match1 is not None and match2 is not None:
            season_rank = match1.group(0)
            season_rank = int(str(season_rank))
            highest_rank = match2.group(0)
            highest_rank = int(str(highest_rank))
            if season_rank > 15001 or highest_rank > 15001:
                return '排名最低为15001请重新输入'
            else:
                rankls = [rank_format(season_rank), rank_format(highest_rank)]
                return rankls
        else:
            return '未匹配到名次'
    # 判断列表长度，=1省略最高名次
    elif len(smsg) == 1:
        match3 = re.search(r'\d+', smsg[0])
        if match3 is not None:
            season_rank = match3.group(0)
            season_rank = int(str(season_rank))
            if season_rank > 15001:
                return '排名最低为15001请重新输入'
            else:
                rankls = [rank_format(season_rank)]
                return rankls
        else:
            return '未匹配到名次'
    else:
        return '请检查指令格式'


# 赛季名次挖矿计算函数
def season_mine(season):
    # 名次大于1000时
    if season > 1000:
        count = 0
        # 8000-15000 为8个档/1000
        while season > 8000:
            season -= 1000
            count += 1
        if season == 8000:
            count += 28
        else:
            # 3500-7000 为8个档/500
            while season > 3500:
                season -= 500
                count += 1
            if season == 3500:
                count += 20
            else:
                # 1100-3000 为20个档/100
                while season > 1100:
                    season -= 100
                    count += 1
        mine = count * 20 + 1770
    # 名次小于等于1000时
    elif season <= 1000 and season > 500:
        mine = season - 501 + 1270
    elif season <= 500 and season > 100:
        mine = (season - 101) * 2 + 470
    elif season <= 100 and season > 10:
        mine = (season - 11) * 3 + 200
    elif season <= 10:
        mine = (season - 1) * 20
    return mine


# 最高名次挖矿计算函数
def highest_mine(highest):
    # 名次大于1000时
    if highest > 1000:
        count = 0
        # 8000-15000 为8个档/1000
        while highest > 8000:
            highest -= 1000
            count += 1
        if highest == 8000:
            count += 28
        else:
            # 3500-7000 为8个档/500
            while highest > 3500:
                highest -= 500
                count += 1
            if highest == 3500:
                count += 20
            else:
                # 1100-3000 为20个档/100
                while highest > 1100:
                    highest -= 100
                    count += 1
        mine = count * 40 + 4220
    # 名次小于等于1000时
    elif highest <= 1000 and highest > 500:
        mine = (highest - 501) * 2 + 1270
    elif highest <= 500 and highest > 100:
        mine = (highest - 101) * 5 + 470
    elif highest <= 100 and highest > 10:
        mine = (highest - 11) * 8 + 200
    elif highest <= 10:
        mine = (highest - 1) * 50
    return mine


# 使用名次(list)来计算竞技场挖矿剩余青辉石的函数
def rank_pyroxene(rankls):
    if len(rankls) == 1:
        rk = rankls[0]
        pyroxene = season_mine(rk)
        return pyroxene
    elif len(rankls) == 2:
        srk = rankls[0]
        hrk = rankls[1]
        pyroxene = season_mine(srk) + highest_mine(hrk)
        return pyroxene
    else:
        return rankls


# 输入消息计算竞技场挖矿剩余青辉石的函数
def bajjc_rank_to_pyroxene(msg):
    rankls = tsf_rank(msg)
    pyroxene = rank_pyroxene(rankls)
    return str(pyroxene)
