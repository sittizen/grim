import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
import plotly.express as px
from enum import Enum

SZ = 10000

ROLLS = { # roll a lot of dice
    "D4": lambda: np.random.randint(1,5, SZ),
    "D6": lambda: np.random.randint(1,7, SZ),
    "D8": lambda: np.random.randint(1,9, SZ),
    "D10": lambda: np.random.randint(1,11, SZ),
    "D12": lambda: np.random.randint(1,13, SZ),
    "D20": lambda: np.random.randint(1,21, SZ),
}

VALPROB = { # probability to roll every value on 3d6
    3 : 0.0046,
    4 : 0.0139,
    5 : 0.0278,
    6 : 0.0463,
    7 : 0.0694,
    8 : 0.0972,
    9 : 0.1157,
    10 : 0.1250,
    11 : 0.1250,
    12 : 0.1157,
    13 : 0.0972,
    14 : 0.0694,
    15 : 0.0463,
    16 : 0.0278,
    17 : 0.0139,
    18 : 0.0046,

}

class ABILITY_CAT(Enum):
    # we assign a category to every different ability modifier range
    ININFLUENTE = (3,) # -3
    INCAPACE = (4,5) # -2
    INADATTO = (6,7,8) # -1
    NORMALE = (9,10,11,12) # 0
    PORTATO = (13,14,15) # +1
    ESPERTO = (16,17) # +2
    ECCEZIONALE = (18,) # +3

    @classmethod
    def next(cls, cat):
        members = list(cls)
        return members[(members.index(cat) + 1)]
    
    @classmethod
    def previous(cls, cat):
        members = list(cls)
        return members[(members.index(cat) - 1)]
    
    @classmethod
    def is_less(cls, cat1, cat2):
        members = list(cls)
        return members.index(cat1) < members.index(cat2)
    
    @classmethod
    def is_more(cls, cat1, cat2):
        members = list(cls)
        return members.index(cat1) > members.index(cat2)

class CATPROB(Enum):
    # probability to be in each ability class
    ININFLUENTE = VALPROB[3]
    INCAPACE = VALPROB[4] + VALPROB[5]
    INADATTO = VALPROB[6] + VALPROB[7] + VALPROB[8]
    NORMALE = VALPROB[9] + VALPROB[10] + VALPROB[11] + VALPROB[12]
    PORTATO = VALPROB[13] + VALPROB[14] + VALPROB[15]
    ESPERTO = VALPROB[16] + VALPROB[17]
    ECCEZIONALE = VALPROB[18]

class DIFFICULTY(Enum):
    # we define 4 possibile difficulty levels
    EASY = 0
    NORMAL = 1
    HARD = 2
    CHALLENGING = 3

class BASE_SUCCESS_RATIO(Enum):
    # we decide the expected success ratio for someone in the normal category
    EASY = 1
    NORMAL = 0.8
    HARD = 0.5
    CHALLENGING = 0.1

class UP_ABILITY_WEIGHT(Enum):
    # we define the weight of expertise in the success ratio
    # the more challenging the task, the less helpful becomes the mastery
    # (everyone in middle school learns equations, relativity theory is grasped by few after years of study)
    EASY = 0.3
    NORMAL = 0.2
    HARD = 0.1
    CHALLENGING = 0.15

class DOWN_ABILITY_WEIGHT(Enum):
    # we define the weight of incompetence in the success ratio
    # the more challenging the task, the more harmful becomes the lack of mastery
    # (you can still play football with friends, you cant dance with no training)
    EASY = 0.2
    NORMAL = 0.3
    HARD = 0.4
    CHALLENGING = 0.5


def expected_task_success_ratios(cat):
    # expected success ratio for every difficulty level, given a certain ability category
    if cat == ABILITY_CAT.NORMALE:
        return BASE_SUCCESS_RATIO
    
    distance, current_cat = 0, ABILITY_CAT.NORMALE

    while current_cat != cat:
        distance += 1
        if ABILITY_CAT.is_less(current_cat, cat):
            current_cat = ABILITY_CAT.next(current_cat)
        if ABILITY_CAT.is_more(current_cat, cat):
            current_cat = ABILITY_CAT.previous(current_cat)

    if ABILITY_CAT.is_less(current_cat, ABILITY_CAT.NORMALE):
        success_ratio = {k.name: getattr(BASE_SUCCESS_RATIO, k.name).value - getattr(DOWN_ABILITY_WEIGHT, k.name).value * distance for k in BASE_SUCCESS_RATIO}
        return Enum(f"{cat.name}_SUCCESS_RATIO", {k:max(min(round(v,2),1), 0) for k,v in success_ratio.items()})
    if ABILITY_CAT.is_more(current_cat, ABILITY_CAT.NORMALE):
        success_ratio = {k.name: getattr(BASE_SUCCESS_RATIO, k.name).value + getattr(UP_ABILITY_WEIGHT, k.name).value * distance for k in BASE_SUCCESS_RATIO}
        tmp = Enum("tmp", {k:max(min(round(v,2),1), 0) for k,v in reversed(success_ratio.items())}.items())
        return Enum(f"{cat.name}_SUCCESS_RATIO", {k.name:k.value for k in reversed(tmp)})
   
def get_expected_task_success_ratio(cat, diff):
    ratios = expected_task_success_ratios(cat)
    if diff.name in ratios.__dict__:
        return ratios[diff.name].value
    if "EASY" in ratios.__dict__:
        return 0
    return 1

print(f"\nExpected success probabilities:")
for cat in ABILITY_CAT:
    print(f"\tbeing {cat.name} : {[(k.name, get_expected_task_success_ratio(cat, k)) for k in  DIFFICULTY]}")


class BaseDice(Enum):
    # we define the base dice for every ability category
    ININFLUENTE = "D6"
    INCAPACE = "D6"
    INADATTO = "D6"
    NORMALE = "D6"
    PORTATO = "D6"
    ESPERTO = "D6"
    ECCEZIONALE = "D6"

class DiffDice(Enum):
    # we define the difficulty dice for every ability category
    ININFLUENTE = "D4"
    INCAPACE = "D6"
    INADATTO = "D6"
    NORMALE = "D6"
    PORTATO = "D6"
    ESPERTO = "D6"
    ECCEZIONALE = "D6"

def task_roll(cat, diff):
    return ROLLS["D20"]()

def mean_ecdf(cat, diff):
    ecdf = ECDF(task_roll(cat, diff))
    vals = ecdf(cat.value) # probabilities to roll under each val of the category
    _num, _den = 0,0
    # return a single value, the weighted mean of the probabilities to roll under each val of the category
    probs = [VALPROB[ability_val] for ability_val in cat.value]
    for value, weight in zip(vals, probs / np.sum(probs)):  
        _num += value * weight 
        _den += weight
    return _num / _den

oks = 0
for cat in ABILITY_CAT:
    res = []
    for diff in DIFFICULTY:
        task = task_roll(cat, diff)
        expected_ratio = get_expected_task_success_ratio(cat, diff)
        estimated_ratio =  mean_ecdf(cat, diff)
        fitval = round(expected_ratio - estimated_ratio, 2)
        if fitval == 0:
            oks += 1
        res.append((diff.name, round(estimated_ratio,2), fitval if fitval else "Ok"))
    print(f"\t{cat.name} - {res}")
print(f"\n{oks} / {len(ABILITY_CAT) * len(DIFFICULTY)} tests ok")




#def attribute_roll(): # we roll a lot of attribute values
#    return ROLLS["D6"]() + ROLLS["D6"]() + ROLLS["D6"]()


#def pcs():
#    return {
#        'STR': attribute_roll(),
#        'DEX': attribute_roll(),
#        'CON': attribute_roll(),
#        'KNO': attribute_roll(),
#        'PER': attribute_roll(),
#        'CAR': attribute_roll(),
#        'ACC': attribute_roll(),
#    }




