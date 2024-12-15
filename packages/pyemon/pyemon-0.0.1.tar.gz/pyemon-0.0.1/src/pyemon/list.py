class ListHelper:
  def __init__(self, list):
    self.List = list

  def len(self):
    return len(self.List)

  def get(self, index, defaultValue = None):
    if index < len(self.List):
      return self.List[index]
    return defaultValue

  def insert(self, index, value):
    self.List.insert(index, value)
    return self

  def unshift(self, value):
    return self.insert(value)

  def shift(self, defaultValue = None):
    if 0 < len(self.List):
      return self.List.pop(0)
    return defaultValue

  def push(self, value):
    self.List.append(value)
    return self

  def pop(self, defaultValue = None):
    if 0 < len(self.List):
      return self.List.pop()
    return defaultValue

  def slice(self, start, stop):
    return self.List[start:stop]

  def __str__(self):
    return str(self.List)
