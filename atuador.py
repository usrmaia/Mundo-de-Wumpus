class Atuador():
  def __init__(self, Solver, BD, Pilha, InfoDoAgente):
    self.bd = BD
    self.p = Pilha # Busca em profundidade
    self.info = InfoDoAgente
    self.s = Solver

  def Atuar(self, acao):
    if acao == "saindo_da_caverna":
      if self.sairDaCaverna(self): 
        print("saiu da caverna")
        self.info.status = "fim"
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
    if self.info.posicaoAtual() == (0, 0):
      self.info.desempenho -= 1
      return True
    else: return False
  
  @staticmethod
  def caminharParaSaida(self):
    try:
      self.p.pop() # Posição atual
      ultima_posicao = self.p.ultPosicao()
      linha = ultima_posicao[0]
      coluna = ultima_posicao[1]

      if linha < self.info.linha: self.girarParaOrientacao(self, 90)
      elif linha > self.info.linha: self.girarParaOrientacao(self, 270)
      elif coluna < self.info.coluna: self.girarParaOrientacao(self, 180)
      elif coluna > self.info.coluna: self.girarParaOrientacao(self, 0)

      self.avancar(self)
    except: 
      print("saiu da caverna")
      self.info.status_agente = "fim"

  @staticmethod
  def pegarOuro(self):
    self.s.adicionarRegra(f"{self.info.linha}_{self.info.coluna}_ouro_pego")
    self.info.desempenho += 1000
  
  @staticmethod
  def avancar(self):
    if self.info.orientacao == 0: self.info.coluna += 1
    elif self.info.orientacao == 90: self.info.linha -= 1
    elif self.info.orientacao == 180: self.info.coluna -= 1
    elif self.info.orientacao == 270: self.info.linha += 1

    self.info.desempenho -= 1

  @staticmethod
  def girarParaOrientacao(self, orientacao):
    diferenca = orientacao - self.info.orientacao

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
    self.info.incrementarOrientacao()
    self.info.desempenho -= 1
  
  @staticmethod
  def girarParaDireita(self):
    self.info.decrementarOrientacao()
    self.info.desempenho -= 1