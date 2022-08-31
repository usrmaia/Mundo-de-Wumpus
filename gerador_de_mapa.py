from random import random
from elementos_do_mapa import ElementosDoMapa

class GeradorDeMapa():
    def __init__(self, linhas, colunas, quantidade_wumpus, quantidade_pocos, quantidade_ouros):
        self.linhas = linhas
        self.colunas = colunas
        self.quantidade_wumpus = quantidade_wumpus
        self.quantidade_pocos = quantidade_pocos
        self.quantidade_ouros = quantidade_ouros
        self.taxa_wumpus = self.quantidade_wumpus / (self.linhas * self.colunas - 1 - self.quantidade_pocos - self.quantidade_ouros)
        self.taxa_pocos = self.quantidade_pocos / (self.linhas * self.colunas - 1 - self.quantidade_wumpus - self.quantidade_ouros)
        self.taxa_ouros = self.quantidade_ouros / (self.linhas * self.colunas - 1 - self.quantidade_wumpus - self.quantidade_pocos)
        self.status_posicao = {} # {linha}_{coluna}_posicao: ((wumpus, poco, ouro, parede), (fedor, brisa, brilho, impacto, grito))
        self.mapa = []
        self.e_mapa = ElementosDoMapa(self.status_posicao)
        self.gerarMapa()
    
    def retornarStatusPosicao(self):
        return self.status_posicao
    
    def gerarMapa(self):
        self.mapearStatusDePosicao(self)
        for linha in range(-1, self.linhas + 1):
            for coluna in range(-1, self.colunas + 1):
                if self.insercaoValida(self, linha, coluna):
                    self.adicionarWumpusEFedor(self, linha, coluna)
                    self.adicionarPocoEBrisa(self, linha, coluna)
                    self.adicionarOuroEBrilho(self, linha, coluna)
                self.adicionarParedeEImpacto(self, linha, coluna)

    @staticmethod
    def mapearStatusDePosicao(self):
        for linha in range(-1, self.linhas + 1):
            for coluna in range(-1, self.colunas + 1):
                status_default = ((0, 0, 0, 0), (0, 0, 0, 0, 0))
                self.status_posicao[f"{linha}_{coluna}_posicao"] = status_default
    
    @staticmethod
    def insercaoValida(self, linha, coluna):
        posicao_inicial = (linha == 0 and coluna == 0)
        borda = (linha == -1 or linha == self.linhas or coluna == -1 or coluna == self.colunas)
        return not (posicao_inicial or borda)

    @staticmethod
    def adicionarWumpusEFedor(self, linha, coluna):
        pode_adicionar = self.quantidade_wumpus >= 1
        roleta = random() < self.taxa_wumpus
        if pode_adicionar and roleta:
            self.adicionarWumpus(self, linha, coluna)
            self.adicionarFedor(self, linha - 1, coluna)
            self.adicionarFedor(self, linha, coluna - 1)
            self.adicionarFedor(self, linha + 1, coluna)
            self.adicionarFedor(self, linha, coluna + 1)
            self.quantidade_wumpus -= 1
  
    @staticmethod
    def adicionarPocoEBrisa(self, linha, coluna):
        pode_adicionar = self.quantidade_pocos >= 1 and not self.e_mapa.possuiWumpus(linha, coluna)
        roleta = random() < self.taxa_pocos
        if pode_adicionar and roleta:
            self.adicionarPoco(self, linha, coluna)
            self.adicionarBrisa(self, linha - 1, coluna)
            self.adicionarBrisa(self, linha, coluna - 1)
            self.adicionarBrisa(self, linha + 1, coluna)
            self.adicionarBrisa(self, linha, coluna + 1)
            self.quantidade_pocos -= 1
        
    @staticmethod
    def adicionarOuroEBrilho(self, linha, coluna):
        pode_adicionar = self.quantidade_ouros >= 1 and not (self.e_mapa.possuiWumpus(linha, coluna) or self.e_mapa.possuiPoco(linha, coluna))
        roleta = random() < self.taxa_ouros
        if pode_adicionar and roleta:
            self.adicionarOuro(self, linha, coluna)
            self.adicionarBrilho(self, linha, coluna)
            self.quantidade_ouros -= 1
    
    @staticmethod
    def adicionarParedeEImpacto(self, linha, coluna):
        e_borda = (linha == -1 or linha == self.linhas) or (coluna == -1 or coluna == self.colunas)
        if e_borda: 
            self.adicionarParede(self, linha, coluna)
            self.adicionarImpacto(self, linha - 1, coluna)
            self.adicionarImpacto(self, linha, coluna - 1)
            self.adicionarImpacto(self, linha + 1, coluna)
            self.adicionarImpacto(self, linha, coluna + 1)

    @staticmethod
    def adicionarWumpus(self, linha, coluna):
        status = self.status_posicao[f"{linha}_{coluna}_posicao"]
        status = ((status[0][0] + 1, status[0][1], status[0][2], status[0][3]), (status[1]))
        self.status_posicao[f"{linha}_{coluna}_posicao"] = status
  
    @staticmethod
    def adicionarPoco(self, linha, coluna):
        status = self.status_posicao[f"{linha}_{coluna}_posicao"]
        status = ((status[0][0], status[0][1] + 1, status[0][2], status[0][3]), (status[1]))
        self.status_posicao[f"{linha}_{coluna}_posicao"] = status
  
    @staticmethod
    def adicionarOuro(self, linha, coluna):
        status = self.status_posicao[f"{linha}_{coluna}_posicao"]
        status = ((status[0][0], status[0][1], status[0][2] + 1, status[0][3]), (status[1]))
        self.status_posicao[f"{linha}_{coluna}_posicao"] = status
  
    @staticmethod
    def adicionarParede(self, linha, coluna):
        status = self.status_posicao[f"{linha}_{coluna}_posicao"]
        status = ((status[0][0], status[0][1], status[0][2], status[0][3] + 1), (status[1])) 
        self.status_posicao[f"{linha}_{coluna}_posicao"] = status

    @staticmethod
    def adicionarFedor(self, linha, coluna):
        if self.insercaoValida(self, linha, coluna) or (linha == 0 and coluna == 0):
            status = self.status_posicao[f"{linha}_{coluna}_posicao"]
            status = ((status[0]), (status[1][0] + 1, status[1][1], status[1][2], status[1][3], status[1][4]))
            self.status_posicao[f"{linha}_{coluna}_posicao"] = status

    @staticmethod
    def adicionarBrisa(self, linha, coluna):
        if self.insercaoValida(self, linha, coluna) or (linha == 0 and coluna == 0):
            status = self.status_posicao[f"{linha}_{coluna}_posicao"]
            status = ((status[0]), (status[1][0], status[1][1] + 1, status[1][2], status[1][3], status[1][4]))
            self.status_posicao[f"{linha}_{coluna}_posicao"] = status
  
    @staticmethod
    def adicionarBrilho(self, linha, coluna):
        status = self.status_posicao[f"{linha}_{coluna}_posicao"]
        status = ((status[0]), (status[1][0], status[1][1], status[1][2] + 1, status[1][3], status[1][4])) 
        self.status_posicao[f"{linha}_{coluna}_posicao"] = status
  
    @staticmethod
    def adicionarImpacto(self, linha, coluna):
        e_linha_externa = linha >= 0 and linha <= self.linhas - 1
        e_coluna_externa = coluna >= 0 and coluna <= self.colunas - 1

        if e_linha_externa and e_coluna_externa:
            status = self.status_posicao[f"{linha}_{coluna}_posicao"]
            status = ((status[0]), (status[1][0], status[1][1], status[1][2], status[1][3] + 1, status[1][4])) 
            self.status_posicao[f"{linha}_{coluna}_posicao"] = status