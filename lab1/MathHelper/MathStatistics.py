import numpy as np


def GetVariance_Shifted(sample: list[int| float]):
    SumOfSquareDeviationsFromEx: float = 0

    Ex = GetExpectedValue(sample)
    a2 = Get_NthRow_Moment(sample, 2)
    a1 = Get_NthRow_Moment(sample, 1)

    NoShiftedVariance = a2 - (a1**2)

    return NoShiftedVariance

def GetVariance(sample: list):
    Sum = 0
    avg = GetExpectedValue(sample=sample)
    for x in sample:
        Sum += (x - avg)**2
    return Sum * (1/len(sample))

def GetVariance_NoShifted(sample: list[int| float]):

    ShiftedVariance = GetVariance_Shifted(sample)
    N = len(sample)

    ShiftRatio = N / (N-1)

    return ShiftedVariance * ShiftRatio

def Get_NthRow_Moment(sample: list[float | int], n: int) -> float:
    Sum: float = 0

    N: int = len(sample)

    for x in sample:
        Sum += x**n
    
    return (1/N) * Sum    

def GetExpectedValue(sample: list[float | int]) -> float:
    Sum: float = 0
    for i in sample:
        Sum += i
    return Sum / len(sample)


class Distributions:

    def Distribution_Normal(x: float, expectation: float, variance: float) -> float:
        part1 = 1 / (variance * (np.pi * 2)**(1/2))
        part2 = np.exp(-0.5 * ((x - expectation) / variance)**2)
        return part1 * part2
    

