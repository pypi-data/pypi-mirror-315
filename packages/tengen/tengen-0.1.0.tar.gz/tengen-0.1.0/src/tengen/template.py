import copy
from pyemon.list import *

class Template:
  __EmptyTemplate = None

  __Templates = {}

  def __init__(self, format = "", name = ""):
    self.Format = format
    self.__Name = name

  @property
  def Name(self):
    return self.__Name

  def to_string(self, args = []):
    if len(args) == 0:
      return self.Format
    return self.Format.format(*args)

  def __str__(self):
    return self.Format

  @classmethod
  def set(cls, template):
    Template.__Templates[template.Name] = template
    return template

  @classmethod
  def get(cls, name):
    if name in Template.__Templates:
      return Template.__Templates[name]
    if Template.__EmptyTemplate is None:
      Template.__EmptyTemplate = Template()
    return Template.__EmptyTemplate

  @classmethod
  def templates(cls):
    return Template.__Templates.values()

  @classmethod
  def render(cls, args):
    newArgs = copy.deepcopy(args)
    return Template.get(List.shift(newArgs)).to_string(newArgs)
