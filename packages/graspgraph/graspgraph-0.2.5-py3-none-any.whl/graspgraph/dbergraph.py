from .dot import *
from .database import *

class Dbergraph:
  def __init__(self, database = None, colors = None, fontName = "Yu Mincho Demibold"):
    if database is None:
      database = Database()
    if colors is None:
      colors = DotColors()
    self.Database = database
    self.Colors = colors
    self.FontName = fontName

  def to_dot(self):
    return DotFactory.dber(self.Database, self.Colors, self.FontName)
