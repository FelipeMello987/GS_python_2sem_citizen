from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()
    assistente = Assistente("Citizen Assist AI", base)

    print(f"=== {assistente.nome} ===")
    print("Este assistente NÃO é um canal oficial e não coleta dados pessoais.")

    while True:
        print("\n1 - Fazer uma pergunta")
        print("2 - Navegar por categorias")
        print("3 - Ver indicadores")
        print("4 - Exportar CSV")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            assistente.encerrar()
            break
        else:
            print("Opção inválida.")


main()