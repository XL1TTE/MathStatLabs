import numpy as np
import math
from enum import Enum


class Interval:
    
    class Mode(Enum):
        Include_Left: int = 0
        Include_Right: int = 1
        Include_Both: int = 2
        Not_Including_Both: int = 3
    
    def __init__(self, a: int | float, b: int | float, mode: Mode):
        self.a = a
        self.b = b
        self.mode = mode
    a: float | int
    b: float | int
    mode: Mode

    def is_within_interval(self, x: int | float) -> bool:
        match(self.mode):
            case Interval.Mode.Include_Left:
                return x < self.b and x >= self.a
            case Interval.Mode.Include_Right:
                return x <= self.b and x > self.a
            case Interval.Mode.Include_Both:
                return x <= self.b and x >= self.a
            case Interval.Mode.Not_Including_Both:
                return x < self.b and x > self.a

    def get_lenght(self) -> float:
        return self.b - self.a

class Distributions:

    class Normal_Distribution:

        def Probability_density_function(x: float | int, expectation: float, variance: float) -> float:
            part1 = 1 / (variance**0.5 * (np.pi * 2)**(1/2))
            part2 = np.exp(-0.5 * ((x - expectation) / variance**0.5)**2)
            return part1 * part2
        
        def Cumulative_distribution_function(x: float | int, expectation: float, variance: float, deapth: int = 100) -> float:
            body_of_erf = (x - expectation) / (variance**0.5 * np.sqrt(2)) 
            erf = find_erf(body_of_erf, deapth)

            return (1 + erf) / 2
    

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

def Get_ConfidenceInterval_of_Mean(sample: list[int | float], significance_level: float, sample_mean: float, sample_variance_noShifted: float,  theory_variance: float = None) -> Interval:
    
    interval: Interval

    if(theory_variance == None):

        N = len(sample)
        standart_t = np.random.standard_t(N-1, 1000)

        quantile_level = 1 - (significance_level / 2)
        t = Get_Nth_Quantile(standart_t, quantile_level)

        formule_body = (t  * sample_variance_noShifted**0.5) / N**0.5

        a = sample_mean - formule_body
        b = sample_mean + formule_body

        interval = Interval(a, b, mode=Interval.Mode.Not_Including_Both)

        return interval
    else:
        standart_normal = np.random.normal(0, 1, 1000)

        quantile_level = 1 - (significance_level / 2)

        r = Get_Nth_Quantile(standart_normal, quantile_level) 
        N = len(sample)

        formule_body =  (r * theory_variance**0.5) / N**0.5

        a = sample_mean - formule_body
        b = sample_mean + formule_body

        interval = Interval(a, b, mode=Interval.Mode.Not_Including_Both)

        return interval

def Get_ConfidenceInterval_of_Variance(sample: list[int | float], significance_level: float, sample_variance_noShifted: float, theory_mean: float = None) -> Interval:
    
    interval: Interval
    
    if(theory_mean == None):
        N = len(sample)
        chi_square = np.random.chisquare(N-1, 1000)

        quantile_level_g1 = significance_level / 2
        quantile_level_g2 = 1 - (significance_level / 2)

        g1 = Get_Nth_Quantile(sample=chi_square, p=quantile_level_g1)
        g2 = Get_Nth_Quantile(sample=chi_square, p=quantile_level_g2)

        formule_body = ((N-1) * sample_variance_noShifted)

        a = formule_body / g2
        b = formule_body / g1

        interval = Interval(a, b, mode=Interval.Mode.Not_Including_Both)
        return interval

    else:
        N = len(sample)
        chi_square = np.random.chisquare(N, 1000)

        variance_sum = 0
        for i in range(0, N):
            variance_sum += (sample[i] - theory_mean)**2

        quantile_level_g1 = significance_level / 2
        quantile_level_g2 = 1 - (significance_level / 2)

        g1 = Get_Nth_Quantile(sample=chi_square, p=quantile_level_g1)
        g2 = Get_Nth_Quantile(sample=chi_square, p=quantile_level_g2)

        a = variance_sum / g2
        b = variance_sum / g1

        interval = Interval(a, b, mode=Interval.Mode.Not_Including_Both)
        return interval


def Get_MeanConfidenceIntervalLenght_SignificanceLevel_Relation_Data(sample: list, partition_mean: float, partition_variance_noShifted) -> tuple[list[float], list[float]]:
    x_mean_confidance_interval_lenghts= []

    y_significance_levels = []

    for significance_level in range(10, 1011, 1):

        significance_level = 1 / significance_level

        y_significance_levels.append(1 - significance_level)

        partition_Mean_CI = Get_ConfidenceInterval_of_Mean(sample, significance_level, partition_mean, partition_variance_noShifted)

        x_mean_confidance_interval_lenghts.append(partition_Mean_CI.get_lenght())

    return x_mean_confidance_interval_lenghts, y_significance_levels

def Get_VarianceConfidenceIntervalLenght_SignificanceLevel_Relation_Data(sample: list, partition_variance_noShifted) -> tuple[list[float], list[float]]:
    x_variance_confidance_interval_lenghts= []

    y_significance_levels = []

    for significance_level in range(10, 1011):

        significance_level = 1 / significance_level

        y_significance_levels.append(1 - significance_level)

        partition_Variance_CI = Get_ConfidenceInterval_of_Variance(sample, significance_level, partition_variance_noShifted)

        x_variance_confidance_interval_lenghts.append(partition_Variance_CI.get_lenght())

    return x_variance_confidance_interval_lenghts, y_significance_levels
