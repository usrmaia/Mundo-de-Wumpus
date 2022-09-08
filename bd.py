import sqlite3 # !pip install db-sqlite3
from tabulate import tabulate # !pip install tabulate 

class BD:
    def __init__(self):
        self.conn = sqlite3.connect("base_de_conhecimento")
        self.cursor = self.conn.cursor()
        self.droparTabela(self)
        self.criarTabela(self)

    def imprimirTabela(self):
        query = "select * from base_de_conhecimento"
        query = self.retornarQuery(self, query)
        
        header = ["Tempo", "Conhecimento", "Raciocínio", "Ação"]
        print(tabulate(query, tablefmt="simple", stralign="center", headers=header))

    def inserirConhecimento(self, conhecimento):
        comando = f"insert into base_de_conhecimento (conhecimento) values ('{conhecimento}')"
        self.executarComando(self, comando)
    
    def inserirRaciocinio(self, raciocinio):
        comando = f"insert into base_de_conhecimento (raciocinio) values ('{raciocinio}')"
        self.executarComando(self, comando)
    
    def inserirAcao(self, acao):
        comando = f"insert into base_de_conhecimento (acao) values ('{acao}')"
        self.executarComando(self, comando)
    
    def retornarConhecimento(self):
        query = f"select conhecimento from base_de_conhecimento"
        tabela = self.retornarQuery(self, query)
        conhecimento = []

        for atomo in tabela: 
            if atomo[0]: conhecimento.append(atomo[0])

        return conhecimento
    
    @staticmethod
    def criarTabela(self):
        self.executarComando(self, """
            create table if not exists base_de_conhecimento (
                tempo integer primary key autoincrement,
                conhecimento varchar,
                raciocinio varchar,
                acao varchar
            )
        """)

    @staticmethod
    def droparTabela(self):
        self.executarComando(self, """
            drop table if exists base_de_conhecimento
        """)

    @staticmethod
    def executarComando(self, comando):
        try:
            self.cursor.execute(comando)
            self.conn.commit()
        except sqlite3.Error as erro:
            print(f"Error: {erro}")
    
    @staticmethod
    def retornarQuery(self, query):
        try:
            self.cursor.execute(query)
            query = self.cursor.fetchall()
            return query
        except sqlite3.Error as erro:
            print(f"Erro: {erro}")
            return []

if __name__ == "__main__":
    bd = BD()
    bd.imprimirTabela()
