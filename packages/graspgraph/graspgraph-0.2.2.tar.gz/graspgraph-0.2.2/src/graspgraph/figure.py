import plotly.graph_objects as pgo
from pyemon.path import *

class FigureTick:
  def __init__(self, dtick = 1, format = "d"):
    self.Dtick = dtick
    self.Format = format

class FigureColors:
  def __init__(self, layoutTitle = "black", xTitle = "black", yTitle = "black", grid = "gray", background = "white", line = "rgb(0, 0, 0)", fill = "rgba(0, 0, 0, 0.15)"):
    self.LayoutTitle = layoutTitle
    self.XTitle = xTitle
    self.YTitle = yTitle
    self.Grid = grid
    self.Background = background
    self.Line = line
    self.Fill = fill

class Figure(pgo.Figure):
  @property
  def LayoutTitleText(self):
    return self.layout.title.text

  @LayoutTitleText.setter
  def LayoutTitleText(self, value):
    self.layout.title.text = value

  @property
  def XTitleText(self):
    return self.layout.xaxis.title.text

  @XTitleText.setter
  def XTitleText(self, value):
    self.layout.xaxis.title.text = value

  @property
  def YTitleText(self):
    return self.layout.yaxis.title.text

  @YTitleText.setter
  def YTitleText(self, value):
    self.layout.yaxis.title.text = value

  def Save(self, filePath, width = 1600, height = 900):
    Path(Path.split(filePath)[0]).makedirs()
    self.write_image(filePath, width = width, height = height)

class FigureFactory:
  @classmethod
  def stats(cls, xValues, yValueGroups, yRange, ticks, colors):
    if len(xValues) <= 0:
      xValues = [0]
      ticks[0].Dtick = 1
    for i in range(3):
      if len(yValueGroups[i]) <= 0:
        yValueGroups[i] = [0]
        ticks[1].Dtick = 1
    figure = Figure(data = [
      pgo.Scatter(showlegend = False, mode = "lines", x = xValues, y = yValueGroups[0], line = dict(color = colors.Line, width = 0)),
      pgo.Scatter(showlegend = False, mode = "lines", x = xValues, y = yValueGroups[1], line = dict(color = colors.Line, width = 5), fillcolor = colors.Fill, fill = "tonexty"),
      pgo.Scatter(showlegend = False, mode = "lines", x = xValues, y = yValueGroups[2], line = dict(color = colors.Line, width = 0), fillcolor = colors.Fill, fill = "tonexty")])
    figure.update_xaxes(zeroline = True, zerolinecolor = colors.Grid, zerolinewidth = 0.5, tickformat = ticks[0].Format, dtick = ticks[0].Dtick, linecolor = colors.Grid, linewidth = 3, gridcolor = colors.Grid, griddash = "dot", mirror = True)
    figure.update_yaxes(zeroline = True, zerolinecolor = colors.Grid, zerolinewidth = 0.5, tickformat = ticks[1].Format, dtick = ticks[1].Dtick, linecolor = colors.Grid, linewidth = 3, gridcolor = colors.Grid, griddash = "dot", mirror = True)
    figure.update_layout(title = dict(text = "", font = dict(color = colors.LayoutTitle, size = 26), x = 0.5),
      xaxis = dict(title = "", color = colors.XTitle, tick0 = xValues[0]),
      yaxis = dict(title = "", color = colors.YTitle, range = yRange),
      font = dict(size = 14),
      paper_bgcolor = colors.Background, plot_bgcolor = colors.Background)
    return figure
