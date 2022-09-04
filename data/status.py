import copy

class status():
    def __init__(self, attackType):
        self.attackType = attackType
        self.idList = {}
        self.cost = 0
        self.addCost = 0
        self.hp = 0
        self.mp = 0
        self.power = 0
        self.diffence = 0
        self.attackMp = 0
        self.healMp = 0
        self.speed = 0
        self.dexterity = 0
        self.attribute = 0
        self.attack = 0
        self.descended = 0
    
    def add(self, heart, rate = 1.0):
        tmp = copy.copy(self)
        tmp.cost += heart.cost
        tmp.addCost += heart.addCost
        tmp.attack += heart.attack
        tmp.attribute += heart.attribute
        tmp.descended += heart.descended

        idList = copy.copy(self.idList)
        idList[heart.id] = heart.name
        tmp.idList = idList

        if (rate == 1.2):
            tmp.hp += heart.hp2
            tmp.mp += heart.mp2
            tmp.power += heart.power2
            tmp.diffence += heart.diffence2
            tmp.attackMp += heart.attackMp2
            tmp.healMp += heart.healMp2
            tmp.speed += heart.speed2
            tmp.dexterity += heart.dexterity2
        else:
            tmp.hp += heart.hp
            tmp.mp += heart.mp
            tmp.power += heart.power
            tmp.diffence += heart.diffence
            tmp.attackMp += heart.attackMp
            tmp.healMp += heart.healMp
            tmp.speed += heart.speed
            tmp.dexterity += heart.dexterity
        return tmp

    
    def calcAttack(self):
        if self.attackType == '斬撃' or self.attackType == '体技':
            return self.power
        elif self.attackType == 'じゅもん':
            return self.attackMp
        elif self.attackType == '攻魔複合斬撃' or self.attackType == '攻魔複合体技':
            return self.power + self.attackMp
        elif self.attackType == 'ブレス':
            return self.power + self.dexterity
        elif self.attackType == 'じゅもん回復' or self.attackType == 'とくぎ回復':
            return self.healMp

    def calcScore(self):
        return self.calcAttack() * (1.0 if self.attack == 0.0 else self.attack) * (1.0 if self.attribute == 0.0 else self.attribute) * (1.0 if self.descended == 0.0 else self.descended)

    def print(self, dict):
        dict.update({
            '選択': self.idList,
            'コスト': self.cost,
            '最大HP': self.hp,
            '最大MP': self.mp,
            'ちから': self.power,
            'みのまもり': self.diffence,
            '攻撃魔力': self.attackMp,
            '回復魔力': self.healMp,
            'すばやさ': self.speed,
            'きようさ': self.dexterity,
            #'attackParam': self.calcAttack(),
            #'攻撃倍率': self.attack,
            #'属性ダメージ': self.attribute,
            #'種族ダメージ': self.descended,
            'score': self.calcScore()
            })
        print(dict)