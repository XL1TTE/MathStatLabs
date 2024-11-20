
def GetVariance_Shifted(sample: list[int| float]):
    SumOfSquareDeviationsFromEx: float = 0

    Ex = GetExpectedValue(sample)
    a2 = Get_NthRow_Moment(sample, 2)
    a1 = Get_NthRow_Moment(sample, 1)

    NoShiftedVariance = a2 - (a1**2)

    return NoShiftedVariance

def GetVariance_NoShifted(sample: list[int| float]):

    ShiftedVariance = GetVariance_Shifted(sample)
    N = len(sample)

    ShiftRatio = N / (N-1)

    return ShiftedVariance * ShiftRatio

def Get_NthRow_Moment(sample: list[float | int], n: int) -> float:
    Sum: float = 0

    N: float = len(sample)

    for x in sample:
        Sum += x**n
    
    return (1/N) * Sum    

def GetExpectedValue(sample: list[float | int]) -> float:
    Sum: float = 0
    for i in sample:
        Sum += i
    return Sum / len(sample)

