import numpy as np


'''Neste primeiro caso o objetivo é fazer a soma cumulativa (1+2+3+...)'''

# Aqui está o exemplo sem nenhuma fução. 
# Se tiveres de usar esta operação muitas vezes tens de estar sempre a repetir 
# linhas de código e a mudar os números um a um
# Neste exemplo temos a soma entre 1 e 10 (10 + 1 porque se fosse só 10 ia ser entre 1 e 9)
lista = list(range(1, 10+1, 1))
soma = np.cumsum(lista)
print("Resultado:", soma[-1])


# Neste caso temos uma função que faz a mesma coisa das linhas acima
# Mas agora como é uma função é muito mais fácil usá-la repetidamente
def cumSum(min, max):
    lst = list(range(min, max+1, 1))
    cum_sum = np.cumsum(lst)
    output = cum_sum[-1]

# Aqui estamos a chamar a função e a fazer os cálculos entre 1 e 10
# Mas se correres só esta linha não te vai dar nada
cumSum(1, 10)


# Aqui temos a função de cima, mas esta tem o return
# O return permite-nos aceder ao resultado da função fora da função
def cumSum2(min, max):
    lst = list(range(min, max+1, 1))
    cum_sum = np.cumsum(lst)
    return cum_sum[-1]
# Aqui tu chamas a função e o "x" representa o return
# No return podes por aquilo que queres aceder fora da função
x = cumSum2(1, 10)
print("Resultado da função:", x)
# Aqui como consegues aceder ao resultado da função
# consegues fazer o que quiseres com esse resultado
# Exemplo:
y = x + x**x
print("y =", y)


'''Agora vamos supor que temos alguma necessidade mais "elaborada"
e precisamos de ter uma função que faça mais ações. Precisamos
também de conseguir aceder ao resultado dessas várias ações
para depois usar no código mais adiante'''

# Vamos usar como exemplo uma função que vai calcular quanto gastamos 
# em cada mês e quanto vai render o dinheiro que vamos poupar
# Na função abaixo, o restante é o que sobra ao fim do mês e a percent_poupada
# é a percentagem desse restante que investes
# Vamos assumir uma taxa de rentabilidade de 3%

def money(salário, restante, percent_poupada):
    gastos = salário - restante
    poupanca = percent_poupada/100 * restante
    capitalizacao = poupanca * 0.03
    return gastos, poupanca, capitalizacao
# Neste exemplo, a função dá return a três valores. 
# Podes dar quantos returns a quantas coisas quiseres. O objetivo é, basicamente,
# dar return a valores que vais precisar mais adiante

# Como há 3 returns, antes de chamar a função tens de definir 3 variáveis
# Cada variável representa um return e estas têm de ser definidas pela ordem 
# dos returns na função
dinheiro_gastp, dinehiro_poupado, dinheiro_capitalizado = money(2700, 770, 50)
print(f"\nForam gastos {dinheiro_gastp}€")
print(f"Foram poupados {dinehiro_poupado}€")
print(f"O dinheiro poupado rendeu {round(dinheiro_capitalizado, 2)}€")
# A partir daqui podes fazer o que bem quiseres com os valores a que deste return
# Exemplo:
if dinheiro_gastp > 700:
    print("\nAndas a gastar muito")

if dinheiro_capitalizado < 5:
    print("A investir assim não vais ter dinheiro para a reforma")

if dinehiro_poupado < 200:
    print("Gasta menos e poupa mais")


# Resumindo só quando não queres aceder a nada da função ao longo do código é que 
# não dás return
# Eu por exemplo tenho de aceder à câmara do PC ou do iPhone
# Posso fazer uma função para aceder a cada uma das câmaras
# Mas não preciso de fazer return a nada. só quero que o código aceda à câmara e pronto