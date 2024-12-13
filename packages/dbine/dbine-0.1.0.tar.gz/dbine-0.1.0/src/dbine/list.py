class ListHelper:
  def __init__(self, list):
    self.List = list

  def len(self):
    return len(self.List)

  def get(self, index, defaultValue = None):
    if index < len(self.List):
      return self.List[index]
    return defaultValue

  def shift(self, defaultValue = None):
    if 0 < len(self.List):
      return self.List.pop(0)
    return defaultValue

  def pop(self, defaultValue = None):
    if 0 < len(self.List):
      return self.List.pop()
    return defaultValue

  def __str__(self):
    return str(self.List)
