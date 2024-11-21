from CsvHelper import Managers
from dataclasses import dataclass

from MathHelper import MathStatistics

from GraphicsHelper import GraphicsBuilder

import numpy

@dataclass
class DataSample:
    value: float
    frequency: int

data = Managers.CsvManager.Scenaries.ReadInType(filepath="test1.csv", OutType=DataSample)

data = [float(x.value) for x in data]

a1 = MathStatistics.GetExpectedValue(data)

s2 = MathStatistics.GetVariance_Shifted(data) ** 0.5
s20 = MathStatistics.GetVariance_NoShifted(data) ** 0.5

fx = [MathStatistics.Distributions.Distribution_Normal(x, a1, s20) for x in sorted(data)]

GraphicsBuilder.Graphics.BuildLinierFigure(sorted(data), fx, outpath="my_plot.png", label_x="Values", label_y="Probability")
GraphicsBuilder.Graphics.BuildHistogramFigure(data, outpath="hist.png")
GraphicsBuilder.Graphics.Build_Mixed_Hist_Linear_Figure(sorted(data), fx, figure_title="TEST")
