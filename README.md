# Citizen Assist AI

Assistente de terminal em Python que orienta pessoas idosas sobre serviços públicos, usando só informações de fontes oficiais. Projeto da Global Solution 2026.2 (Pensamento Computacional e Automação com Python, FIAP).

## Integrantes

| Nome | RM |
|------|----|
| Felipe Mello Ramalho Cagnin | 569237 |

Trabalho individual.

## Público e problema

**Público:** pessoas idosas (60 anos ou mais).

**Problema:** a informação sobre Cartão SUS, vacinas, remédios, direitos e denúncia existe, mas está espalhada, em linguagem técnica e misturada com sites que parecem oficiais e não são.

**Solução:** o assistente responde dúvidas digitadas ou escolhidas por categoria e sempre mostra a fonte, a data de verificação e o aviso de que não é um canal oficial. Ele não pede nem registra dados pessoais.

## ODS relacionados

- **ODS 3:** Saúde e Bem-Estar
- **ODS 10:** Redução das Desigualdades
- **ODS 16:** Paz, Justiça e Instituições Eficazes

## Como executar

Requisito: Python 3, sem bibliotecas externas.

1. Baixe ou clone o repositório.
2. Abra o terminal dentro da pasta do projeto.
3. Execute:

```
python main.py
```

Menu: 1 pergunta, 2 navegar por categorias, 3 indicadores, 4 exportar CSV, 0 sair. Ao sair, o assistente pede uma nota de facilidade de 1 a 5 e exporta o CSV.

## O código em resumo

| Arquivo | O que faz |
|---------|-----------|
| `main.py` | Cria a base e o assistente e mostra o menu |
| `orientacao.py` | Classe `Orientacao`: guarda os dados de uma orientação e a exibe na tela |
| `base_conhecimento.py` | Classe `BaseConhecimento`: lê o JSON, lista categorias, pontua e busca |
| `assistente.py` | Classe `Assistente`: faz o atendimento, guarda o histórico, calcula indicadores e exporta o CSV |
| `data/base_conhecimento.json` | Base com 10 orientações em 4 categorias (Saúde, Direitos, Benefícios e Acesso digital) |
| `data/historico.json` | Gerado pelo programa: um registro por atendimento |
| `data/atendimentos.csv` | Gerado pelo programa: histórico exportado com `csv.DictWriter` |

As classes se encaixam por composição: o `Assistente` tem uma `BaseConhecimento`, que tem uma lista de objetos `Orientacao`.

**Regras de atendimento:**
- Entradas inválidas (opção fora da faixa, letras, resposta vazia, s/n inválido) não encerram o programa.
- Pergunta com 8 ou mais dígitos ou com `@` é recusada e não é registrada.
- JSON ausente ou corrompido não trava o programa.
- Se o texto digitado for o nome de uma categoria, o assistente abre a lista dela.

**Indicadores calculados:** resposta encontrada (%), taxa de acerto (%), tempo médio para encontrar, tentativas por atendimento, facilidade de uso (1 a 5) e lista de dúvidas sem solução.

## Regra de pontuação

A pergunta, as palavras-chave e o título são normalizados (minúsculas, sem acentos e sem pontuação) e comparados pelas 6 primeiras letras de cada palavra (o radical). Isso permite entender plural e variações, como "beneficios" e "beneficio".

| Regra | Resultado |
|-------|-----------|
| Palavra-chave da orientação aparece na pergunta | +3 pontos |
| Palavra da pergunta (4 letras ou mais) aparece no título | +1 ponto |
| Melhor orientação com 6 pontos ou mais | Confiança ALTA |
| Melhor orientação com 3 a 5 pontos | Confiança MÉDIA |
| Nenhuma orientação com 3 pontos | "Não encontrei" e sugestão de categorias |

`buscar()` devolve uma lista de tuplas `(pontos, orientacao)`, da maior para a menor pontuação. O assistente mostra a melhor orientação e até duas alternativas com pelo menos 3 pontos.

**Exemplo:** em "Como faço o cartão do SUS?", a orientação 1 recebe +3 por "cartao do sus", +3 por "sus" e +1 porque "cartão" está no título: 7 pontos, confiança ALTA.

## Integrações com outras disciplinas

Não há.

## Fontes consultadas

Cada orientação da base guarda a fonte e a data de verificação (12/11/2026).

| Id | Tema | Fonte |
|----|------|-------|
| 1 | Cartão SUS | https://www.gov.br/saude/pt-br/acesso-a-informacao/faq/tematicos-e-outros/como-conseguir-o-cartao-sus |
| 2 | Vacinação da pessoa idosa | https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/s/saude-da-pessoa-idosa/vacinacao-da-pessoa-idosa |
| 3 | Farmácia Popular | https://www.gov.br/saude/pt-br/assuntos/noticias/2024/julho/saiba-como-retirar-medicamentos-e-outros-itens-pelo-farmacia-popular |
| 4 | Transporte gratuito | https://bilheteunico.sptrans.com.br/especial/pessoa-idosa/ |
| 5 | Atendimento prioritário | https://www.planalto.gov.br/ccivil_03/leis/l10048.htm |
| 6 | Denúncia de violência (Disque 100) | https://www.gov.br/mdh/pt-br/assuntos/noticias/2026/defeso-eleitoral/agosto/voce-sabe-como-denunciar-a-violencia-contra-pessoas-idosas |
| 7 | BPC | https://www.gov.br/pt-br/servicos/solicitar-beneficio-assistencial-ao-idoso |
| 8 | Meu INSS | https://www.gov.br/pt-br/temas/meu-inss |
| 9 | CadÚnico | https://www.gov.br/pt-br/servicos/inscrever-se-no-cadastro-unico-para-programas-sociais-do-governo-federal |
| 10 | Conta gov.br | https://www.gov.br/pt-br/servicos/criar-sua-conta-gov.br |

## Teste com usuários

O teste foi feito com 3 pessoas de fora da equipe, somando **13 atendimentos** (7 por pergunta e 6 por navegação em categorias), em 13/11/2026. Nenhum nome ou dado dessas pessoas foi registrado.

| Indicador | Resultado |
|-----------|-----------|
| Resposta encontrada | 84,6% (11 de 13) |
| Taxa de acerto (ajudou) | 84,6% (11 de 13) |
| Tempo médio para encontrar | 19,8 s |
| Tentativas por atendimento | 1,0 |
| Facilidade de uso (1 a 5) | 5,0 |

**Dúvidas sem solução:**
- "quero transporte de graça"
- "bom dia"

**O que o teste mostrou:** todos os 6 atendimentos por categoria deram certo. Entre as 7 perguntas digitadas, 5 foram encontradas e 2 não. A pergunta "bom dia" é uma saudação fora do assunto da base. Já "quero transporte de graça" é uma dúvida real que não foi encontrada, porque a orientação de transporte só tinha as palavras-chave "transporte gratuito", "onibus", "gratuidade", "passe livre" e "passagem", e a pergunta recebeu só 2 pontos.

**Melhoria feita a partir do teste:** foi adicionada a palavra-chave "transporte" à orientação de transporte gratuito (id 4). Com ela, a pergunta "quero transporte de graça" passa a ser encontrada, com 5 pontos e confiança MÉDIA.

## Limitações

- A busca compara apenas o início das palavras. Sinônimos só são encontrados se estiverem nas palavras-chave, como mostrou o teste com "transporte de graça".
- O assistente não responde saudações nem assuntos fora da base.
- A base tem 10 orientações e cobre só parte das dúvidas de pessoas idosas.
- A orientação de transporte gratuito segue as regras da cidade de São Paulo. Em outras cidades, as regras e os locais de atendimento podem ser diferentes.
- As informações podem mudar com o tempo. Cada orientação mostra a data em que foi conferida.
- O assistente não é um canal oficial e não substitui o atendimento dos órgãos públicos.

## Vídeo técnico

https://youtu.be/U9AXOyt7jlw?si=8yThaXUsHToul1Km
