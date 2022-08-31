from colorama import Fore, init, deinit # !pip install colorama
from tabulate import tabulate # !pip install tabulate 
from mapa import Mapa
from bd import BD
from solver import Solver
from agente import Agente

class MundoDeWumpus():
  def __init__(self):
    self.mapa = Mapa(linhas = 4, colunas = 4, quantidade_wumpus = 1, quantidade_pocos = 2, quantidade_ouros = 2)
    # self.mapa.gerarMapa()
    self.base_de_conhecimento = BD()
    self.solver = Solver(4, 4, self.base_de_conhecimento)
    self.agente = Agente(self.solver, self.base_de_conhecimento)
    self.linha = 0
    self.coluna = 0
    self.orientacao = 0 # ângulo
    self.desempenho = 0
    self.status_agente = "explorando"
    self.pilha_de_exploracao = []
  
  def imprimirMapa(self):
    self.mapa.imprimirMapa()
  
  def resolverMundoDeWumpus(self):
    while self.status_agente == "explorando":
    #if self.status_agente == "explorando":
      self.empilharPosicao(self)
      self.agente.definirDesempenho(self.desempenho)
      self.agente.definirPilhaDeExploracao(self.pilha_de_exploracao)
      self.agente.definirLinhaColuna(self.linha, self.coluna)
      self.agente.definirOrientacao(self.orientacao)

      percepcao = self.receberSensor(self)
      acao = self.agente.Agente(percepcao)
      self.base_de_conhecimento.inserirAcao(acao)

      print(f"posicao: {self.agente.linha}_{self.agente.coluna}") 
      try: print(f"percepcao: {percepcao}") 
      except: pass
      print(f"desenpenho: {self.desempenho} status_argente: {self.status_agente}")
      print(f"pilha_de_exploracao: {self.pilha_de_exploracao}")

      self.atuadores(self, acao)

      self.validarVida(self, percepcao)
  
  @staticmethod
  def empilharPosicao(self):
    posicao_atual = (self.linha, self.coluna)
    if self.pilha_de_exploracao:
      ultima_posicao = self.pilha_de_exploracao[-1]
      linha = ultima_posicao[0]
      coluna = ultima_posicao[1]
      ultima_posicao = (linha, coluna)
      if ultima_posicao == posicao_atual: pass
      else: self.pilha_de_exploracao.append(posicao_atual)
    else: self.pilha_de_exploracao.append(posicao_atual)
  
  @staticmethod
  def validarVida(self, percepcao):
    wumpus = percepcao[0][0]
    poco = percepcao[0][1]
    parede = percepcao[0][3]

    if wumpus or poco or parede: 
      self.status_agente == "morto"
      print("Agente morto")
      exit(1)
  
  @staticmethod
  def atuadores(self, acao):
    if acao == "saindo_da_caverna":
      if self.sairDaCaverna(self): 
        print("saiu da caverna")
        self.status_agente = "fim"
        self.base_de_conhecimento.inserirAcao("sair_da_caverna")
      else: self.caminharParaVoltar(self)      
    elif acao == "pegar_ouro": self.pegarOuro(self)
    elif acao == "frente": self.avancar(self)
    elif acao == "esquerda": 
      self.girarParaEsquerda(self)
      self.base_de_conhecimento.inserirAcao("avancar")
      self.avancar(self)
    elif acao == "direita":
      self.girarParaDireita(self)
      self.base_de_conhecimento.inserirAcao("avancar")
      self.avancar(self)
    else: 
      self.caminharParaVoltar(self) 
  
  def imprimirMapaDoConhecimento(self):
    mapa = []
    init() # colorama
    for linha in range(-1, 5):
      elementos_da_linha = []
      for coluna in range(-1, 5):
        elementos_da_celula = ""

        if linha == self.linha and coluna == self.coluna:
          elementos_da_celula += (Fore.WHITE + f"agente{self.orientacao}")

        if self.solver.perguntarRegra(f"{linha}_{coluna}_wumpus"):
          elementos_da_celula += (Fore.GREEN + "wumpus")
        if self.solver.perguntarRegra(f"{linha}_{coluna}_poco"):
          elementos_da_celula += (Fore.RED + "poco")
        if self.solver.perguntarRegra(f"{linha}_{coluna}_ouro"):
          elementos_da_celula += (Fore.YELLOW + "ouro")
        if self.solver.perguntarRegra(f"{linha}_{coluna}_parede"):
          elementos_da_celula += (Fore.MAGENTA + "parede")
        if self.solver.perguntarRegra(f"{linha}_{coluna}_fedor"):
          elementos_da_celula += (Fore.GREEN + "fedor")
        if self.solver.perguntarRegra(f"{linha}_{coluna}_brisa"):
          elementos_da_celula += (Fore.RED + "brisa")
        if self.solver.perguntarRegra(f"{linha}_{coluna}_brilho"):
          elementos_da_celula += (Fore.YELLOW + "brilho")
        if self.solver.perguntarRegra(f"{linha}_{coluna}_impacto"):
          elementos_da_celula += (Fore.MAGENTA + "impacto")
        
        if elementos_da_celula == "": elementos_da_celula += (Fore.WHITE + "ok") 
        
        elementos_da_linha.append(elementos_da_celula)
      mapa.append(elementos_da_linha)
    deinit() # colorama
    print(tabulate(mapa, tablefmt="plain", stralign="center"))
    print(Fore.WHITE) # gambiarra
  
  def imprimirBaseDeConhecimento(self):
    self.base_de_conhecimento.imprimirTabela()
  
  @staticmethod
  def receberSensor(self):
    return self.mapa.retornarStatusDaPosica(self.linha, self.coluna)  

  @staticmethod
  def sairDaCaverna(self):
    if self.linha == 0 and self.coluna == 0:
      self.desempenho -= 1
      return True
    else: return False
  
  @staticmethod
  def caminharParaVoltar(self):
    try:
      self.pilha_de_exploracao.pop() # Posição atual
      ultima_posicao = self.pilha_de_exploracao.pop()
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
      self.pilha_de_exploracao = []

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
    print(f"diferenca = orientacao - self.orientacao: {diferenca} = {orientacao} - {self.orientacao}")

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

if __name__ == "__main__":
    mundo_de_wumpus = MundoDeWumpus()
    mundo_de_wumpus.imprimirMapa()
    mundo_de_wumpus.resolverMundoDeWumpus()
    mundo_de_wumpus.imprimirMapaDoConhecimento()
    mundo_de_wumpus.imprimirBaseDeConhecimento()