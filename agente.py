from random import choice

class Agente():
  def __init__(self, solver, base_de_conhecimento):
    self.solver = solver
    self.base_de_conhecimento = base_de_conhecimento
    self.linha = 0
    self.coluna = 0
    self.max_linha = 0
    self.max_coluna = 0
    self.orientacao = 0
    self.posicoes = []
    self.desempenho = 0
    self.status_agente = "explorando"
    self.pilha_de_exploracao = []
    self.proxima_direcao = []

  def definirDesempenho(self, desempenho):
    self.desempenho = desempenho
  
  def definirPilhaDeExploracao(self, pilha_de_exploracao):
    self.pilha_de_exploracao = pilha_de_exploracao
  
  def definirLinhaColuna(self, linha, coluna):
    self.linha = linha
    self.coluna = coluna
  
  def definirOrientacao(self, orientacao):
    self.orientacao = orientacao
  
  def Agente(self, percepcao):
    self.inferir(self, percepcao)
    self.criarNovoConhecimento(self)
    acao = self.escolherAcao(self)
    return acao
  
  @staticmethod
  def inferir(self, percepcao):
    fedor = percepcao[1][0]
    brisa = percepcao[1][1]
    brilho = percepcao[1][2]
    impacto = percepcao[1][3]
    # grito = self.percepcao[1][4]

    if fedor == 1: self.solver.possui1Fedor(self.linha, self.coluna)
    elif fedor == 2: self.solver.possui2Fedor(self.linha, self.coluna)
    elif fedor == 3: self.solver.possui3Fedor(self.linha, self.coluna)
    else: self.solver.naoPossuiFedor(self.linha, self.coluna)

    if brisa == 1: self.solver.possui1Brisa(self.linha, self.coluna)
    elif brisa == 2: self.solver.possui2Brisa(self.linha, self.coluna)
    elif brisa == 3: self.solver.possui3Brisa(self.linha, self.coluna)
    else: self.solver.naoPossuiBrisa(self.linha, self.coluna)

    if impacto == 1: self.solver.possui1Impacto(self.linha, self.coluna)
    elif impacto == 2: self.solver.possui2Impacto(self.linha, self.coluna)
    else: self.solver.naoPossuiImpacto(self.linha, self.coluna)

    if brilho: self.solver.possuiBrilho(self.linha, self.coluna)
    else: self.solver.naoPossuiBrilho(self.linha, self.coluna)

    posicao_explorada = f"{self.linha}_{self.coluna}_explorado"
    self.solver.adicionarRegra(posicao_explorada)

    self.max_linha = max(self.max_linha, self.linha)
    self.max_coluna = max(self.max_coluna, self.coluna)
    self.posicoes.append((self.linha, self.coluna))
  
  @staticmethod
  def criarNovoConhecimento(self):
    conhecimento = self.base_de_conhecimento.retornarConhecimento()
    novo_conhecimento = []

    for linha in range(0, self.max_linha + 1):
      for coluna in range(0, self.max_coluna + 1):
        # if (linha, coluna) in self.posicoes:

        regra = f"{linha}_{coluna}_wumpus"
        if self.perguntarRegraComCerteza(self, regra): novo_conhecimento.append(f"{regra}")
        elif self.perguntarRegraComCerteza(self, f"- {regra}"): novo_conhecimento.append(f"- {regra}")
        
        regra = f"{linha}_{coluna}_poco"
        if self.perguntarRegraComCerteza(self, regra): novo_conhecimento.append(f"{regra}")
        elif self.perguntarRegraComCerteza(self, f"- {regra}"): novo_conhecimento.append(f"- {regra}")

        regra = f"{linha}_{coluna}_ouro"
        if self.perguntarRegraComCerteza(self, regra): novo_conhecimento.append(f"{regra}")
        elif self.perguntarRegraComCerteza(self, f"- {regra}"): novo_conhecimento.append(f"- {regra}")

        regra = f"{linha}_{coluna}_parede"
        if self.perguntarRegraComCerteza(self, regra): novo_conhecimento.append(f"{regra}")
        elif self.perguntarRegraComCerteza(self, f"- {regra}"): novo_conhecimento.append(f"- {regra}")
      
    for atomo in novo_conhecimento: 
      if not atomo in conhecimento:
        self.base_de_conhecimento.inserirConhecimento(atomo)
        # não adicionar ao solver
  
  @staticmethod
  def escolherAcao(self):
    explorar = self.explorar(self)

    if self.perguntarSairDaCaverna(self): return "saindo_da_caverna"
    elif self.perguntarOuro(self): return "pegar_ouro"
    elif explorar: return explorar
    else: return "retornar"
  
  @staticmethod
  def perguntarSairDaCaverna(self): 
    if self.desempenho > 0: return True
    elif self.desempenho < 0 and len(self.pilha_de_exploracao) == 1 and not self.proxima_direcao: return True
    else: return False

  @staticmethod
  def perguntarOuro(self):
    ouro = self.solver.perguntarRegra(f"{self.linha}_{self.coluna}_ouro")
    pego = f"{self.linha}_{self.coluna}_ouro_pego"
    pego = self.perguntarRegraComCerteza(self, pego)
    if ouro and not pego: return True
    else: return False
  
  @staticmethod
  def explorar(self):
    # Definir direções
    busca = {
        # direcao: (pode_avancar, foi_explorado)
        "frente": (False, True),
        "esquerda": (False, True),
        "atras": (False, True),
        "direita": (False, True)        
    }

    for direcao in ["frente", "esquerda", "atras", "direita"]:
      pode_avancar = False
      foi_explorado = True

      if self.peguntarAvancar(self): pode_avancar = True
      if not self.peguntarExplorado(self): foi_explorado = False
      
      busca[direcao] = (pode_avancar, foi_explorado)
      self.incrementarOrientacao(self)

    print(busca)

    # Decidir para onde vai 
    proxima_direcao = [] # Prioridade: (True, False)
    for direcao in ["frente", "esquerda", "direita"]:
      if busca[direcao] == (True, False):
        proxima_direcao.append(direcao) 
    
    self.proxima_direcao = proxima_direcao # perguntarSairDaCaverna

    if proxima_direcao: 
      proxima_direcao = choice(proxima_direcao)
      return proxima_direcao
    else: return False

  @staticmethod
  def perguntarRegraComCerteza(self, regra):
    # Verdadeira apenas se houver certeza
    if "-" in regra:
      regra = self.solver.perguntarRegra(f"{regra}") and not self.solver.perguntarRegra(f"{regra[2:]}")
      if regra: return True
      else: return False
    else:
      regra = self.solver.perguntarRegra(f"{regra}") and not self.solver.perguntarRegra(f"- {regra}")
      if regra: return True
      else: return False

  @staticmethod
  def peguntarAvancar(self):
    linha, coluna = self.posicaoAFrente(self)

    try:
      wumpus = self.solver.perguntarRegra(f"{linha}_{coluna}_wumpus")
      poco = self.solver.perguntarRegra(f"{linha}_{coluna}_poco")
      parede = self.solver.perguntarRegra(f"{linha}_{coluna}_parede")

      return not (wumpus or poco or parede)
    except: return False
  
  @staticmethod
  def peguntarExplorado(self):
    linha, coluna = self.posicaoAFrente(self)
    explorado = not (self.solver.perguntarRegra(f"{linha}_{coluna}_explorado") and self.solver.perguntarRegra(f"- {linha}_{coluna}_explorado"))
    return explorado
    try: 
      if self.solver.perguntarRegra(f"{linha}_{coluna}_explorado"):
        if self.solver.perguntarRegra(f"- {linha}_{coluna}_explorado"): return False
        else: return True
      else: return False
    except: return False

  @staticmethod
  def posicaoAFrente(self):
    linha = self.linha
    coluna = self.coluna
    if self.orientacao == 0: coluna += 1
    elif self.orientacao == 90: linha -= 1
    elif self.orientacao == 180: coluna -= 1
    elif self.orientacao == 270: linha += 1
    return linha, coluna

  @staticmethod
  def incrementarOrientacao(self):
    self.orientacao += 90
    if self.orientacao == 360: self.orientacao = 0
  
  @staticmethod
  def decrementarOrientacao(self):
    self.orientacao -= 90
    if self.orientacao == -90: self.orientacao = 270