import numpy as np
from enum import Enum
import math
from scipy import stats as stats


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

        @staticmethod
        def Probability_density_function_theory(x: float | int, expectation: float, variance: float) -> float:
            part1: float = 1 / (np.sqrt(variance) * (np.pi * 2)**(1/2))
            part2: float = np.exp(-0.5 * ((x - expectation) / (np.sqrt(variance)))**2)
            return part1 * part2
        @staticmethod
        def Cumulative_distribution_function_theory(x: float | int, expectation: float, variance: float) -> float:
            body_of_erf: float = (x - expectation) / (np.sqrt(variance) * np.sqrt(2)) 
            erf: float = math.erf(body_of_erf)

            return (1 + erf) / 2
        @staticmethod
        def Cumulative_distribuion_function_emp(x: float | int, sample: list) -> float:
            Sum = 0
            for item in sample:
                    Sum += Heaviside_function(x - item)
            return Sum / len(sample)
        
        @staticmethod
        def Generate_pdf_data(step: float = 0.1, expectation: float | int = 0, variance: float | int = 1) -> tuple[list[float], list[float]]:
            sigma = Round(np.sqrt(variance), 2)
            Breadth = Interval(-4 * sigma, 4 * sigma, mode=Interval.Mode.Include_Both)

            x = []
            y = []

            while(Breadth.a < Breadth.b):
                x.append(Breadth.a)
                y.append(Distributions.Normal_Distribution.Probability_density_function_theory(Breadth.a, expectation=expectation, variance=variance))

                Breadth.a += step
            return x, y
        
        @staticmethod
        def Generate_cdf_data(step: float = 0.1, expectation: float | int = 0, variance: float | int = 1) -> tuple[list[float], list[float]]:
            sigma = Round(np.sqrt(variance), 2)
            Breadth = Interval(-4 * sigma, 4 * sigma, mode=Interval.Mode.Include_Both)

            x = []
            y = []

            while(Breadth.a < Breadth.b):
                x.append(Breadth.a)
                y.append(Distributions.Normal_Distribution.Cumulative_distribution_function_theory(Breadth.a, expectation=expectation, variance=variance))

                Breadth.a += step
            return x, y


@staticmethod
def Round(value: float, decimals:int =2):
    factor = 10 ** decimals
    return round(value * factor) / factor

def Heaviside_function(x: float | int) -> int:
    return 0 if x < 0 else 1 


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

def Get_Nth_Quantile_sample(sample: list, p: float):
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
        t = stats.t.ppf(quantile_level, N-1)

        formule_body = (t  * sample_variance_noShifted**0.5) / N**0.5

        a = sample_mean - formule_body
        b = sample_mean + formule_body

        interval = Interval(a, b, mode=Interval.Mode.Not_Including_Both)

        return interval
    else:
        quantile_level = 1 - (significance_level / 2)

        r = stats.norminvgauss.ppf(quantile_level) 
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

        quantile_level_g1 = significance_level / 2
        quantile_level_g2 = 1 - (significance_level / 2)

        g1 = stats.chi2.ppf(quantile_level_g1, N)
        g2 = stats.chi2.ppf(quantile_level_g2, N)

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

        g1 = stats.chi2.ppf(quantile_level_g1, N-1)
        g2 = stats.chi2.ppf(quantile_level_g2, N-1)

        a = variance_sum / g2
        b = variance_sum / g1

        interval = Interval(a, b, mode=Interval.Mode.Not_Including_Both)
        return interval


def Get_MeanConfidenceIntervalLenght_SignificanceLevel_Relation_Data(sample: list, partition_mean: float, partition_variance_noShifted: float, sign_level_step: float = 0.0001, TL_From: float = 0.9, TL_To: float = 1.0) -> tuple[list[float], list[float]]:
    
    x: list[float] = []
    y: list[float] = []

    current, end = TL_From, TL_To

    while(current < end):

        x.append(current)

        partition_Mean_CI = Get_ConfidenceInterval_of_Mean(sample, (1 - current), partition_mean, partition_variance_noShifted)

        y.append(partition_Mean_CI.get_lenght())

        current += sign_level_step
        current = Round(current, 6)

    return x, y

def Get_VarianceConfidenceIntervalLenght_SignificanceLevel_Relation_Data(sample: list, partition_variance_noShifted) -> tuple[list[float], list[float]]:
    x_variance_confidance_interval_lenghts= []

    y_significance_levels = []

    for significance_level in range(10, 1011):

        significance_level = 1 / significance_level

        y_significance_levels.append(1 - significance_level)

        partition_Variance_CI = Get_ConfidenceInterval_of_Variance(sample, significance_level, partition_variance_noShifted)

        x_variance_confidance_interval_lenghts.append(partition_Variance_CI.get_lenght())

    return x_variance_confidance_interval_lenghts, y_significance_levels
