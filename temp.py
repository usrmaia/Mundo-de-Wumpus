class A():
  def __init__(self):
    self.a = "a"

  def mudar(self): self.a = "mudou tambem"

class B():
  def __init__(self):
    self.b = "b"
  
  def mudar(self): self.b = "mudou"

class C():
  def __init__(self):
    self.c = "c"
    self.class_A = A()
    self.class_B = B()
    self.class_A.a = "x"
    self.class_B.b = "y"
    self.class_A.mudar()
    self.class_B.mudar()
    print(self.class_A.a)
    print(self.class_B.b)

c = C()