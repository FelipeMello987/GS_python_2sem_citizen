import csv
import json
import os
import time
from datetime import datetime

CAMINHO_HISTORICO = "data/historico.json"
CAMINHO_CSV = "data/atendimentos.csv"
CAMPOS = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
          "ajudou", "tentativas", "tempo", "nota"]


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = self.carregar_historico()
        self.registros_sessao = 0

    def carregar_historico(self):
        try:
            with open(CAMINHO_HISTORICO, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if isinstance(dados, list):
                return dados
        except (OSError, json.JSONDecodeError):
            pass
        return []

    def salvar_historico(self):
        try:
            os.makedirs("data", exist_ok=True)
            with open(CAMINHO_HISTORICO, "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)
        except OSError:
            print("Não foi possível salvar o histórico.")

    def confirmar(self, mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta in ("s", "n"):
                return resposta == "s"
            print("Responda s ou n.")

    def tem_dado_pessoal(self, texto):
        digitos = sum(1 for c in texto if c.isdigit())
        return digitos >= 8 or "@" in texto

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou,
                  tentativas, tempo):
        self.historico.append({
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo": tempo,
            "nota": None,
        })
        self.registros_sessao += 1
        self.salvar_historico()

    def perguntar(self):
        tentativas = 0
        inicio = time.time()
        while True:
            texto = input("\nDigite sua dúvida (0 para voltar): ").strip()
            if texto == "0":
                return
            if texto == "":
                print("Digite sua dúvida.")
                continue
            if self.tem_dado_pessoal(texto):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            categoria = self.base.achar_categoria(texto)
            if categoria:
                self.navegar_categoria(categoria)
                tentativas = 0
                inicio = time.time()
                continue

            tentativas += 1
            resultados = self.base.buscar(texto)

            if not resultados or resultados[0][0] < 3:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras ou digite o nome de uma categoria:")
                for categoria in self.base.categorias():
                    print("  -", categoria)
                tempo = round(time.time() - inicio, 1)
                self.registrar("pergunta", texto, None, False, False,
                               tentativas, tempo)
                continue

            pontos, melhor = resultados[0]
            confianca = "ALTA" if pontos >= 6 else "MÉDIA"
            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)\n")
            melhor.exibir()

            alternativas = [o for p, o in resultados[1:3] if p >= 3]
            if alternativas:
                print("\nTalvez também ajude:")
                for o in alternativas:
                    print("  -", o.titulo)

            ajudou = self.confirmar("\nEssa orientação respondeu sua dúvida? (s/n): ")
            tempo = round(time.time() - inicio, 1)
            self.registrar("pergunta", texto, melhor.id, True, ajudou,
                           tentativas, tempo)
            if ajudou:
                print("Que bom que ajudou!")
                tentativas = 0
                inicio = time.time()
            else:
                print("Sinto muito. Reescreva sua dúvida com outras palavras.")

    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("Nenhuma categoria disponível.")
            return
        while True:
            print("\nCategorias:")
            for i, categoria in enumerate(categorias, 1):
                print(f"{i} - {categoria}")
            print("0 - Voltar")
            opcao = input("Escolha: ").strip()
            if opcao == "0":
                return
            if not opcao.isdigit() or not 1 <= int(opcao) <= len(categorias):
                print("Opção inválida.")
                continue
            self.navegar_categoria(categorias[int(opcao) - 1])

    def navegar_categoria(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        inicio = time.time()
        while True:
            print(f"\n{categoria}:")
            for i, o in enumerate(orientacoes, 1):
                print(f"{i} - {o.titulo}")
            print("0 - Voltar")
            opcao = input("Escolha: ").strip()
            if opcao == "0":
                return
            if not opcao.isdigit() or not 1 <= int(opcao) <= len(orientacoes):
                print("Opção inválida.")
                continue
            escolhida = orientacoes[int(opcao) - 1]
            print()
            escolhida.exibir()
            ajudou = self.confirmar("\nEssa orientação respondeu sua dúvida? (s/n): ")
            tempo = round(time.time() - inicio, 1)
            self.registrar("categoria", "", escolhida.id, True, ajudou, 1, tempo)
            if ajudou:
                print("Que bom que ajudou!")
            else:
                print("Sinto muito que não ajudou.")
                if self.confirmar("Quer escrever sua dúvida com suas palavras? (s/n): "):
                    self.perguntar()
            inicio = time.time()

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("\nAinda não há atendimentos.")
            return
        encontrados = [h for h in self.historico if h["encontrou"]]
        ajudaram = [h for h in self.historico if h["ajudou"]]
        notas = [h["nota"] for h in self.historico if h.get("nota")]
        tempo_medio = sum(h["tempo"] for h in encontrados) / len(encontrados) if encontrados else 0
        tentativas = sum(h["tentativas"] for h in self.historico) / total
        facilidade = sum(notas) / len(notas) if notas else 0
        sem_solucao = []
        for h in self.historico:
            if h["pergunta"] and not h["ajudou"] and h["pergunta"] not in sem_solucao:
                sem_solucao.append(h["pergunta"])

        print("\n=== Indicadores ===")
        print(f"Atendimentos: {total}")
        print(f"Resposta encontrada: {len(encontrados) / total * 100:.1f}%")
        print(f"Taxa de acerto (ajudou): {len(ajudaram) / total * 100:.1f}%")
        print(f"Tempo médio para encontrar: {tempo_medio:.1f} s")
        print(f"Tentativas por atendimento: {tentativas:.1f}")
        print(f"Facilidade de uso (1 a 5): {facilidade:.1f}")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for pergunta in sem_solucao:
                print("  -", pergunta)
        else:
            print("  - Nenhuma")

    def exportar_csv(self):
        try:
            os.makedirs("data", exist_ok=True)
            with open(CAMINHO_CSV, "w", newline="", encoding="utf-8") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)
                escritor.writeheader()
                for h in self.historico:
                    escritor.writerow({campo: h.get(campo) for campo in CAMPOS})
            print(f"CSV exportado em {CAMINHO_CSV}")
        except OSError:
            print("Não foi possível exportar o CSV.")

    def encerrar(self):
        if self.registros_sessao > 0:
            while True:
                nota = input("De 1 a 5, qual a facilidade de usar o assistente? ").strip()
                if nota.isdigit() and 1 <= int(nota) <= 5:
                    break
                print("Digite um número de 1 a 5.")
            self.historico[-1]["nota"] = int(nota)
            self.salvar_historico()
        self.exportar_csv()
        print("Até logo!")