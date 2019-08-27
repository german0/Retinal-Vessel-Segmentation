import numpy as np
import pathlib
from pylab import *
from datetime import datetime
import mahotas

##################################### CALCULO DAS LINHAS ##############################################

'''binarização da imagem'''
def binarization(im, x, y, window):
    N, M = im.shape
    r = zeros_like(im)
    wx, wy = (int(N / x), int(M / y))
    aux = zeros((wx, wy))
    if (window == 1):
        for i in range(0, x):
            for j in range(0, y):
                aux = im[i * wx:(i + 1) * wx, j * wy:(j + 1) * wy]
                photo = aux.astype(np.uint8)
                T_otsu = mahotas.otsu(photo)
                binary = photo > T_otsu
                r[i * wx:(i + 1) * wx, j * wy:(j + 1) * wy] = binary
    else:
        photo = im.astype(np.uint8)
        T_otsu = mahotas.otsu(photo)
        r = photo > T_otsu
    return r


'''coloca as intensidades entre 0 e 255'''
def threshold(value):
    return 0 if (value < 0) else (255 if (value > 255) else int(value))


'''inverte as cores de uma imagem em niveis de cinzento'''
def invert_image(image):
    return 255 - image


'''cálculo do ponto inverso a um ponto dado'''
def inverse_point(x, y, half):
    difx = half - x
    dify = y - half
    return half + difx, half - dify


'''função de cálculo da reta ortogonal'''
def compute_inverse(array, size):
    inverted = []
    for coordx, coordy in array:
        inverted.append((size - 1 - coordx, coordy))
    return inverted


'''função que completa a linha desenhada'''
def complete_line(array, size):
    new = []
    final = []
    inverse = []
    half = round((size - 1) / 2)
    # obter valores da inversa
    # atualizar valores do array
    for coordx, coordy in array:
        newx, newy = coordx, coordy + half
        new.append((newx, newy))
        inverse = inverse_point(newx, newy, half)
        if inverse not in new:
            new.append(inverse)
    return new


'''função de desenho das retas (para teste)'''
def draw_line(array, size):
    matrix = zeros((size, size))
    for coordx, coordy in array:
        matrix[coordx, coordy] = 1
    imshow(matrix * 255)
    figure()


'''transforma graus em radianos'''
def toRadian(angle):
    return ((angle * math.pi) / 180)


'''transforma inclinações em declives'''
def getDeclive(angle):
    return 0 if ((angle % 180) == 0) else math.tan(toRadian(angle))


'''descoberna das inclinações necessárias para o primeiro quadrante'''
def slope():
    angle = 90 / 6
    incline = []
    number = 1
    i = 0
    while (i <= 90):
        incline.append(i)
        i += angle
        number += 1
    return incline


'''cálculo dos pontos x,y que intersetam os limites da janela, limitando a reta'''
def limits(angle, size):
    m = getDeclive(angle)
    if (angle >= 0 and angle <= 45):  # interseta a primeira metade (lado direito) do 1ºquadrante
        x = size
        y = m * x
    else:
        y = size
        x = y / m
    return round(x), round(y)


'''algoritmo de bresenham, para decidir que pixel pintar'''
def bresenham(angle, size, x0, y0, x1, y1):
    declive = getDeclive(angle)
    # array correspondente aos pixeis pertencentes ao desenho da linha
    matrix = []
    x, y = x0, y0
    dx = x1 - x0
    dy = y1 - y0
    if (angle <= 45):
        # variável de dermina a direção do passo
        fault_value = dx / 2
        matrix.append((size - 1 - x, y))
        # dar um passo em y (variável y na matriz)
        y += 1
        while (y < x1):
            fault_value -= dy
            # caso o fault_value <0 dar um passo em direção a y
            if fault_value < 0:
                x += 1
                fault_value += dx
                matrix.append((size - 1 - x, y))
            # caso o fault_value >0 dar um passo em direção a x
            else:
                matrix.append((size - 1 - x, y))
            y += 1
    else:
        fault_value = dy / 2
        matrix.append((size - 1 - x, y))
        # dar um passo na direção do eixo y (size-x na matriz)
        x += 1
        while (x < y1):
            fault_value -= dx
            if fault_value < 0:
                y += 1
                fault_value += dy
                matrix.append((size - 1 - x, y))
            else:
                matrix.append((size - 1 - x, y))
            x += 1
    return matrix


'''Cálculo das ortogonais'''
def compute_ortogonal(lines):
    pos = 0
    ort_lines = []
    for line in lines:
        ort_pos = get_ortogonal(pos)
        ortogonal = lines[ort_pos][0:3]
        ort_lines.append(ortogonal)
        pos += 1
    return ort_lines


'''Cálculo das coordenadas de cada uma das linhas'''
def compute_lines(matrix_size):
    # array com coordenadas das linhas
    lines = []
    linesinv = []
    linesortogonal = []
    size = round(15 / 2)
    # angulos das retas com a parte positiva de x no primeiro quadrante
    inclines = slope()
    x0, y0 = (0, 0)
    for angle in inclines:
        matrix = zeros((matrix_size, matrix_size))
        x1, y1 = limits(angle, size)
        # matrix da imagem da linha, no primeiro quadrante
        frst_quadrant = bresenham(angle, size, x0, y0, x1, y1)
        # completar a linha
        complete = complete_line(frst_quadrant, matrix_size)
        lines.append(complete)
        if (angle != 0 and angle != 90):
            # retas complementares
            inverse = compute_inverse(complete, matrix_size)
            linesinv.append(inverse)
    lines += reversed(linesinv)
    linesortogonal = compute_ortogonal(lines)
    return lines, linesortogonal


##################################### CALCULO DO S E S0 ##############################################

'''cálculo do angulo ortogonal
ortogonal angles: 0 45 90 135
caso os angulos sejam 30, 45 ou 60, a ortogonal=135'''
def get_ortogonal(pos):
    # na matriz lines, as coordenadas das linhas estão em ordem desde os angulos 0 a 165
    # logo o angulo é dado pela posição das coordenandas da linha x15(incremento de angulo para angulo)
    angle = pos * 15
    ortogonal = angle

    # angulos do primeiro quadrante
    if angle == 30 or angle == 45 or angle == 60:
        return int(135 / 15)
    if angle == 15 or angle == 0:
        return int(90 / 15)
    if angle == 75 or angle == 90:
        return int(0 / 15)

    # angulos do segundo quadrante
    if angle == 120 or angle == 135 or angle == 150:
        return int(45 / 15)
    if angle == 105:
        return int(0 / 15)
    if angle == 165:
        return int(90 / 15)
        # retorna a posição da reta ortogonal
    return int(ortogonal / 15)


'''Média das intensidades de uma linha'''
# flag verifica se existem pixeis fora da borda
def average_line(image, line, ortogonal, mask, average, flag):
    avgline = 0
    avgort = 0
    size = len(line)
    # se a flag for 1 é necessário verificar se todos os pontos
    # da reta se encontram dentro da retina de modo a não efetuar cálculos desnecessários
    if flag == 1:
        for i in range(0, size):
            x1, y1 = line[i]
            if (i < len(ortogonal)):
                x2, y2 = ortogonal[i]
                avgort += image[x2, y2] if (mask[x2, y2] == 1) else average
            avgline += image[x1, y1] if (mask[x1, y1] == 1) else average
    else:
        # caso a flag seja 0 então todos os pontos da reta vão contar para a média
        for i in range(0, size):
            x1, y1 = line[i]
            if (i < len(ortogonal)):
                x2, y2 = ortogonal[i]
                avgort += image[x2, y2]
            avgline += image[x1, y1]
    return avgline / size, avgort / len(ortogonal)


'''Cálculo de L(i,j)'''
def compute_l(image, lines, ortogonal, mask):
    list_l = []
    list_lzero = []
    pos = 0
    n = average_window(image)
    # verifica se todos os pontos da imagem se encontram dentro da borda
    flag = verifica_imagem(mask)
    for line in lines:
        avg_l, avg_lzero = average_line(image, line, ortogonal[pos], mask, n, flag)
        list_l.append(avg_l)
        list_lzero.append(avg_lzero)
        pos += 1
    return n, max(list_l), max(list_lzero)


'''média de uma imagem'''
def average_window(image):
    return image.mean()


'''Verifica se existem pixeis fora da borda'''
def verifica_imagem(mask):
    flag = 0
    if 0 in mask:
        flag = 1
    return flag


'''Cálculo de S e S0'''
def greylevel_average(window_size, invimage, mask, lines, ortogonal):
    N, L = invimage.shape
    posx, posy = nonzero(mask > 0)
    elements = nonzero(mask)

    # Por exemplo, a direção ortogonal das orientações 30,45, and 60 é 135
    # 30+90= 120 45+90=135 60+90=150, o angulo principal mais próximo é 135
    s = zeros_like(invimage)
    szero = zeros_like(invimage)
    size = elements[0].size
    print("\nComputação do valor de Lij...")
    for k in range(0, size):
        x = elements[0][k]
        y = elements[1][k]
        # cálculo do n l(i,j) e l0(i,j)
        n, l_ij, lzero_ij = compute_l(invimage[x - 7:x + 8, y - 7:y + 8], lines, ortogonal,
                                      mask[x - 7:x + 8, y - 7:y + 8])

        # S(i,j)=L(i,j)-N
        s[x, y] = threshold(l_ij - n)
        szero[x, y] = threshold(lzero_ij - n)
    return s[7:7 + N, 7:7 + L], szero[7:7 + N, 7:7 + L]


##################################### MAIN ##############################################
def run():
    matrix_size = 15
    flag = '1'
    while (flag == '1'):
        flag = input("Carregar imagem[1] ou Sair[2]:")
        if (flag == '1'):
            try:
                diretoria = input("Diretoria da base de dados:")
                pasta = input("Training[1] ou Test[2]:")
                out = diretoria
                subpasta = ""

                if pasta == '1':
                    subpasta = "training"
                elif pasta == '2':
                    subpasta = "test"
                path = diretoria + "\\" + subpasta + "\\"

                imagename = input("Imagem (01_test):")
                imagepath = path + "images\\" + imagename + ".tif"
                maskpath = path + "mask\\" + imagename + "_mask.gif"
                pathlib.Path(out + "\\output_ricci").mkdir(parents=True, exist_ok=True)

                print("\nInicialização de variáveis e imagens ...")
                read = imread(imagepath)
                mask = imread(maskpath)
                image = read[:, :, 1]

                # adição de uma borda à imagem
                N, L = image.shape
                s = (N + 15, L + 15)
                border = zeros(s)
                rond = round(15 / 2)
                border[rond:(rond + N), rond:(rond + L)] = image

                border_mask = zeros_like(border)
                border_mask[rond:(rond + N), rond:(rond + L)] = mask

                print("Direitoria da imagem: " + imagepath)
                print("Diretoria com resultados: " + out + "\\output_ricci\\")

                print("\nCálculo das Linhas Especificadas ...")
                # cálculo das linhas input:tamanho da matriz de "desenho"
                lines, ortogonal = compute_lines(matrix_size)

                # inverter a imagem
                inverted_image = invert_image(border)

                print("\nCálculo de S e S0...")
                # cálculo de S e S0
                print("Início")
                start = datetime.now()
                s1, s2 = greylevel_average(matrix_size - 1, inverted_image, border_mask, lines, ortogonal)
                s1 = s1[rond:(rond + N), rond:(rond + L)]
                s2 = s2[rond:(rond + N), rond:(rond + L)]
                b = datetime.now()
                print("\nCálculo completo: " + str(b - start))
                print("Binarização da imagem por otsu...")
                binary = binarization(s1, 2, 2, 1)
                end = datetime.now()
                imsave(out + "\\output_ricci\\" + imagename + "S0_manual.tif", invert_image(s1), cmap='gray')
                imsave(out + "\\output_ricci\\" + imagename + "S1_manual.tif", invert_image(s2), cmap='gray')
                imsave(out + "\\output_ricci\\" + imagename + "binary_manual.tif", binary, cmap='gray')
                print("\nTempo Total: " + str(end - start))
                print("Imagens geradas...")
            except Exception as e:
                print(e)
                print("Imagem inválida...")
    print("Saída efetuada com sucesso.")

run()