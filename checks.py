import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
import plotly.express as px
from enum import Enum

SZ = 10

class VALPROB(Enum):
    THREE = 0.46
    FOUR = 1.39
    FIVE = 2.78
    SIX = 4.63
    SEVEN = 6.94
    EIGHT = 9.72
    NINE = 11.57
    TEN = 12.50
    ELEVEN = 12.50
    TWELVE = 11.57
    THIRTEEN = 9.72
    FOURTEEN = 6.94
    FIFTEEN = 4.63
    SIXTEEN = 2.78
    SEVENTEEN = 1.39
    EIGHTEEN = 0.46

class CATEGORY(Enum):
    ININFLUENTE = (3,3)
    INCAPACE = (4,5)
    INADATTO = (6,8)
    NORMALE = (9,12)
    PORTATO = (13,15)
    ESPERTO = (16,17)
    ECCEZIONALE = (18, 18)

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
    ININFLUENTE = VALPROB.THREE.value
    INCAPACE = VALPROB.FOUR.value + VALPROB.FIVE.value
    INADATTO = VALPROB.SIX.value + VALPROB.SEVEN.value + VALPROB.EIGHT.value
    NORMALE = VALPROB.NINE.value + VALPROB.TEN.value + VALPROB.ELEVEN.value + VALPROB.TWELVE.value
    PORTATO = VALPROB.THIRTEEN.value + VALPROB.FOURTEEN.value + VALPROB.FIFTEEN.value
    ESPERTO = VALPROB.SIXTEEN.value + VALPROB.SEVENTEEN.value
    ECCEZIONALE = VALPROB.EIGHTEEN.value

print("\nProbabilità di avere una capacità:")
for cat in CATEGORY:
    val = cat.value[0] if cat.value[0] == cat.value[1] else f"da {cat.value[0]} a {cat.value[1]}"
    print(f"\t{cat.name} ({val}) : {getattr(CATPROB, cat.name).value}")

class BASE_SUCCESS_RATIO(Enum):
    # expected success ratio for a normal category
    EASY = 1
    NORMAL = 0.80
    HARD = 0.5
    CHALLENGING = 0

class UP_CATEGORY_WEIGHT(Enum):
    # the more challenging the task, the less helpful becomes the mastery
    # (everyone in middle school learns equations, relativity theory is grasped by few after years of study)
    EASY = 0.3
    NORMAL = 0.2
    HARD = 0.1
    CHALLENGING = 0.1

class DOWN_CATEGORY_WEIGHT(Enum):
    # the more challenging the task, the more harmful becomes the lack of mastery
    # (you can still play football with friends, you cant dance with no training)
    EASY = 0.25
    NORMAL = 0.3
    HARD = 0.4
    CHALLENGING = 0.45


def task_success_ratios(cat):
    multiplier = 0
    current_cat = CATEGORY.NORMALE

    if cat == CATEGORY.NORMALE:
        return BASE_SUCCESS_RATIO

    while current_cat != cat:
        if CATEGORY.is_less(current_cat, cat):
            multiplier += 1
            current_cat = CATEGORY.next(current_cat)
        if CATEGORY.is_more(current_cat, cat):
            multiplier += 1
            current_cat = CATEGORY.previous(current_cat)

    if CATEGORY.is_less(current_cat, CATEGORY.NORMALE):
        success_ratio = {k.name: getattr(BASE_SUCCESS_RATIO, k.name).value - getattr(DOWN_CATEGORY_WEIGHT, k.name).value * multiplier for k in BASE_SUCCESS_RATIO}
        output = Enum(f"{cat.name}_SUCCESS_RATIO", {k:max(min(round(v,2),1), 0) for k,v in success_ratio.items()})
    if CATEGORY.is_more(current_cat, CATEGORY.NORMALE):
        success_ratio = {k.name: getattr(BASE_SUCCESS_RATIO, k.name).value + getattr(UP_CATEGORY_WEIGHT, k.name).value * multiplier for k in BASE_SUCCESS_RATIO}
        tmp = Enum("tmp", {k:max(min(round(v,2),1), 0) for k,v in reversed(success_ratio.items())}.items())
        output = Enum(f"{cat.name}_SUCCESS_RATIO", {k.name:k.value for k in reversed(tmp)})
    return output


print(f"\nProbabilità di successo avendo una capacità:")
for cat in CATEGORY:
    print(f"{cat.name}")
    print(f"task: {[(k.name, k.value) for k in task_success_ratios(cat)]}")

def d4():
    return np.random.randint(1,5, SZ)
def d6():
    return np.random.randint(1,7, SZ)
def d8():
    return np.random.randint(1,9, SZ)
def d10():
    return np.random.randint(1,11, SZ)
def d12():
    return np.random.randint(1,13, SZ)
def d20():
    return np.random.randint(1,21, SZ)

def attribute_roll():
    return d6() + d6() + d6()



def pcs():
    return {
        'STR': attribute_roll(),
        'DEX': attribute_roll(),
        'CON': attribute_roll(),
        'KNO': attribute_roll(),
        'PER': attribute_roll(),
        'CAR': attribute_roll(),
        'ACC': attribute_roll(),
    }

#print(pcs())



