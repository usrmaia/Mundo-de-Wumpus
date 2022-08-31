from pysat.solvers import Glucose3 #!pip install python-sat

class Solver():
  def __init__(self, linhas, colunas, bd):
    self.glucose = Glucose3()
    self.linhas = linhas
    self.colunas = colunas
    self.bd = bd
    self.mapeamento = {}
    self.mapeamento_reverso = {}
    self.index = 1
    self.atomo = ""
    self.atomo_cima = ""
    self.atomo_esquerda = ""
    self.atomo_direita = ""
    self.atomo_baixo = ""
    self.mapear(self)
    self.regrasDoMapa(self)
  
  def perguntarRegra(self, regra):
    # Verdade caso não aja conflito ou por facuidade
    try: regra = self.mapeamento[regra]
    except: 
      self.mapeamento[f"{regra}"] = self.index
      self.mapeamento[f"- {regra}"] = -self.index
      self.mapeamento_reverso[self.index] = f"{regra}"
      self.mapeamento_reverso[-self.index] = f"- {regra}"

      self.index += 1
      regra = self.mapeamento[regra]

    if self.glucose.solve(assumptions=[regra]): 
      return True
    return False

  def adicionarRegra(self, regra):
    self.mapeamento[f"{regra}"] = self.index
    self.mapeamento[f"- {regra}"] = -self.index
    self.mapeamento_reverso[self.index] = f"{regra}"
    self.mapeamento_reverso[-self.index] = f"- {regra}"
    self.index += 1

    self.atomo = self.mapeamento[f"{regra}"]
    self.eVerdade(self)

  def naoPossuiFedor(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_fedor"]
    self.eFalso(self)

    self.naoPossui(self, linha, coluna, "wumpus")
    
  def naoPossuiBrisa(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_brisa"]
    self.eFalso(self)

    self.naoPossui(self, linha, coluna, "poco")
    
  def possui1Fedor(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_fedor"]
    self.eVerdade(self)

    self.possui1Verdadeiro(self, linha, coluna, "wumpus")

  def possui1Brisa(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_brisa"]
    self.eVerdade(self)

    self.possui1Verdadeiro(self, linha, coluna, "poco")
     
  def possui2Fedor(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_fedor"]
    self.eVerdade(self)

    self.possui2Verdadeiro(self, linha, coluna, "wumpus")

  def possui2Brisa(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_brisa"]
    self.eVerdade(self)

    self.possui2Verdadeiro(self, linha, coluna, "poco")

  def possui3Fedor(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_fedor"]
    self.eVerdade(self)

    self.possui3Verdadeiro(self, linha, coluna, "wumpus")

  def possui3Brisa(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_brisa"]
    self.eVerdade(self)
    
    self.possui3Verdadeiro(self, linha, coluna, "poco")

  def naoPossuiBrilho(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_brilho"]
    self.eFalso(self)

    self.atomo = self.mapeamento[f"{linha}_{coluna}_ouro"]
    self.eFalso(self)
  
  def possuiBrilho(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_brilho"]
    self.eVerdade(self)

    self.atomo = self.mapeamento[f"{linha}_{coluna}_ouro"]
    self.eVerdade(self)
  
  def naoPossuiImpacto(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_impacto"]
    self.eFalso(self)
    
    self.naoPossui(self, linha, coluna, "parede")

  def possui1Impacto(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_impacto"]
    self.eVerdade(self)

    self.possui1Verdadeiro(self, linha, coluna, "parede")

    self.impactosAdjacentesVertical(self, linha, coluna)

    self.impactosAdjacentesHorizontal(self, linha, coluna)

  def possui2Impacto(self, linha, coluna):
    self.atomo = self.mapeamento[f"{linha}_{coluna}_impacto"]
    self.eVerdade(self)

    self.possui2Verdadeiro(self, linha, coluna, "parede")
    
    self.impactosAdjacentesVertical(self, linha, coluna)

    self.impactosAdjacentesHorizontal(self, linha, coluna)

  @staticmethod
  def regrasDoMapa(self):
    for linha in range(0, self.linhas):
      for coluna in range(0, self.colunas):
        atomo1 = self.mapeamento[f"{linha}_{coluna}_wumpus"]
        atomo2 = self.mapeamento[f"{linha}_{coluna}_poco"]
        atomo3 = self.mapeamento[f"{linha}_{coluna}_ouro"]

        self.glucose.add_clause([-atomo1, -atomo2])
        self.glucose.add_clause([-atomo1, -atomo3])
        self.glucose.add_clause([-atomo2, -atomo3])

    for linha in [-1, 0, self.linhas - 1, self.linhas]:
      for coluna in range(-1, self.colunas + 1):
        try: atomo1 = self.mapeamento[f"{linha}_{coluna}_parede"]
        except: 
          self.mapearInstancia(self, linha, coluna, "parede")
          atomo1 = self.mapeamento[f"{linha}_{coluna}_parede"]

        try: atomo2 = self.mapeamento[f"{linha}_{coluna}_impacto"]
        except: 
          self.mapearInstancia(self, linha, coluna, "impacto")
          atomo2 = self.mapeamento[f"{linha}_{coluna}_impacto"]

        self.glucose.add_clause([-atomo1, -atomo2])

    for linha in range(-1, self.linhas):
      for coluna in [-1, 0, self.linhas - 1, self.linhas]:
        try: atomo1 = self.mapeamento[f"{linha}_{coluna}_parede"]
        except: 
          self.mapearInstancia(self, linha, coluna, "parede")
          atomo1 = self.mapeamento[f"{linha}_{coluna}_parede"]

        try: atomo2 = self.mapeamento[f"{linha}_{coluna}_impacto"]
        except: 
          self.mapearInstancia(self, linha, coluna, "impacto")
          atomo2 = self.mapeamento[f"{linha}_{coluna}_impacto"]

        self.glucose.add_clause([-atomo1, -atomo2])
    
    self.glucose.add_clause([self.mapeamento[f"-1_0_parede"]])
    self.glucose.add_clause([self.mapeamento[f"0_-1_parede"]])
  
  @staticmethod
  def mapearInstancia(self, linha, coluna, objeto):
    try: self.mapeamento[f"{linha}_{coluna}_{objeto}"]
    except:
        self.mapeamento[f"{linha}_{coluna}_{objeto}"] = self.index
        self.mapeamento[f"- {linha}_{coluna}_{objeto}"] = -self.index
        self.mapeamento_reverso[self.index] = f"{linha}_{coluna}_{objeto}"
        self.mapeamento_reverso[-self.index] = f"- {linha}_{coluna}_{objeto}"

        self.index += 1

  @staticmethod
  def mapear(self):
    for linha in range(0, self.linhas):
      for coluna in range(0, self.colunas):
        self.mapearInstancia(self, linha, coluna, "wumpus")
        self.mapearInstancia(self, linha, coluna, "poco")
        self.mapearInstancia(self, linha, coluna, "ouro")
        self.mapearInstancia(self, linha, coluna, "fedor")
        self.mapearInstancia(self, linha, coluna, "brisa")
        self.mapearInstancia(self, linha, coluna, "brilho")
        self.mapearInstancia(self, linha, coluna, "impacto")
    
    for linha in [0, self.linhas - 1]:
      for coluna in range(0, self.colunas):
        self.mapearInstancia(self, linha, coluna, "impacto")

    for linha in range(0, self.linhas):
      for coluna in [0, self.colunas - 1]:
        self.mapearInstancia(self, linha, coluna, "impacto")
    
    for linha in [-1, self.linhas]:
      for coluna in range(-1, self.colunas + 1):
        self.mapearInstancia(self, linha, coluna, "parede")

    for linha in range(-1, self.linhas + 1):
      for coluna in [-1, self.colunas]:
        self.mapearInstancia(self, linha, coluna, "parede")

  def imprimirMapeamento(self):
    print("mapeamento[posição] -> index")
    print(self.mapeamento)
    print("mapeamento_reverso[index] -> posição")
    print(self.mapeamento_reverso)
  
  @staticmethod
  def inserirConhecimento(self, conhecimento):
    self.bd.inserirConhecimento(f"{self.mapeamento_reverso[conhecimento]}")

  @staticmethod
  def inserirRaciocinio(self, raciocinio):
    regra = ""
    for atomo in raciocinio:
      regra += f"{self.mapeamento_reverso[atomo]}, "
    regra = regra[0:-2]
    self.bd.inserirRaciocinio(regra)
  
  def resolverSolve(self):
    self.glucose.solve()

  def retornarSolve(self):
    self.glucose.get_model()
  
  def imprimirSolve(self):
    print(self.glucose.get_model())

  # Equivalências Lógicas

  @staticmethod
  def eVerdade(self):
    self.glucose.add_clause([self.atomo])

    self.inserirConhecimento(self, self.atomo)

  @staticmethod
  def eFalso(self):
    self.glucose.add_clause([-self.atomo])

    self.inserirConhecimento(self, -self.atomo)
  
  @staticmethod
  def naoPossui(self, linha, coluna, objeto):
    try: self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_{objeto}"]
    except: 
      self.mapearInstancia(self, linha - 1, coluna, objeto)
      self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_{objeto}"]

    try: self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_{objeto}"]
    except:
      self.mapearInstancia(self, linha, coluna - 1, objeto)
      self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_{objeto}"]

    try: self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_{objeto}"]
    except:
      self.mapearInstancia(self, linha + 1, coluna, objeto)
      self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_{objeto}"]

    try: self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_{objeto}"]
    except:
      self.mapearInstancia(self, linha, coluna + 1, objeto)
      self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_{objeto}"]

    self.glucose.add_clause([-self.atomo_cima])
    self.glucose.add_clause([-self.atomo_esquerda])
    self.glucose.add_clause([-self.atomo_baixo])
    self.glucose.add_clause([-self.atomo_direita])

    self.inserirConhecimento(self, -self.atomo_cima)
    self.inserirConhecimento(self, -self.atomo_esquerda)
    self.inserirConhecimento(self, -self.atomo_baixo)
    self.inserirConhecimento(self, -self.atomo_direita)

  @staticmethod
  def possui1Verdadeiro(self, linha, coluna, objeto):
    try: self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_{objeto}"]
    except: 
      self.mapearInstancia(self, linha - 1, coluna, objeto)
      self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_{objeto}"]

    try: self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_{objeto}"]
    except:
      self.mapearInstancia(self, linha, coluna - 1, objeto)
      self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_{objeto}"]

    try: self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_{objeto}"]
    except:
      self.mapearInstancia(self, linha + 1, coluna, objeto)
      self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_{objeto}"]

    try: self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_{objeto}"]
    except:
      self.mapearInstancia(self, linha, coluna + 1, objeto)
      self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_{objeto}"]

    self.glucose.add_clause([-self.atomo_cima, -self.atomo_esquerda])
    self.glucose.add_clause([-self.atomo_cima, -self.atomo_baixo])
    self.glucose.add_clause([-self.atomo_cima, -self.atomo_direita])
    self.glucose.add_clause([-self.atomo_esquerda, -self.atomo_baixo])
    self.glucose.add_clause([-self.atomo_esquerda, -self.atomo_direita])
    self.glucose.add_clause([-self.atomo_baixo, -self.atomo_direita])

    self.inserirRaciocinio(self, [-self.atomo_cima, -self.atomo_esquerda])
    self.inserirRaciocinio(self, [-self.atomo_cima, -self.atomo_baixo])
    self.inserirRaciocinio(self, [-self.atomo_cima, -self.atomo_direita])
    self.inserirRaciocinio(self, [-self.atomo_esquerda, -self.atomo_baixo])
    self.inserirRaciocinio(self, [-self.atomo_esquerda, -self.atomo_direita])
    self.inserirRaciocinio(self, [-self.atomo_baixo, -self.atomo_direita])
  
  @staticmethod
  def possui2Verdadeiro(self, linha, coluna, objeto):
    try: self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_{objeto}"]
    except: 
      self.mapearInstancia(self, linha - 1, coluna, objeto)
      self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_{objeto}"]

    try: self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_{objeto}"]
    except:
      self.mapearInstancia(self, linha, coluna - 1, objeto)
      self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_{objeto}"]

    try: self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_{objeto}"]
    except:
      self.mapearInstancia(self, linha + 1, coluna, objeto)
      self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_{objeto}"]

    try: self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_{objeto}"]
    except:
      self.mapearInstancia(self, linha, coluna + 1, objeto)
      self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_{objeto}"]

    self.glucose.add_clause([-self.atomo_cima, -self.atomo_esquerda, -self.atomo_baixo])
    self.glucose.add_clause([-self.atomo_cima, -self.atomo_esquerda, -self.atomo_direita])
    self.glucose.add_clause([-self.atomo_cima, -self.atomo_baixo, -self.atomo_direita])
    self.glucose.add_clause([-self.atomo_esquerda, -self.atomo_baixo, -self.atomo_direita])

    self.inserirRaciocinio(self, [-self.atomo_cima, -self.atomo_esquerda, -self.atomo_baixo])
    self.inserirRaciocinio(self, [-self.atomo_cima, -self.atomo_esquerda, -self.atomo_direita])
    self.inserirRaciocinio(self, [-self.atomo_cima, -self.atomo_baixo, -self.atomo_direita])
    self.inserirRaciocinio(self, [-self.atomo_esquerda, -self.atomo_baixo, -self.atomo_direita])

  @staticmethod
  def possui3Verdadeiro(self, linha, coluna, objeto):
    try: self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_{objeto}"]
    except: 
      self.mapearInstancia(self, linha - 1, coluna, objeto)
      self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_{objeto}"]

    try: self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_{objeto}"]
    except:
      self.mapearInstancia(self, linha, coluna - 1, objeto)
      self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_{objeto}"]

    try: self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_{objeto}"]
    except:
      self.mapearInstancia(self, linha + 1, coluna, objeto)
      self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_{objeto}"]

    try: self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_{objeto}"]
    except:
      self.mapearInstancia(self, linha, coluna + 1, objeto)
      self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_{objeto}"]

    self.glucose.add_clause([-self.atomo_cima, -self.atomo_esquerda, -self.atomo_baixo, -self.atomo_direita])
    self.glucose.add_clause([self.atomo_cima, self.atomo_esquerda])
    self.glucose.add_clause([self.atomo_cima, self.atomo_baixo])
    self.glucose.add_clause([self.atomo_cima, self.atomo_direita])
    self.glucose.add_clause([self.atomo_esquerda, self.atomo_baixo])
    self.glucose.add_clause([self.atomo_esquerda, self.atomo_direita])
    self.glucose.add_clause([self.atomo_baixo, self.atomo_direita])

    self.inserirRaciocinio(self, [-self.atomo_cima, -self.atomo_esquerda, -self.atomo_baixo, -self.atomo_direita])
    self.inserirRaciocinio(self, [self.atomo_cima, self.atomo_esquerda])
    self.inserirRaciocinio(self, [self.atomo_cima, self.atomo_baixo])
    self.inserirRaciocinio(self, [self.atomo_cima, self.atomo_direita])
    self.inserirRaciocinio(self, [self.atomo_esquerda, self.atomo_baixo])
    self.inserirRaciocinio(self, [self.atomo_esquerda, self.atomo_direita])
    self.inserirRaciocinio(self, [self.atomo_baixo, self.atomo_direita])
  
  @staticmethod
  def impactosAdjacentesHorizontal(self, linha, coluna):
    # ((p&e)#(p&d))_impacto>((c&-b)#(-c&b))_parede
    try: self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_parede"]
    except: 
      self.mapearInstancia(self, linha - 1, coluna, "parede")
      self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_parede"]

    try: self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_impacto"]
    except:
      self.mapearInstancia(self, linha, coluna - 1, "impacto")
      self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_impacto"]

    try: self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_parede"]
    except:
      self.mapearInstancia(self, linha + 1, coluna, "parede")
      self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_parede"]

    try: self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_impacto"]
    except:
      self.mapearInstancia(self, linha, coluna + 1, "impacto")
      self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_impacto"]

    self.glucose.add_clause([-self.atomo_esquerda, self.atomo_cima, self.atomo_baixo])
    self.glucose.add_clause([-self.atomo_esquerda, -self.atomo_cima, -self.atomo_baixo])
    self.glucose.add_clause([-self.atomo_direita, self.atomo_cima, self.atomo_baixo])
    self.glucose.add_clause([-self.atomo_direita, -self.atomo_cima, -self.atomo_baixo])  

    self.inserirRaciocinio(self, [-self.atomo_esquerda, self.atomo_cima, self.atomo_baixo])
    self.inserirRaciocinio(self, [-self.atomo_esquerda, -self.atomo_cima, -self.atomo_baixo])
    self.inserirRaciocinio(self, [-self.atomo_direita, self.atomo_cima, self.atomo_baixo])
    self.inserirRaciocinio(self, [-self.atomo_direita, -self.atomo_cima, -self.atomo_baixo])
  
  @staticmethod
  def impactosAdjacentesVertical(self, linha, coluna):

    try: self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_impacto"]
    except: 
      self.mapearInstancia(self, linha - 1, coluna, "impacto")
      self.atomo_cima = self.mapeamento[f"{linha - 1}_{coluna}_impacto"]

    try: self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_parede"]
    except:
      self.mapearInstancia(self, linha, coluna - 1, "parede")
      self.atomo_esquerda = self.mapeamento[f"{linha}_{coluna - 1}_parede"]

    try: self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_impacto"]
    except:
      self.mapearInstancia(self, linha + 1, coluna, "impacto")
      self.atomo_baixo = self.mapeamento[f"{linha + 1}_{coluna}_impacto"]

    try: self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_parede"]
    except:
      self.mapearInstancia(self, linha, coluna + 1, "parede")
      self.atomo_direita = self.mapeamento[f"{linha}_{coluna + 1}_parede"]

    self.glucose.add_clause([-self.atomo_cima, self.atomo_esquerda, self.atomo_direita])
    self.glucose.add_clause([-self.atomo_cima, -self.atomo_esquerda, -self.atomo_direita])
    self.glucose.add_clause([-self.atomo_baixo, self.atomo_esquerda, self.atomo_direita])
    self.glucose.add_clause([-self.atomo_baixo, -self.atomo_esquerda, -self.atomo_direita]) 

    self.inserirRaciocinio(self, [-self.atomo_cima, self.atomo_esquerda, self.atomo_direita])
    self.inserirRaciocinio(self, [-self.atomo_cima, -self.atomo_esquerda, -self.atomo_direita])
    self.inserirRaciocinio(self, [-self.atomo_baixo, self.atomo_esquerda, self.atomo_direita])
    self.inserirRaciocinio(self, [-self.atomo_baixo, -self.atomo_esquerda, -self.atomo_direita])   