import random


def gerador_senha_super_seguro() -> str:
    frutas = ['mamao', 'kiwi', 'abacaxi']
    cores = ['azul', 'vermelho', 'amarelo']
    numeros = ['1', '2', '3']
    caracteres_especiais = ['!', '@', '#']
    
    fruta = random.choice(frutas)
    cor = random.choice(cores)
    numero = random.choice(numeros)
    caracter = random.choice(caracteres_especiais)
    
    return fruta + cor + numero + caracter