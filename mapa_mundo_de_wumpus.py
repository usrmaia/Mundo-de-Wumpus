from operator import truediv
from random import random
#!pip install tabulate # Exibe dados em uma grid
from tabulate import tabulate
#!pip install colorama # Dar cor ao texto
from colorama import Fore, init, deinit

class Mapa():
  def __init__(self, linhas, colunas, quantidade_wumpus, quantidade_pocos, quantidade_ouro):
    self.linhas = linhas
    self.colunas = colunas
    self.quantidade_wumpus = quantidade_wumpus
    self.taxa_wumpus = self.quantidade_wumpus / (self.linhas * self.colunas - 3)
    self.quantidade_pocos = quantidade_pocos
    self.taxa_pocos = self.quantidade_pocos / (self.linhas * self.colunas - 3 - self.quantidade_wumpus)
    self.quantidade_ouro = quantidade_ouro
    self.taxa_ouro = self.quantidade_ouro / (self.linhas * self.colunas - 3 - self.quantidade_wumpus - self.quantidade_pocos)
    self.status = {} # linha_coluna_pos -> ((wumpus, poco, ouro), (fedor, brisa, brilho, grito))
    self.mapa = []
    self.mapearStatus(self)
    self.gerarMapa(self)

  @staticmethod
  def mapearStatus(self):
    for linha in range(0, self.linhas):
      for coluna in range(0, self.colunas):
        self.status[f"{linha}_{coluna}_pos"] = ((0, 0, 0), (0, 0, 0, 0))
  
  @staticmethod
  def gerarMapa(self):
    for linha in range(0, self.linhas):
      for coluna in range(0, self.colunas):
        if self.insercaoValida(linha, coluna):
          self.adicionarWumpusEFedor(self, linha, coluna)
          self.adicionarPocoEBrisa(self, linha, coluna)
          self.adicionarOuroEBrilho(self, linha, coluna)

  def imprimirMapa(self):
    init() # colorama
    for linha in range(0, self.linhas):
      elementos_da_linha = []
      for coluna in range(0, self.colunas):
        if self.possuiWumpus(self, linha, coluna):
          elementos_da_linha.append(Fore.GREEN + "wumpus")
        elif self.possuiPoco(self, linha, coluna):
          elementos_da_linha.append(Fore.RED + "poco")
        elif self.possuiBrilho(self, linha, coluna):
          elementos_da_linha.append(Fore.YELLOW + "ouro")
        elif self.possuiFedor(self, linha, coluna):
          elementos_da_linha.append(Fore.GREEN + str(self.possuiFedor(self, linha, coluna)) + "fedor")
        elif self.possuiBrisa(self, linha, coluna):
          elementos_da_linha.append(Fore.RED + str(self.possuiBrisa(self, linha, coluna)) + "brisa")
        elif self.possuiOK(self, linha, coluna):
          elementos_da_linha.append(Fore.WHITE + "ok")
      
      self.mapa.append(elementos_da_linha)
    deinit() # colorama
        
    print(tabulate(self.mapa, tablefmt="plain", stralign="center"))
  
  def retornarStatusDaPosica(self, linha, coluna):
    try:
      return self.status[f"{linha}_{coluna}_pos"]
    except:
      print("Posição inválida!")
      return False

  @staticmethod
  def insercaoValida(linha, coluna):
    return not ((linha == 0 and coluna == 0) or (linha == 0 and coluna == 1) or (linha == 1 and coluna == 0))

  @staticmethod
  def adicionarWumpusEFedor(self, linha, coluna):
    if self.quantidade_wumpus >= 1:
      if random() < self.taxa_wumpus:
        self.adicionarWumpus(self, linha, coluna)
        self.adicionarFedor(self, linha - 1, coluna)
        self.adicionarFedor(self, linha, coluna - 1)
        self.adicionarFedor(self, linha + 1, coluna)
        self.adicionarFedor(self, linha, coluna + 1)
        self.quantidade_wumpus -= 1
  
  @staticmethod
  def adicionarPocoEBrisa(self, linha, coluna):
    if self.quantidade_pocos >= 1 and not self.possuiWumpus(self, linha, coluna):
      if random() < self.taxa_pocos:
        self.adicionarPoco(self, linha, coluna)
        self.incrementaBrisa(self, linha - 1, coluna)
        self.incrementaBrisa(self, linha, coluna - 1)
        self.incrementaBrisa(self, linha + 1, coluna)
        self.incrementaBrisa(self, linha, coluna + 1)
        self.quantidade_pocos -= 1
  
  @staticmethod
  def adicionarOuroEBrilho(self, linha, coluna):
    if self.quantidade_ouro >= 1 and not (self.possuiWumpus(self, linha, coluna) or self.possuiPoco(self, linha, coluna)):
      if random() < self.taxa_ouro:
        self.adicionarOuro(self, linha, coluna)
        self.incrementaBrilho(self, linha, coluna)
        self.quantidade_ouro -= 1

  @staticmethod
  def adicionarWumpus(self, linha, coluna):
    status = self.status[f"{linha}_{coluna}_pos"]
    status = ((status[0][0] + 1, status[0][1], status[0][2]), (status[1]))
    self.status[f"{linha}_{coluna}_pos"] = status

  @staticmethod
  def adicionarFedor(self, linha, coluna):
    try:
      status = self.status[f"{linha}_{coluna}_pos"]
      status = ((status[0]), (status[1][0] + 1, status[1][1], status[1][2], status[1][3]))
      self.status[f"{linha}_{coluna}_pos"] = status
    except: pass
  
  @staticmethod
  def possuiWumpus(self, linha, coluna):
    if self.status[f"{linha}_{coluna}_pos"][0][0]:
      return True
    return False

  @staticmethod
  def adicionarPoco(self, linha, coluna):
    status = self.status[f"{linha}_{coluna}_pos"]
    status = ((status[0][0], status[0][1] + 1, status[0][2]), (status[1]))
    self.status[f"{linha}_{coluna}_pos"] = status

  @staticmethod
  def incrementaBrisa(self, linha, coluna):
    try:
      status = self.status[f"{linha}_{coluna}_pos"]
      status = ((status[0]), (status[1][0], status[1][1] + 1, status[1][2], status[1][3]))
      self.status[f"{linha}_{coluna}_pos"] = status
    except: pass
  
  @staticmethod
  def possuiPoco(self, linha, coluna):
    if self.status[f"{linha}_{coluna}_pos"][0][1]:
      return True
    return False
  
  @staticmethod
  def adicionarOuro(self, linha, coluna):
    status = self.status[f"{linha}_{coluna}_pos"]
    status = ((status[0][0], status[0][1], status[0][2] + 1), (status[1]))
    self.status[f"{linha}_{coluna}_pos"] = status
  
  @staticmethod
  def incrementaBrilho(self, linha, coluna):
    status = self.status[f"{linha}_{coluna}_pos"]
    status = ((status[0]), (status[1][0], status[1][1], status[1][2] + 1, status[1][3])) 
    self.status[f"{linha}_{coluna}_pos"] = status
  
  @staticmethod
  def possuiFedor(self, linha, coluna):
    fedor = self.status[f"{linha}_{coluna}_pos"][1][0]
    if fedor:
      return fedor
    return False
  
  @staticmethod
  def possuiBrisa(self, linha, coluna):
    brisa = self.status[f"{linha}_{coluna}_pos"][1][1]
    if brisa:
      return brisa
    return False
  
  @staticmethod
  def possuiBrilho(self, linha, coluna):
    if self.status[f"{linha}_{coluna}_pos"][1][2]:
      return True
    return False
  
  @staticmethod
  def possuiOK(self, linha, coluna):
    status = self.status[f"{linha}_{coluna}_pos"]
    for tupla in status:
      for i in tupla:
        if i != 0:
          return False
    return True


mapa = Mapa(6, 6, 2, 5, 2)
mapa.imprimirMapa()
