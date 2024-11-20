from CsvHelper import Managers
from dataclasses import dataclass

from MathHelper import MathStatistics

@dataclass
class DataSample:
    value: float
    frequency: int

data = Managers.CsvManager.Scenaries.ReadInType(filepath="test1.csv", OutType=DataSample)

data = [float(x.value) for x in data]

print(MathStatistics.GetExpectedValue(data))


a = MathStatistics.GetVariance_Shifted(data)
b = MathStatistics.GetVariance_NoShifted(data)
