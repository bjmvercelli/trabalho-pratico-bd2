class View():
    def start(self):
        return self.menu()

    def menu(self):
        print("M E N U")
        print("1. Requisitar")
        print("2. Sair")
        print()
        opcao = int(input("Digite a opcao desejada: "))
        print()
        return opcao