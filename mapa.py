from colorama import Fore, init, deinit # !pip install colorama
from tabulate import tabulate
from elementos_do_mapa import ElementosDoMapa # !pip install tabulate 
from gerador_de_mapa import GeradorDeMapa

class Mapa():
    """ O mapa é composto por wumpus (monstros mortais), poços (mortais) e
    ouro (objetivo), além disso, fedor (indica a presença de wumpus),
    brisa (indica a presença de poço) e brilho (indica a prensença de ouro) """  
    def __init__(self, linhas, colunas, quantidade_wumpus, quantidade_pocos, quantidade_ouros):
        self.linhas = linhas
        self.colunas = colunas
        self.gerador_de_mapa = GeradorDeMapa(linhas, colunas, quantidade_wumpus, quantidade_pocos, quantidade_ouros)
        self.status_posicao = self.gerador_de_mapa.retornarStatusPosicao()
        self.e_mapa = ElementosDoMapa(self.status_posicao)
    
    def retornarStatusDaPosica(self, linha, coluna):
        try: return self.status_posicao[f"{linha}_{coluna}_posicao"]
        except:
            print("Posição inválida!")
            return []

    def imprimirMapa(self):
        mapa = self.retornarMapaColorido(self)
        
        print(tabulate(mapa, tablefmt="plain", stralign="center"))
        print(Fore.WHITE) # gambiarra

    @staticmethod
    def retornarMapaColorido(self):
        mapa = []

        init(convert=True, autoreset=True) # colorama
        for linha in range(-1, self.linhas + 1):
            elementos_da_linha = []
            for coluna in range(-1, self.colunas + 1):
                elementos_da_celula = self.retornarElementosDaPosicao(self, linha, coluna)
                elementos_da_linha.append(elementos_da_celula)
            mapa.append(elementos_da_linha)
        deinit() # colorama

        return mapa
    
    @staticmethod
    def retornarElementosDaPosicao(self, linha, coluna):
        elementos_da_celula = ""
        if self.e_mapa.possuiParede(linha, coluna):
            elementos_da_celula += (Fore.MAGENTA + "parede")
        if self.e_mapa.possuiImpacto(linha, coluna):
            elementos_da_celula += (Fore.MAGENTA + str(self.e_mapa.retornarQuantidadeDeImpacto(linha, coluna)) + "impacto")
        if self.e_mapa.possuiWumpus(linha, coluna):
            elementos_da_celula += (Fore.GREEN + "wumpus")
        if self.e_mapa.possuiPoco(linha, coluna):
            elementos_da_celula += (Fore.RED + "poco")
        if self.e_mapa.possuiOuro(linha, coluna):
            elementos_da_celula += (Fore.YELLOW + "ouro")
        if self.e_mapa.possuiFedor(linha, coluna):
            elementos_da_celula += (Fore.GREEN + str(self.e_mapa.retornarQuantidadeDeFedor(linha, coluna)) + "fedor")
        if self.e_mapa.possuiBrisa(linha, coluna):
            elementos_da_celula += (Fore.RED + str(self.e_mapa.retornarQuantidadeDeBrisa(linha, coluna)) + "brisa")
        if self.e_mapa.possuiBrilho(linha, coluna):
            elementos_da_celula += (Fore.YELLOW + "brilho")
        if self.e_mapa.possuiOK(linha, coluna):
            elementos_da_celula += (Fore.WHITE + "ok")
        
        return elementos_da_celula

if __name__ == "__main__":
    mapa = Mapa(4, 4, 1, 2, 1)
    mapa.imprimirMapa()