# 生成符合ercharts格式的json字符串
import random
import json
province = {'北京': 0, '天津': 0, '上海': 0, '重庆': 0, '河北': 0, '山西': 0, '辽宁': 0, '吉林': 0, '黑龙江': 0,
            '江苏': 0, '浙江': 0, '安徽': 0, '福建': 0, '江西': 0, '山东': 0, '河南': 0, '湖北': 0,
            '湖南': 0, '广东': 0, '海南': 0, '四川': 0, '贵州': 0, '云南': 0, '陕西': 0, '甘肃': 0,
            '青海': 0, '台湾': 0, '内蒙古': 0, '广西': 0, '西藏': 0, '宁夏': 0,
            '新疆': 0, '香港': 0, '澳门': 0}


def randomResultFileName():
    resultFileName = ''
    randomStr = "qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLMKNJBHVHGCFXDSAZ1234569785_"
    for i in range(20):
        resultFileName += randomStr[random.randint(0, len(randomStr) - 1)]
    resultFileName += '.txt'
    return resultFileName

# 分析结果写入json文件


def getProvinceJsonPath(jsonCountOfCity,):
    for i in province:
        stringx = ['{"name":"', i, '","value":', str(province[i]), '},']
        jsonCountOfCity = jsonCountOfCity + ''.join(stringx)
    jsonCountOfCity = jsonCountOfCity[:-1]
    jsonCountOfCity += ']'
    if jsonCountOfCity == ']':
        jsonCountOfCity = '{}'
    resultFileName = randomResultFileName()
    with open('./res/' + resultFileName, 'w', encoding='utf-8', newline='') as resultFile:
        resultFile.write(jsonCountOfCity)
    return resultFileName

# #读取文件
# def getProvinceMap(filePath,para):
#     jsonCountOfCity="["
#     with open(filePath, 'r+', encoding='utf-8', newline='') as csvFile:
#         for line in csvFile:                   # 总读取数
#             line = line.strip('\r\n')   # 删除末尾的无用字符
#             data = line.split(',')      # 按照,分割成元组
#             if data[3] in para.values():
#                 province[data[3]]+=1
#     csvFile.close()
#     return writeProvinceJson(jsonCountOfCity)
#
# def getProvinceMapPCL(filePath,paraP,paraC):
#     jsonCountOfCity="["
#     with open(filePath, 'r+', encoding='utf-8', newline='') as csvFile:
#         for line in csvFile:                   # 总读取数
#             line = line.strip('\r\n')   # 删除末尾的无用字符
#             data = line.split(',')      # 按照,分割成元组
#             if data[3] in paraP.values() and data[4] in paraC.values():
#                 province[data[3]]+=1
#     csvFile.close()
#     return writeProvinceJson(jsonCountOfCity)


def getProvinceMapPCTL(filePath, startDate, endDate, paraP, paraC):
    jsonCountOfCity = "["
    with open(filePath, 'r+', encoding='utf-8', newline='') as csvFile:
        for line in csvFile:                   # 总读取数
            line = line.strip('\r\n')   # 删除末尾的无用字符
            data = line.split(',')      # 按照,分割成元组
            if data[3] in paraP.values() and data[4] in paraC.values() and startDate <= data[1] <= endDate:
                province[data[3]] += 1
    csvFile.close()
    return getProvinceJsonPath(jsonCountOfCity)


def getProvinceMapPTL(filePath, startDate, endDate, para):
    jsonCountOfCity = "["
    with open(filePath, 'r+', encoding='utf-8', newline='') as csvFile:
        for line in csvFile:                   # 总读取数
            line = line.strip('\r\n')   # 删除末尾的无用字符
            data = line.split(',')      # 按照,分割成元组
            if data[3] in para.values() and startDate <= data[1] <= endDate:
                province[data[3]] += 1
    csvFile.close()
    return getProvinceJsonPath(jsonCountOfCity)


def provinceAnalysis(filePath, para):
    the_dict = para
    # # 可   #5地区有时间空分类空
    # if the_dict['地区'] and not the_dict['时间'] and not the_dict['分类']:
    #     return getProvinceMap(filePath,the_dict['地区'])
    # # 可   #6地区有时间空分类有
    # elif the_dict['地区'] and not the_dict['时间'] and the_dict['分类']:
    #     return getProvinceMapPCL(filePath, the_dict['地区'], the_dict['分类'])
    # 可   #7地区有时间有分类有
    if the_dict['地区'] and the_dict['时间'] and the_dict['分类']:
        return getProvinceMapPCTL(filePath, the_dict['时间']['0'], the_dict['时间']['1'], the_dict['地区'], the_dict['分类'])
    # 可   #8地区有时间有分类空
    elif the_dict['地区'] and the_dict['时间'] and not the_dict['分类']:
        return getProvinceMapPTL(filePath, the_dict['时间']['0'], the_dict['时间']['1'], the_dict['地区'])
