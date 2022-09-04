import math
import data.Color as Color

class heartData():
    def __init__(self, data, attributeType, attackType, descendedType):
        self.id = data.get('id')
        self.name = data.get('名前')
        self.cost = data.get('コスト')
        self.addCost = data.get('最大コスト')
        color = data.get('色')
        if color == Color.Color(0).name:
            self.color = 0
        elif color == Color.Color(1).name:
            self.color = 1
        elif color == Color.Color(2).name:
            self.color = 2
        elif color == Color.Color(3).name:
            self.color = 3
        elif color == Color.Color(4).name:
            self.color = 4
        elif color == Color.Color(5).name:
            self.color = 5

        ## 1.0倍データ
        self.hp = data.get('最大HP')
        self.mp = data.get('最大MP')
        self.power = data.get('ちから')
        self.diffence = data.get('みのまもり')
        self.attackMp = data.get('攻撃魔力')
        self.healMp = data.get('回復魔力')
        self.speed = data.get('すばやさ')
        self.dexterity = data.get('きようさ')

        ## 1.2倍データ
        self.hp2 = math.ceil(data.get('最大HP') * 1.2)
        self.mp2 = math.ceil(data.get('最大MP') * 1.2)
        self.power2 = math.ceil(data.get('ちから') * 1.2)
        self.diffence2 = math.ceil(data.get('みのまもり') * 1.2)
        self.attackMp2 = math.ceil(data.get('攻撃魔力') * 1.2)
        self.healMp2 = math.ceil(data.get('回復魔力') * 1.2)
        self.speed2 = math.ceil(data.get('すばやさ') * 1.2)
        self.dexterity2 = math.ceil(data.get('きようさ') * 1.2)

        # ダメージ倍率計算
        if attackType == '斬撃' or attackType == '攻魔複合斬撃':
            self.attack = data.get('斬撃ダメージ')
            getter = attributeType + "属性斬撃ダメージ"
            self.attribute = data.get(getter)
        elif attackType == '体技' or attackType == '攻魔複合体技':
            self.attack = data.get('体技ダメージ')
            getter = attributeType + "属性体技ダメージ"
            self.attribute = data.get(getter)
        elif attackType == 'じゅもん':
            self.attack = data.get('じゅもんダメージ')
            getter = attributeType + "属性じゅもんダメージ"
            self.attribute = data.get(getter)
        elif attackType == 'ブレス':
            self.attack = data.get('ブレスダメージ')
            getter = attributeType + "属性ブレスダメージ"
            self.attribute = data.get(getter)
        elif attackType == 'じゅもん回復':
            self.attack = 0
            self.attribute = data.get("じゅもんHP回復効果")
        elif attackType == 'とくぎ回復':
            self.attack = 0
            self.attribute = data.get("とくぎHP回復効果")

        # 種族ダメージ倍率計算
        self.descended = 0
        if descendedType != None:
            getter = descendedType + "系ダメージ"
            self.descended = data.get(getter)