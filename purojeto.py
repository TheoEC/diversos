import math
def Simplificador_de_equacoes(v):
    print('Simplifique sua equação booleana')
    x = v

    def montador_de_tabelas(n, resultado):
        l = [bin(numero)[2:] for numero in range(n)]       # faz uma lista com os a posição na tabela verdade em binario
        tabela_verdade = []
        for posi in range(n):                       # deixa todos os binarios com o mesmo tamanho e acrescenta a entrada no final de cada termo
            while len(l[posi]) != len(l[-1]):
                l[posi] = "0" + l[posi]
            v = l[posi] + resultado[posi]
            tabela_verdade.append(v)
        return (tabela_verdade)

    while True:                             # verifica se a entrada tem tamanho suficiente para montar a tabela
        if (math.log2(len(x))) % 1 == 0 and x.count('0') + x.count('1') + x.count('x') == len(x):
            quantidade_de_variaveis = int(math.log2(len(x)))
            n = quantidade_de_variaveis
            tabela_verdade_formatada = montador_de_tabelas(2 ** quantidade_de_variaveis, x)
            break
        else:
            print('Valor invalido, por favor digite novamente:')
            x = input()
    print(tabela_verdade_formatada)
    binarios = {x[0:len(x) - 1]: int(x[0:len(x) - 1], 2) for x in tabela_verdade_formatada}     # dicionario que salva os elementos da tabela com sua posição
    for valores in tabela_verdade_formatada:
        print(valores)

    grupos = [[] for qnt in range(n + 1)]  # Grupos de 1s
    exclusao = []
    for elementos in tabela_verdade_formatada:   # gera os implicantes que serão utilizados para serem permutados e formarem implicantes primos
        if elementos[-1] == '0':
            exclusao.append(elementos)
        else:
            grupos[elementos.count("1") + elementos.count("x") - 1].append(elementos[0:len(elementos) - 1])
    for elementos in exclusao:
        tabela_verdade_formatada.pop(tabela_verdade_formatada.index(elementos))

    print('Selecionada:', tabela_verdade_formatada)

    for vazios in grupos:                    # Filtro de grupos vazios
        if len(vazios) == 0:
            grupos.pop(grupos.index(vazios))
    relacao_de_grupos = [[] for qnt in range(len(grupos) - 1)]
    print('\n' + 'Grupos:', '\n', grupos)

    def posicao(j):
        pos = []                # verifica a posição de " _ " nos implicantes
        x = [k for k in j]
        d = 0
        for p in x:
            if p == '_':
                pos.append(d)
            d += 1
        return pos

    implicantes_primos = []
    qtd = 1
    grupos = [x for j in grupos for x in j]

    def permutacao(implicante1, implicante2):  # gerador de implicantes atraves de comparações de outros implicantes
        implicante_final = ''
        for pos in range(n):
            if posicao(implicante1) == posicao(implicante2):
                if implicante1[pos] == implicante2[pos]:
                    implicante_final += implicante2[pos]
                else:
                    implicante_final += '_'
        return implicante_final

    posicao_dos_permutantes = {elementos[0:len(elementos) - 1]: str(int(elementos[0:len(elementos) - 1], 2)) for elementos in tabela_verdade_formatada}
    inter = binarios

    while len(grupos) > 1:              # gera so implicantes primos e os separam
        atualização_de_grupo = []
        for implicante1 in grupos:
            contador = 0
            for implicante2 in grupos:                # gera novos grupos de implicantes que futuramente serão permutados
                if implicante2 != implicante1:
                    implicante_final = permutacao(implicante1, implicante2)
                    posicao_dos_permutantes[implicante_final] = str(inter[implicante2]) + "," + str(inter[implicante1])
                    if implicante_final.count('_') == qtd and (implicante_final in atualização_de_grupo) == False:
                        atualização_de_grupo.append(implicante_final)
                        contador += 1
                    elif implicante_final.count('_') == qtd:
                        contador += 1
            if contador == 0:                # seleciona os implicantes primos
                implicantes_primos.append(implicante1)
        qtd += 1
        inter = posicao_dos_permutantes
        if len(atualização_de_grupo) == 0:
            break
        grupos = atualização_de_grupo
    for implicante in grupos:                                # adiciona o ultimo grupo formado na lista de implicantes primos
        if (implicante in implicantes_primos) == False:
            implicantes_primos.append(implicante)
    print("implicantes primos", implicantes_primos)

    for implicante in implicantes_primos:             # forma uma lista com os numeros que serão colunas na tabela
        print(implicante, ':', posicao_dos_permutantes[implicante])
    tamanho_da_tabela = [tamanho for tamanho in range(2 ** quantidade_de_variaveis) if montador_de_tabelas(2 ** quantidade_de_variaveis, x)[tamanho][-1] == "1"]

    def lista_de_implicantes(a):    # gera os implicantes permutados repetindo os termos iguais e trocando os diferentes por " _ "
        str1 = []
        valores = posicao_dos_permutantes[a].split(',')
        novalista = [tamanho_da_tabela.index(int(numeros)) for numeros in valores if (int(numeros) in tamanho_da_tabela) == True]
        for tamanho in range(len(tamanho_da_tabela)):
            if (tamanho in novalista) == True:
                str1 += '0'
            else:
                str1 += '-'
        return str1

    for i in implicantes_primos:             # monta a tabela e faz um dicionario dos implicantes e sua linha na tabela
        if lista_de_implicantes(i).count("0") != 0:
            print(i, lista_de_implicantes(i), posicao_dos_permutantes[i])
    matriz_de_implicantes = [lista_de_implicantes(i) for i in implicantes_primos if lista_de_implicantes(i).count("0") != 0]
    dic_de_implicantes = {i: lista_de_implicantes(i) for i in implicantes_primos if lista_de_implicantes(i).count("0") != 0}
    print(dic_de_implicantes)

    def verificar(m=[], dic={}):              # verifica linhas aonde um dos zeros está sozinho na coluna
        l = [j for i in m for j in range(len(i)) if i[j] == "0"]
        return [z for z in set([b[0] for b in dic.items() for c in [b for a in l if l.count(a) == 1 for b in m if b[a] == "0"] if(c in [a for a in b]) == True])]

    print(verificar(matriz_de_implicantes, dic_de_implicantes))
    l = [verificar(matriz_de_implicantes, dic_de_implicantes)]
    possiveis_variaveis = ["A", "B", "C", "D", "E", "F", "G", "H"]

    def equacao(l=[]):                       # forma a equação booleana baseada nos implicantes
        eq = ""
        for i in l:
            for j in range(len(i)):
                if i[j] == "0":
                    eq += possiveis_variaveis[j].lower() + "'"
                elif i[j] == "1":
                    eq += possiveis_variaveis[j]
            if i == l[-1]:
                break
            eq += " + "
        return eq
    print(equacao(l[0])+"\n")

    def redutor_tabela(m=[]):               # monta a tabela reduzida e faz um dicionario dos implicantes e sua nova linha
        um_zero = [a for a in [j for i in m for j in range(len(i)) if i[j] == "0"] if
                   [j for i in m for j in range(len(i)) if i[j] == "0"].count(a) == 1]
        zeros_na_linha_de_um_zero = [f for f in set(
            [b for z in um_zero for a in m if a[z] == "0" for b in range(len(a)) if a[b] == "0" and b != z])]
        reduzida = []
        implicantes = []
        lista_colunas_excluidas = sorted(set([j for i in [um_zero, zeros_na_linha_de_um_zero] for j in i]))
        for w in m:                    # diminui a tabela excluindo as colunas
            cont = 0
            for q in um_zero:
                if w[q] == "0":
                    cont += 1
            if cont == 0:
                implicantes.append([b[0] for b in dic_de_implicantes.items() if (w in [a for a in b]) == True])
                for n in lista_colunas_excluidas[::-1]:
                    w.pop(n)
                reduzida.append(w)
        dic_imp = {c: reduzida[b] for b in range(len(implicantes)) for c in implicantes[b]}
        excluidos = []
        comparados = []
        if um_zero != []:        # seleciona os termos a serem passados para a nova tabela
            for i in range(len(reduzida)):
                for j in range(len(reduzida)):
                    cont = 0
                    di = [[b for b in dic_imp.items()][i]]
                    di2 = [[b for b in dic_imp.items()][j]]
                    if reduzida[i] != reduzida[j] and i != j:
                        for a in range(len(reduzida[j])):
                            x=reduzida[i],reduzida[j]
                            if reduzida[j][a] == reduzida[i][a] and reduzida[j][a] == "0":
                                cont += 1
                        if cont == reduzida[j].count("0"):
                            excluidos.append(j)
                    elif reduzida[i] == reduzida[j] and (str(i) + str(j) in comparados) == False and (str(j) + str(i) in comparados) == False:
                        if i != j and di[0][0].count("_") < di2[0][0].count("_"):
                            excluidos.append(i)
                        elif i != j:
                            excluidos.append(j)
                    comparados.append(str(i) + str(j))
            num = [[j for j in dic_imp.items()][i][0] for i in excluidos]
            for z in sorted(set(excluidos))[::-1]:
                reduzida.pop(z)
                del dic_imp[num[excluidos.index(z)]]
            print("reduzida:")
            for i in range(len(reduzida)):
                print([b for b in dic_imp.items()][i][0],reduzida[i])
            print(dic_imp)
        return reduzida, dic_imp

    def regras_simpli(lista=[]):                # simplifica a expressão atraves das:
        for i in range(len(lista)):             # regras de simplificação:
            new_str = ''                        # XX = X
            for j in lista[i]:                  # X + XY = X
                if (j in new_str) == False:
                    new_str += j
            lista[i] = new_str
        menor = [b for b in lista if len(b) == sorted([len(i) for i in lista])[0]]
        print('menor qnt', menor)
        for b in range(len(lista)):
            for i in menor:
                cont=0
                for j in i:
                    if (j in lista[b])==True:
                        cont+=1
                if cont==len(i):
                    lista[b]=i
        print("simplificado", sorted(set(lista)))
        return sorted(set(lista))

    def permutas(n=[], n2=[]):              # gera os novos termos da expessão permutada
        l = []
        print("\n"+'serão permutados', n, n2,"\n")
        for i in n:
            for j in n2:
                eq2 = str(i) + str(j)
                eq = sorted([i for i in eq2])
                l.append(''.join(eq))
        print("expressão permutada", l)
        j = regras_simpli(l)
        return j

    def petrick(l={}):           # usa o metodo de petrick pera simplificar equações
        print("metodo de Petrick "+"\n")
        m = [i[1] for i in l.items()]
        termos=[i[0] for i in l.items()]
        numeros=["A","B","C","D","E","F","G"]
        numeros2=[10,11,12,13,14,15,16]
        for a in range(len(m)):
            print(termos[a],m[a])
        new_m = []
        for i in range(len(m[0])):          # gera os termos a serem permutados
            new_ime = []
            for b in range(len(m)):
                if m[b][i] == '0' and b<10:
                    new_ime.append(b)
                elif m[b][i]=="0" and b>=10:
                    new_ime.append(numeros[int(str(b)[1])])
            new_m.append(new_ime)
        print(new_m)
        while len(new_m) != 1:              # seleciona os termos a serem permutados
            p = []
            for a in range(0, len(new_m), 2):
                try:
                    p.append(permutas(new_m[a], new_m[a + 1]))
                except:
                    p.append(new_m[-1])
                    break
            new_m = [i for i in p]
        print("\n"+"equação final",new_m[0])
        menores=[b for b in new_m[0] if len(b)==sorted([len(a)for a in new_m[0]])[0]]
        print("\n"+"menores termos",menores)
        menores2=[]
        for a in menores[0]:
            if (a in numeros)==True:
                menores2.append(str(numeros2[numeros.index(a)]))
            else:
                menores2.append(a)
        print("selecionado",menores2)
        impli=[termos[a] for a in range(len(termos)) if (str(a) in menores2)==True]
        print("\n"+"implicantes para a equação",impli)
        return impli

    while True:                 # forma todas as tabelas reduzidas e verifica se o metodo de petrick é necessario
        matriz_nova = redutor_tabela(matriz_de_implicantes)
        if matriz_nova[0] == [] or matriz_nova[0] == [[]]:
            break
        elif matriz_nova[0] == matriz_de_implicantes:
            l.append(petrick(matriz_nova[1]))
            break
        l.append(verificar(matriz_nova[0], matriz_nova[1]))
        print(verificar(matriz_nova[0], matriz_nova[1]),"\n")
        matriz_de_implicantes = matriz_nova[0]
        dic_de_implicantes = matriz_nova[1]

    l = [b for a in l for b in a]
    print('\n'+equacao(l))

def faz_sincrono(v):
    Qtd_de_flip_flops = 0
    for i in v:
        if int(i) > Qtd_de_flip_flops:
            Qtd_de_flip_flops = int(i)

    def faz_bin(x, limite):
        b = bin(int(x))[2:]
        while len(b) < int(limite):
            b ='0' + b
        return b

    print('certo ate aqui')
    tabela_binarios = []

    for i in v:
        tabela_binarios.append(faz_bin(i, Qtd_de_flip_flops))
    for i in tabela_binarios:
        print(i)

    for i in range(Qtd_de_flip_flops):
        variaveis = []
        for b in range(len(v)):
            valor = tabela_binarios[v][i]
            if b = 
            valor_dois

faz_sincrono('0123')
