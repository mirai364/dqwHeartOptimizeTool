import json
import re
import datetime
import data.status as status
import data.heartData as heartData

## jsonの読み込み
jobJson = open('json\job.json', 'r', encoding='utf-8')
jobList = json.load(jobJson)
jobLevelJson = open('json\jobLevel.json', 'r', encoding='utf-8')
jobLevelList = json.load(jobLevelJson)
heartJson = open('json\heart.json', 'r', encoding='utf-8')
heartList = json.load(heartJson)

filterList = {}
score = 0
scoreTmp = None
count = 0

def getData(jobName, level):
    ## job計算
    job = next((item for item in jobList if item['name'] == jobName), None)
    if job == None:
        return
    ## cost計算
    rank = job.get('rank')
    jobLevel = next((item for item in jobLevelList if item['lv'] == level and item['rank'] == rank), None)

    return (jobLevel.get("cost"),job.get("frame1"),job.get("frame2"),job.get("frame3"),job.get("frame4"))

def initHerat(condition, attributeType, attackType, descendedType):
    global filterList

    ## 条件に従って使用するこころ情報を取得
    for item in filter(lambda heart: heart['condition']==None, heartList):
        heart = heartData.heartData(item, attributeType, attackType, descendedType)
        filterList[heart.id] = heart
    
    if condition == None:
        return

    isSearchHp = condition.startswith('HP') and condition.endswith('以下')
    conditionHpLimit = 0
    if isSearchHp:
        conditionHpLimit = int(re.findall('HP([0-9]+)%以下', condition))

    conditionList = filter(lambda heart: heart['condition']!=None, heartList)
    for conditionData in conditionList:
        isMatch = True
        for con in conditionData['condition'].split("_"):
            if isMatch == False:
                continue

            if isSearchHp and con.startswith('HP') and con.endswith('以下'):
                hpLimit = int(re.findall('HP([0-9]+)%以下', con))
                if (hpLimit < conditionHpLimit):
                    isMatch = False
            elif con != condition:
                isMatch = False
        
        if isMatch:
            tmp = heartData.heartData(conditionData, attributeType, attackType, descendedType)
            filterList[tmp.id] = tmp

def calcRate(frame, color):
    colorList = frame.split('_')
    for frameColor in colorList:
        tmp = int(frameColor)
        if tmp == 0:
            return 1.2
        elif color == 0:
            return 1.2
        elif tmp == color:
            return 1.2
    return 1.0

def loop(cost, heart, frame, status, isUpdate=False):
    global filterList
    global count

    frameKey = heart.id
    if frameKey != '0' and frameKey in status.idList:
        return None
    if status.cost + heart.cost > cost + status.addCost + heart.addCost:
        return None

    tmp = status.add(heart, calcRate(frame, heart.color))
    if isUpdate:
        updateScore(tmp)
        count += 1
    return tmp

def updateScore(status):
    global score
    global scoreTmp
    tmpScore = status.calcScore()
    if tmpScore > score:
        score = tmpScore
        scoreTmp = status

if __name__ == "__main__":
    job = 'バトルマスター'
    level = 43
    targetCost = None
    condition = None
    attributeType = 'ドルマ'
    attackType = 'ブレス'
    descendedType = None

    start = datetime.datetime.now()
    print('start', start)
    initHerat(condition, attributeType, attackType, descendedType)
    cost, frame1, frame2, frame3, frame4 = getData(job, level)
    if targetCost != None:
        cost = targetCost

    heartList = filterList.values()
    ## 1つめ
    for heart1 in heartList:
        tmp1 = loop(cost, heart1, frame1, status.status(attackType))
        if (tmp1 == None):
            continue

        ## 2つめ
        for heart2 in heartList:
            tmp2 = loop(cost, heart2, frame2, tmp1)
            if (tmp2 == None):
                continue

            ## 3つめ
            for heart3 in heartList:
                tmp3 = loop(cost, heart3, frame3, tmp2)
                if (tmp3 == None):
                    continue

                ## 4つめ
                if frame4 != None:
                    for heart4 in heartList:
                        loop(cost, heart4, frame4, tmp3, True)
                else:
                    updateScore(tmp3)
                    count += 1

    print('end', count, datetime.datetime.now() - start)
    scoreTmp.print({})