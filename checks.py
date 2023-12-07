import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
import plotly.express as px
from enum import Enum

SZ = 10000

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

class ABILITY(Enum):
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

print("\nProbabilità di avere un'abilità:")
for cat in ABILITY:
    val = cat.value[0] if cat.value[0] == cat.value[1] else f"da {cat.value[0]} a {cat.value[1]}"
    print(f"\t{cat.name} ({val}) : {getattr(CATPROB, cat.name).value}")

class DIFFICULTY(Enum):
    EASY = 0
    NORMAL = 1
    HARD = 2
    CHALLENGING = 3

class BASE_SUCCESS_RATIO(Enum):
    # expected success ratio for a normal ABILITY
    EASY = 1
    NORMAL = 0.80
    HARD = 0.5
    CHALLENGING = 0

class UP_ABILITY_WEIGHT(Enum):
    # the more challenging the task, the less helpful becomes the mastery
    # (everyone in middle school learns equations, relativity theory is grasped by few after years of study)
    EASY = 0.3
    NORMAL = 0.2
    HARD = 0.1
    CHALLENGING = 0.1

class DOWN_ABILITY_WEIGHT(Enum):
    # the more challenging the task, the more harmful becomes the lack of mastery
    # (you can still play football with friends, you cant dance with no training)
    EASY = 0.25
    NORMAL = 0.3
    HARD = 0.4
    CHALLENGING = 0.45


def expected_task_success_ratios(cat):
    multiplier = 0
    current_cat = ABILITY.NORMALE

    if cat == ABILITY.NORMALE:
        return BASE_SUCCESS_RATIO

    while current_cat != cat:
        if ABILITY.is_less(current_cat, cat):
            multiplier += 1
            current_cat = ABILITY.next(current_cat)
        if ABILITY.is_more(current_cat, cat):
            multiplier += 1
            current_cat = ABILITY.previous(current_cat)

    if ABILITY.is_less(current_cat, ABILITY.NORMALE):
        success_ratio = {k.name: getattr(BASE_SUCCESS_RATIO, k.name).value - getattr(DOWN_ABILITY_WEIGHT, k.name).value * multiplier for k in BASE_SUCCESS_RATIO}
        output = Enum(f"{cat.name}_SUCCESS_RATIO", {k:max(min(round(v,2),1), 0) for k,v in success_ratio.items()})
    if ABILITY.is_more(current_cat, ABILITY.NORMALE):
        success_ratio = {k.name: getattr(BASE_SUCCESS_RATIO, k.name).value + getattr(UP_ABILITY_WEIGHT, k.name).value * multiplier for k in BASE_SUCCESS_RATIO}
        tmp = Enum("tmp", {k:max(min(round(v,2),1), 0) for k,v in reversed(success_ratio.items())}.items())
        output = Enum(f"{cat.name}_SUCCESS_RATIO", {k.name:k.value for k in reversed(tmp)})
    return output


print(f"\nProbabilità attese di successo avendo una capacità:")
for cat in ABILITY:
    print(f"{cat.name}")
    print(f"task: {[(k.name, k.value) for k in expected_task_success_ratios(cat)]}")

ROLLS = {
    "D4": lambda: np.random.randint(1,5, SZ),
    "D6": lambda: np.random.randint(1,7, SZ),
    "D8": lambda: np.random.randint(1,9, SZ),
    "D10": lambda: np.random.randint(1,11, SZ),
    "D12": lambda: np.random.randint(1,13, SZ),
    "D20": lambda: np.random.randint(1,21, SZ),
}

def attribute_roll():
    return ROLLS["D6"]() + ROLLS["D6"]() + ROLLS["D6"]()

print(attribute_roll())
print(attribute_roll())
print(attribute_roll())

def task_roll(base_dice, diff_dice, diff):
    diff_roll = [0, ] * SZ
    for i in range(diff.value):
        diff_roll += ROLLS[diff_dice]()
    return ROLLS[base_dice]() + ROLLS[base_dice]() + diff_roll

def mean_ecdf(base_dice, diff_dice, diff, ability):
    task = task_roll(base_dice, diff_dice, diff)
    ecdf = ECDF(task)
    # probabilities of success for the lower and upper bounds of the ability class
    low, high = ecdf(ability.value)
    return (low+high) / 2


def get_expected_task_success_ratio(ab, diff):
    ratios = expected_task_success_ratios(ab)
    if diff.name in ratios.__dict__:
        return ratios[diff.name].value
    return 0.0

for base_dice in ("D8", ):
    for diff_dice in ("D4", "D6",):
        print(f"\nProbabilità stimata con base {base_dice} e difficulty {diff_dice}")
        for ab in ABILITY:
            for diff in DIFFICULTY:
                task = task_roll(base_dice, diff_dice, diff)
                expected_ratio = get_expected_task_success_ratio(ab,diff)
                estimated_ratio =  mean_ecdf(base_dice, diff_dice, diff, ab)
                print(f"\t{ab.name} - {diff.name} : {estimated_ratio} (expected: {expected_ratio})")

                






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




