class PreferenciasDeMapa():
  def __init__(self, linhas, colunas, qtd_wumpus, qtd_pocos, qtd_ouros):
    self.linhas = linhas
    self.colunas = colunas
    self.qtd_wumpus = qtd_wumpus
    self.qtd_pocos = qtd_pocos
    self.qtd_ouros = qtd_ouros
  
  def tamanho(self): return (self.linhas, self.colunas)
  
class InfoDoAgente():
  def __init__(self, linha = 0, coluna = 0, orientacao = 0,
              desempenho = 0, status = "explorando"):
    self.linha = linha
    self.coluna = coluna
    self.orientacao = orientacao
    self.desempenho = desempenho
    self.status = status
  
  def posicaoAtual(self): return (self.linha, self.coluna)

  def posicaoAFrente(self):
    linha = self.linha 
    coluna = self.coluna

    match self.orientacao:
      case 0: coluna += 1
      case 90: linha -= 1
      case 180: coluna -= 1
      case 270: linha += 1

    return linha, coluna

  def incrementarOrientacao(self):
    self.orientacao += 90
    if self.orientacao == 360: self.orientacao = 0
  
  def decrementarOrientacao(self):
    self.orientacao -= 90
    if self.orientacao == -90: self.orientacao = 270

class Pilha():
  def __init__(self):
    self.p = []
  
  def pop(self): return self.p.pop()
  def get(self): return self.p
  def len(self): return len(self.p)
  
  def ultPosicao(self):
    if self.p: return self.p[-1]
    return []
  
  def add(self, pos_atual):
    if self.p and self.ultPosicao() == pos_atual: pass
    else: self.p.append(pos_atual)
  
if __name__ == "__main__":  
  p = Pilha()
  print(p.ultPosicao())