from atuador import Atuador
from mapa import Mapa
from bd import BD
from solver import Solver
from agente import Agente
from util import Pilha, PreferenciasDeMapa

class MundoDeWumpus():
  def __init__(self, PreferenciasDeMapa, BD):
    self.mapa = Mapa(PreferenciasDeMapa)
    self.bd = BD
    self.s = Solver(PreferenciasDeMapa.tamanho(), self.bd)
    self.p = Pilha() # Busca em profundidade
    self.agente = Agente(self.s, self.bd)
    self.atuador = Atuador(self.s, self.bd, self.p, self.agente.info)
  
  def resolverMundoDeWumpus(self):
    info = self.agente.retornarInformacoesDoAgente()

    #while info.status == "explorando":
    if info.status == "explorando":
      self.p.add(info.posicaoAtual())
      self.agente.atualizarPilha(self.p)

      percepcao = self.receberSensor(self)
      acao = self.agente.Agente(percepcao)
      self.bd.inserirAcao(acao)

      print(f"posicao: {info.posicaoAtual()}") 
      print(f"percepcao: {percepcao}") 
      print(f"desempenho: {info.desempenho} status: {info.status}")
      print(f"ação: {acao}")
      print(f"pilha_de_exploracao: {self.p.get()}")

      self.atuador.Atuar(acao)

      self.validarVida(self, percepcao)
  
  def imprimirMapa(self):
    self.mapa.imprimirMapa()
  
  def imprimirMapaDoConhecimento(self):
    self.agente.imprimirMapa()
  
  def imprimirBaseDeConhecimento(self):
    self.bd.imprimirTabela()
  
  @staticmethod
  def validarVida(self, percepcao):
    wumpus = percepcao[0][0]
    poco = percepcao[0][1]
    parede = percepcao[0][3]

    if wumpus or poco or parede: 
      self.agente.info.status = "morto"
      print("Agente morto")
      exit(1) 
  
  @staticmethod
  def receberSensor(self):
    pos_atual = self.agente.info.posicaoAtual()
    return self.mapa.retornarStatusDaPosica(pos_atual)  
  
if __name__ == "__main__":
  pref_mapa = PreferenciasDeMapa(
                linhas = 4,
                colunas = 4, 
                qtd_wumpus = 1, 
                qtd_pocos = 1, 
                qtd_ouros = 2
              )
  bd = BD()
  mw = MundoDeWumpus(pref_mapa, bd)

  while(input() == "" and mw.agente.info.status != "fim"):
    mw.resolverMundoDeWumpus()
    mw.imprimirMapa()
    mw.imprimirMapaDoConhecimento()
    # bd.imprimirTabela()