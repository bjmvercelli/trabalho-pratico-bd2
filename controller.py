from view import View
from model import *

class Controller:
    def __init__(self):
        self.view = View()
        
    def start(self):
        opcao = self.view.start()

        while opcao != 2:
            if opcao == 1:
                #chama a funcao para pegar todos os generos da API
                API().getGenres()
                
                # chama a funcao para pegar o id de todos os filmes da API 
                # e a partir de cada id requisita os outros dados desse filme
                # e dados de outras tabelas relacionadas a esse filme
                API().getMovies()

            opcao = self.view.menu()

if __name__ == "__main__":
    ctrl = Controller()
    ctrl.start()