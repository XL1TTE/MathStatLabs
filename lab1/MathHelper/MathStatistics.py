import numpy as np
import math

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

def Get_Nth_Quantile(sample: list, p: float):
    ordered_sample = sorted(sample)
    N = len(ordered_sample)

    ordered_sample.append(ordered_sample[-1])

    k = int(p * (N-1))
    if(k + 1 < p * N):
        return ordered_sample[k+1]
    elif(k + 1 > p * N):
        return ordered_sample[k]
    
    return (ordered_sample[k] + ordered_sample[k+1]) / 2
 
def Get_median_value_for_sample(sample: list):
    ordered_sample = sorted(sample)
    N = len(ordered_sample)
    if(N % 2 == 0):
        k = int(N / 2)
        return (ordered_sample[k] + ordered_sample[k-1]) / 2
    else:
        k = int(N / 2)
        return ordered_sample[k]
    

def find_erf(x: float | int, depth: int):
    if(depth <= 5000 and depth >= 0):

        part0 = 2 / np.sqrt(np.pi)

        Sum = 0

        for n in range(0, depth):
            part1 = x / (2*n + 1)

            multiplier = 1
            for i in range(1, n + 1):
                expr = (-1 * x**2) / i
                multiplier *= expr
            Sum += part1 * multiplier

        return Sum * part0
    else:
        raise Exception("Max depth is 5000.")
    
class Distributions:

    class Normal_Distribution:

        def Probability_density_function(x: float | int, expectation: float, variance: float) -> float:
            part1 = 1 / (variance * (np.pi * 2)**(1/2))
            part2 = np.exp(-0.5 * ((x - expectation) / variance)**2)
            return part1 * part2
        
        def Cumulative_distribution_function(x: float | int, expectation: float, variance: float, deapth: int = 100) -> float:
            body_of_erf = (x - expectation) / (variance * np.sqrt(2)) 
            erf = find_erf(body_of_erf, deapth)

            return (1 + erf) / 2
    

