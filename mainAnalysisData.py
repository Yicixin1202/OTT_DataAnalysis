# 生成符合ercharts格式的json字符串
import json
import random


def randomResultFileName():
    resultFileName = ''
    randomStr = "qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLMKNJBHVHGCFXDSAZ1234569785_"
    for i in range(20):
        resultFileName += randomStr[random.randint(0, len(randomStr) - 1)]
    resultFileName += '.txt'
    return resultFileName
# 分析结果写入json文件


def writePieJson(jsonStr, allDataCount, ipAddressCount):
    string = ['],"电影电视":[', '],"音乐":[', '],"购物":[', '],"游戏":[']
    for x, y in allDataCount.items():
        t = ""
        strList1 = ['{"ipAddress":{"text":"', x,
                    '","total":' + str(ipAddressCount[x]) + '},"业务行为":[']
        t = t + ''.join(strList1)
        cnt = 0
        for q, z in y.items():
            for f, g in z.items():
                strList2 = ['{"name":"', f, '","value":', str(g), '},']
                t = t + ''.join(strList2)
            t = t[:-1]
            t = '%s%s' % (t, string[cnt])
            cnt += 1
            if 4 is cnt:
                cnt = 0
        t = t[:-10]
        t = '%s%s' % (t, ']},')
        jsonStr += t
    jsonStr = jsonStr[:-1]
    jsonStr += ']'
    if jsonStr == ']':
        jsonStr = '{}'
    print(jsonStr)
    resultFileName = randomResultFileName()
    with open('./res/' + resultFileName, 'w', encoding='utf-8', newline='') as resultFile:
        resultFile.write(jsonStr)
    return resultFileName


def getPieChart(filePath, beginDate, endDate, paraP, paraC):
    allDataCount = {}
    ipAddressCount = {}
    jsonStr = "["
    print(paraC)
    with open(filePath, 'r+', encoding='utf-8', newline='') as csvFile:
        for line in csvFile:                   # 总读取数
            line = line.strip('\r\n')   # 删除末尾的无用字符
            data = line.split(',')      # 按照,分割成元组
            if data[4] in paraC.values() and beginDate <= data[1] and data[1] <= endDate and data[3] in paraP.values():
                if data[0] in ipAddressCount:
                    ipAddressCount[data[0]] += 1
                    allDataCount[data[0]]['action'][data[4]] += 1
                    if data[4] == '电影电视':  # 某类目下的细分
                        allDataCount[data[0]]['movieStyle'][data[5]] += 1
                    elif data[4] == '音乐':
                        allDataCount[data[0]]['musicStyle'][data[5]] += 1
                    elif data[4] == '购物':
                        allDataCount[data[0]]['shopStyle'][data[5]] += 1
                    else:
                        allDataCount[data[0]]['gameStyle'][data[5]] += 1
                else:
                    ipAddressCount[data[0]] = 1
                    allDataCount[data[0]] = {'action': {'电影电视': 0, '音乐': 0, '购物': 0, '游戏': 0},
                                             'movieStyle': {'喜剧': 0, '爱情': 0, '动画': 0, '恐怖': 0, '科幻': 0, '动作': 0,
                                                            '战争': 0, '家庭': 0, '古装': 0, '纪录片': 0},
                                             'musicStyle': {'中国特色': 0, '儿童': 0, '动漫ACG': 0, '古典': 0, '嘻哈': 0,
                                                            '摇滚': 0, '民谣': 0, '流行': 0, '电子': 0},
                                             'shopStyle': {'乐器': 0, '女装': 0, '家电数码': 0, '母婴儿童': 0, '珠宝配饰': 0,
                                                           '男装': 0, '美妆': 0, '运动健身': 0, '书籍课程': 0, '游戏动漫': 0,
                                                           '零食生鲜': 0, '明星周边': 0},
                                             'gameStyle': {'休闲益智': 0, '角色扮演': 0, '跑酷竞速': 0, '扑克棋牌': 0, '动作冒险': 0,
                                                           '飞行射击': 0, '经营策略': 0, '体育竞技': 0}}
                    allDataCount[data[0]]['action'][data[4]] += 1
                    if data[4] == '电影电视':  # 某类目下的细分
                        allDataCount[data[0]]['movieStyle'][data[5]] += 1
                    elif data[4] == '音乐':
                        allDataCount[data[0]]['musicStyle'][data[5]] += 1
                    elif data[4] == '购物':
                        allDataCount[data[0]]['shopStyle'][data[5]] += 1
                    else:
                        allDataCount[data[0]]['gameStyle'][data[5]] += 1
    csvFile.close()
    resultFilePath = writePieJson(jsonStr, allDataCount, ipAddressCount)
    return resultFilePath


def analysis(filePath, para):
    the_dict = para
    return getPieChart(filePath, the_dict['时间']['0'], the_dict['时间']['1'], the_dict['地区'],
                       the_dict['分类'])
