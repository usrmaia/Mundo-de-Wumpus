class Atuador():
  def __init__(self, BD, Pilha, InfoDoAgente, ):
    self.bd = BD
    self.p = Pilha # Busca em profundidade
    self.desempenho = desempenho
    self.orientacao = orientacao

  def Atuar(self, acao):
    if acao == "saindo_da_caverna":
      if self.sairDaCaverna(self): 
        print("saiu da caverna")
        self.status_agente = "fim"
        self.bd.inserirAcao("sair_da_caverna")
      else: 
        self.caminharParaSaida(self)      
    elif acao == "pegar_ouro": 
      self.pegarOuro(self)
    elif acao == "frente": 
      self.avancar(self)
    elif acao == "esquerda": 
      self.girarParaEsquerda(self)
      self.bd.inserirAcao("avancar")
      self.avancar(self)
    elif acao == "direita":
      self.girarParaDireita(self)
      self.bd.inserirAcao("avancar")
      self.avancar(self)
    else: 
      self.caminharParaSaida(self)
    
  @staticmethod
  def sairDaCaverna(self):
    if self.linha == 0 and self.coluna == 0:
      self.desempenho -= 1
      return True
    else: return False
  
  @staticmethod
  def caminharParaSaida(self):
    try:
      self.p.pop() # Posição atual
      ultima_posicao = self.p.pop()
      linha = ultima_posicao[0]
      coluna = ultima_posicao[1]

      if linha < self.linha: self.girarParaOrientacao(self, 90)
      elif linha > self.linha: self.girarParaOrientacao(self, 270)
      elif coluna < self.coluna: self.girarParaOrientacao(self, 180)
      elif coluna > self.coluna: self.girarParaOrientacao(self, 0)

      self.avancar(self)
    except: 
      print("saiu da caverna")
      self.status_agente = "fim"
      self.p = []

  @staticmethod
  def pegarOuro(self):
    self.solver.adicionarRegra(f"{self.linha}_{self.coluna}_ouro_pego")
    self.desempenho += 1000
  
  @staticmethod
  def avancar(self):
    if self.orientacao == 0: self.coluna += 1
    elif self.orientacao == 90: self.linha -= 1
    elif self.orientacao == 180: self.coluna -= 1
    elif self.orientacao == 270: self.linha += 1

    self.desempenho -= 1

  @staticmethod
  def girarParaOrientacao(self, orientacao):
    diferenca = orientacao - self.orientacao

    if diferenca == 0: pass
    elif diferenca == 90: 
      self.girarParaEsquerda(self)
    elif diferenca == -90: 
      self.girarParaDireita(self)
    elif diferenca == 180:
      self.girarParaEsquerda(self)
      self.girarParaEsquerda(self)
    elif diferenca == -180:
      self.girarParaEsquerda(self)
      self.girarParaEsquerda(self)
    elif diferenca == 270:
      self.girarParaDireita(self)
    elif diferenca == -270:
      self.girarParaEsquerda(self)

  @staticmethod
  def girarParaEsquerda(self):
    self.incrementarOrientacao(self)
    self.desempenho -= 1
  
  @staticmethod
  def girarParaDireita(self):
    self.decrementarOrientacao(self)
    self.desempenho -= 1
  
  @staticmethod
  def incrementarOrientacao(self):
    self.orientacao += 90
    if self.orientacao == 360: self.orientacao = 0
  
  @staticmethod
  def decrementarOrientacao(self):
    self.orientacao -= 90
    if self.orientacao == -90: self.orientacao = 270