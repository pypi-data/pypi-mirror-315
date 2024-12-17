def soma(*numeros):
    if len(numeros) == 0:
        raise ValueError("É necessário fornecer pelo menos um número.")
    return sum(numeros)


def subtracao(*numeros):
    if len(numeros) == 0:
        raise ValueError("É necessário fornecer pelo menos um número.")
    resultado = numeros[0]  # Primeiro número é a base inicial
    for numero in numeros[1:]:
        resultado -= numero  # Subtrai o próximo número
    return resultado


def multiplicacao(*numeros):
    if len(numeros) == 0:
        raise ValueError("É necessário fornecer pelo menos um número.")
    resultado = 1  # Começamos com 1, já que é o elemento neutro da multiplicação
    for numero in numeros:
        resultado *= numero  # Multiplica cada número pelo acumulado
    return resultado


def divisao(*numeros):
    if len(numeros) == 0:
        raise ValueError("É necessário fornecer pelo menos um número.")
    resultado = numeros[0]  # Primeiro número é o dividendo inicial
    for numero in numeros[1:]:
        if numero == 0:
            raise ZeroDivisionError("Não é possível dividir por zero.")
        resultado /= numero  # Divide pelo próximo número
    return resultado