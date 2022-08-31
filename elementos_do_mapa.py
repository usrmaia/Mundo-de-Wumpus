class ElementosDoMapa():
    def __init__(self, status_posicao):
        self.status_posicao = status_posicao

    def possuiWumpus(self, linha, coluna):
        if self.status_posicao[f"{linha}_{coluna}_posicao"][0][0]:
            return True
        return False
  
    def possuiPoco(self, linha, coluna):
        if self.status_posicao[f"{linha}_{coluna}_posicao"][0][1]:
            return True
        return False
  
    def possuiOuro(self, linha, coluna):
        if self.status_posicao[f"{linha}_{coluna}_posicao"][0][2]:
            return True
        return False
  
    def possuiParede(self, linha, coluna):
        if self.status_posicao[f"{linha}_{coluna}_posicao"][0][3]:
            return True
        return False
  
    def possuiFedor(self, linha, coluna):
        fedor = self.status_posicao[f"{linha}_{coluna}_posicao"][1][0]
        if fedor:
            return True
        return False
    
    def retornarQuantidadeDeFedor(self, linha, coluna):
        fedor = self.status_posicao[f"{linha}_{coluna}_posicao"][1][0]
        return fedor
  
    def possuiBrisa(self, linha, coluna):
        brisa = self.status_posicao[f"{linha}_{coluna}_posicao"][1][1]
        if brisa:
            return brisa
        return False
    
    def retornarQuantidadeDeBrisa(self, linha, coluna):
        brisa = self.status_posicao[f"{linha}_{coluna}_posicao"][1][1]
        return brisa
  
    def possuiBrilho(self, linha, coluna):
        if self.status_posicao[f"{linha}_{coluna}_posicao"][1][2]:
            return True
        return False
  
    def possuiImpacto(self, linha, coluna):
        impacto = self.status_posicao[f"{linha}_{coluna}_posicao"][1][3]
        if impacto:
            return impacto
        return False
    
    def retornarQuantidadeDeImpacto(self, linha, coluna):
        impacto = self.status_posicao[f"{linha}_{coluna}_posicao"][1][3]
        return impacto
  
    def possuiOK(self, linha, coluna):
        status = self.status_posicao[f"{linha}_{coluna}_posicao"]
        for tupla in status:
            for elemento in tupla:
                if elemento != 0:
                    return False
        return True