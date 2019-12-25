# 生成符合ercharts格式的json字符串
import json
import random
allDataCount = {}


def randomResultFileName():
    resultFileName = ''
    randomStr = "qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLMKNJBHVHGCFXDSAZ1234569785_"
    for i in range(20):
        resultFileName += randomStr[random.randint(0, len(randomStr) - 1)]
    resultFileName += '.txt'
    return resultFileName

# 分析结果写入json文件


def getCalendarJsonPath(jsonStr):
    cnt = 0
    cnt2 = 1
    for x, y in allDataCount.items():
        strList = ['{"', str(cnt), '":"', x, '","',
                   str(cnt2), '":"', str(y), '"},']
        jsonStr = jsonStr + ''.join(strList)

    jsonStr = jsonStr[:-1]
    jsonStr += ']'
    if jsonStr == ']':
        jsonStr = '{}'
    resultFileName = randomResultFileName()
    with open('./res/' + resultFileName, 'w', encoding='utf-8', newline='') as resultFile:
        resultFile.write(jsonStr)
    return resultFileName
# 读取文件


def getCalendarFigurePCTL(filePath, startingDay, endDay, paraP, paraC):

    jsonStr = "["
    dateCount = {}  # 记录ip地址是否已统计过
    with open(filePath, encoding='utf-8', newline='') as csvFile:
        for line in csvFile:  # 总读取数
            line = line.strip('\r\n')  # 删除末尾的无用字符
            data = line.split(',')  # 按照,分割成元组
            if startingDay <= data[1] <= endDay and data[3] in paraP.values() and data[4] in paraC.values():
                if (data[1] in dateCount):
                    allDataCount[data[1]] += 1
                else:
                    dateCount[data[1]] = 1
                    allDataCount[data[1]] = 1

        csvFile.close()
    return getCalendarJsonPath(jsonStr)


def getCalendarFigurePTL(filePath, startingDay, endDay, paraP):

    jsonStr = "["
    dateCount = {}  # 记录ip地址是否已统计过
    with open(filePath, encoding='utf-8', newline='') as csvFile:
        for line in csvFile:  # 总读取数
            line = line.strip('\r\n')  # 删除末尾的无用字符
            data = line.split(',')  # 按照,分割成元组
            if startingDay <= data[1] <= endDay and data[3] in paraP.values():
                if (data[1] in dateCount):
                    allDataCount[data[1]] += 1
                else:
                    dateCount[data[1]] = 1
                    allDataCount[data[1]] = 1

        csvFile.close()
    return getCalendarJsonPath(jsonStr)


def CalendarAnalysis(filePath, para):
    the_dict = para
    # 7地区有时间有分类有
    if the_dict['地区'] and the_dict['时间'] and the_dict['分类']:
        return getCalendarFigurePCTL(filePath, the_dict['时间']['0'], the_dict['时间']['1'], the_dict['地区'], the_dict['分类'])
    # 可   #8地区有时间有分类空
    elif the_dict['地区'] and the_dict['时间'] and not the_dict['分类']:
        return getCalendarFigurePTL(filePath, the_dict['时间']['0'], the_dict['时间']['1'], the_dict['地区'])
