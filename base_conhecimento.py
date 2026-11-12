import json
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


def radical(palavra):
    return palavra[:6]


def radicais(texto):
    palavras = normalizar(texto).split()
    return " " + " ".join(radical(p) for p in palavras) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self.orientacoes = [Orientacao(**d) for d in dados]
        except (OSError, json.JSONDecodeError, TypeError):
            print("Atenção: base de conhecimento ausente ou inválida.")
            self.orientacoes = []

    def categorias(self):
        return sorted(set(o.categoria for o in self.orientacoes))

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def achar_categoria(self, texto):
        for categoria in self.categorias():
            if radicais(texto) == radicais(categoria):
                return categoria
        return None

    def pontuar(self, pergunta, orientacao):
        palavras = normalizar(pergunta).split()
        pergunta_rad = radicais(pergunta)
        titulo_rad = radicais(orientacao.titulo)
        pontos = 0
        for palavra in orientacao.palavras_chave:
            if radicais(palavra) in pergunta_rad:
                pontos += 3
        for palavra in set(palavras):
            if len(palavra) >= 4 and " " + radical(palavra) + " " in titulo_rad:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda t: t[0], reverse=True)
        return resultados