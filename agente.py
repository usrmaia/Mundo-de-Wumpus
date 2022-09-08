from email.policy import default
from random import choice
from colorama import Fore, init, deinit 
from tabulate import tabulate
from atuador import Atuador
from util import InfoDoAgente, Pilha

class Agente():
  def __init__(self, s, BD):
    self.s = s
    self.bd = BD
    self.info = InfoDoAgente()
    self.p = Pilha()
    self.proxima_direcao = []
    self.atuador = Atuador(self.s, self.bd, self.p, self.info)

  def retornarInformacoesDoAgente(self): return self.info
  def atualizarPilha(self, Pilha): self.p = Pilha
  
  # TODO fazer objeto percepcao
  def Agente(self, percepcao):
    self.inferir(self, percepcao)
    acao = self.escolherAcao(self)
    return acao
  
  @staticmethod
  def inferir(self, percepcao):
    fedor = percepcao[1][0]
    brisa = percepcao[1][1]
    brilho = percepcao[1][2]
    impacto = percepcao[1][3]

    match fedor:
      case 0: self.s.naoPossuiFedor(self.info.linha, self.info.coluna)
      case 1: self.s.possui1Fedor(self.info.linha, self.info.coluna)
      case 2: self.s.possui2Fedor(self.info.linha, self.info.coluna)
      case 3: self.s.possui3Fedor(self.info.linha, self.info.coluna)
    
    match brisa:
      case 0: self.s.naoPossuiBrisa(self.info.linha, self.info.coluna)
      case 1: self.s.possui1Brisa(self.info.linha, self.info.coluna)
      case 2: self.s.possui2Brisa(self.info.linha, self.info.coluna)
      case 3: self.s.possui3Brisa(self.info.linha, self.info.coluna)
    
    match impacto:
      case 1: self.s.possui1Impacto(self.info.linha, self.info.coluna)
      case 2: self.s.possui2Impacto(self.info.linha, self.info.coluna)
      case _: self.s.naoPossuiImpacto(self.info.linha, self.info.coluna)
    
    match brilho:
      case 0: self.s.naoPossuiBrilho(self.info.linha, self.info.coluna)
      case 1: self.s.possuiBrilho(self.info.linha, self.info.coluna)

    posicao_explorada = f"{self.info.linha}_{self.info.coluna}_explorado"
    self.s.adicionarRegra(posicao_explorada)  
  
  def imprimirMapa(self):
      mapa = []
      init() # colorama
      for linha in range(-1, 5):
        elementos_da_linha = []
        for coluna in range(-1, 5):
          elementos_da_celula = ""

          if linha == self.info.linha and coluna == self.info.coluna:
            elementos_da_celula += (Fore.WHITE + f"agente{self.info.orientacao}")

          if self.s.perguntarRegra(f"{linha}_{coluna}_wumpus"):
            elementos_da_celula += (Fore.GREEN + "wumpus")
          if self.s.perguntarRegra(f"{linha}_{coluna}_poco"):
            elementos_da_celula += (Fore.RED + "poco")
          if self.s.perguntarRegra(f"{linha}_{coluna}_ouro"):
            elementos_da_celula += (Fore.YELLOW + "ouro")
          if self.s.perguntarRegra(f"{linha}_{coluna}_parede"):
            elementos_da_celula += (Fore.MAGENTA + "parede")
          if self.s.perguntarRegra(f"{linha}_{coluna}_fedor"):
            elementos_da_celula += (Fore.GREEN + "fedor")
          if self.s.perguntarRegra(f"{linha}_{coluna}_brisa"):
            elementos_da_celula += (Fore.RED + "brisa")
          if self.s.perguntarRegra(f"{linha}_{coluna}_brilho"):
            elementos_da_celula += (Fore.YELLOW + "brilho")
          if self.s.perguntarRegra(f"{linha}_{coluna}_impacto"):
            elementos_da_celula += (Fore.MAGENTA + "impacto")
          
          if elementos_da_celula == "": elementos_da_celula += (Fore.WHITE + "ok") 
          
          elementos_da_linha.append(elementos_da_celula)
        mapa.append(elementos_da_linha)
      deinit() # colorama
      print(tabulate(mapa, tablefmt="plain", stralign="center"))
      print(Fore.WHITE) # bug - remover fará com que todas os outputs fiquem coloridos
  
  @staticmethod
  def escolherAcao(self):
    explorar = self.podeExplorar(self)

    if self.podeSairDaCaverna(self): return "saindo_da_caverna"
    elif self.temOuro(self): return "pegar_ouro"
    elif explorar: return explorar
    else: return "retornar"
  
  @staticmethod
  def podeSairDaCaverna(self): 
    if self.info.desempenho > 0: return True
    elif self.info.desempenho < 0 and self.p.len() == 1 \
      and not self.proxima_direcao: return True
    else: return False

  @staticmethod
  def temOuro(self):
    regra_tem_ouro = f"{self.info.linha}_{self.info.coluna}_ouro"
    ouro = self.s.perguntarRegraComCerteza(regra_tem_ouro)
    regra_foi_pego = f"{self.info.linha}_{self.info.coluna}_ouro_pego"
    pego = self.s.perguntarRegraComCerteza(regra_foi_pego)
    
    if ouro and not pego: return True
    else: return False
  
  @staticmethod
  def podeExplorar(self):
    status_adjacentes = self.retornarStatusAdjacentes(self)
    # print(status_adjacentes)
    proxima_direcao = self.retornarProximaDirecao(self, status_adjacentes)
    return proxima_direcao
    
  @staticmethod
  def retornarStatusAdjacentes(self):
    status_adjacentes = {
      # direcao: (pode_avancar, foi_explorado)
    }

    for direcao in ["frente", "esquerda", "atras", "direita"]:
      pode_avancar = False
      foi_explorado = True

      if self.podeAvancar(self): pode_avancar = True

      linha, coluna = self.info.posicaoAFrente()
      if not self.foiExplorado(self, linha, coluna): foi_explorado = False
      
      status_adjacentes[direcao] = (pode_avancar, foi_explorado)
      self.info.incrementarOrientacao()

    return status_adjacentes

  @staticmethod
  def retornarProximaDirecao(self, status_adjacentes):
    proxima_direcao = [] # Prioridade: (True, False)
    
    for direcao in ["frente", "esquerda", "atras", "direita"]:
      if status_adjacentes[direcao] == (True, False):
        proxima_direcao.append(direcao) 
    
    self.proxima_direcao = proxima_direcao # usado em podeSairDaCaverna()

    if proxima_direcao: return choice(proxima_direcao)
    return []

  @staticmethod
  def podeAvancar(self):
    linha, coluna = self.info.posicaoAFrente()

    try:
      wumpus = self.s.perguntarRegra(f"{linha}_{coluna}_wumpus")
      poco = self.s.perguntarRegra(f"{linha}_{coluna}_poco")
      parede = self.s.perguntarRegra(f"{linha}_{coluna}_parede")

      return not (wumpus or poco or parede)
    except: return False
  
  @staticmethod
  def foiExplorado(self, linha, coluna):
    regra = f"{linha}_{coluna}_explorado"
    explorado = self.s.perguntarRegraComCerteza(regra)
    # explorado = not (self.s.perguntarRegra(f"{linha}_{coluna}_explorado") and self.s.perguntarRegra(f"- {linha}_{coluna}_explorado"))
    return explorado