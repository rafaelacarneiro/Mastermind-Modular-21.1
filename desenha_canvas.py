'''
Autores:    Daniel Peralta (1811442)
            Felipe Meiga (2011460)
            Rafaela Carneiro (2011483)
'''

from tkinter import *
import random

'''def iniciar_novo_jogo():    # abre uma janela para o usuario escolher entre os niveis I, II e III
    janela = Tk()
    janela.geometry('300x250')
    janela.config(bg='white')
    msg = Label(janela,bg='white',text='Escolha o nível da próxima partida',font='Courier 10 bold')
    msg.pack()
    nivelI = Button(janela, bg='lightblue',text='I',font='Times 24 bold',width=3)
    nivelI.pack()
    nivelII = Button(janela, bg='lightblue',text='II',font='Times 24 bold',width=3)
    nivelII.pack()
    nivelIII = Button(janela, bg='lightblue',text='III',font='Times 24 bold',width=3)
    nivelIII.pack()
    return

def janela_inicial(habilitado=False):       # abre a janela inicial do jogo, onde o jogador escolhe iniciar uma nova partida ou continuar uma partida antiga
    ini = Tk()
    ini.geometry('400x200')
    ini.config(bg='white')
    l = Label(ini,bg='lightblue',text='BEM VINDO AO MASTERMIND',font='Courier 20 bold')
    l.pack()
    novoJogo = Button(ini,bg='lightpink',text='INICIAR NOVA PARTIDA',font='Courier 14 bold',command=iniciar_novo_jogo) # se o usuario escolher iniciar uma nova partida,
    #                                                                                                                   abre uma janela para a escolha do nivel
    novoJogo.pack()
    continuar = Button(ini,bg='lightpink',text='CONTINUAR PARTIDA ANTERIOR',font='Courier 14 bold',state='disabled')
    if habilitado:
        continuar['state']='normal'
    continuar.pack()
    mainloop()
    return'''

def mostra_senha(cnv,pedras,nivel,senha,xi=20,xf=50,teste=False):      # define a senha e monta ela na parte de cima do tabuleiro(onde fica a senha escondida durante o jogo)
    '''lCores = ['red','green','blue','yellow','pink','cyan'] # cores disponiveis para o nivel 1
    if nivel != 1:                                          # se nao for o nivel 1, tera mais cores
        lCores.append('brown')
        if nivel == 3:
            lCores.append('purple')
    if teste==True:                                 #essa parte da funcao é usada apenas para fazer os testes unitarios
        for cont in range(pedras):
            cor = input('Entre com uma cor para montar a senha ')
            o = cnv.create_oval(xi,20,xf,50,outline=cor,fill=cor)
            xi = xf+10
            xf = xi+30
        return'''
    #for cont in range(pedras):                      # define as cores da senha de forma aleatoria e posiciona o desenho
        #cor = random.choice(lCores)
    for cor in senha:
        o = cnv.create_oval(xi,20,xf,50,outline=cor,fill=cor)
        xi = xf+10
        xf = xi+30
    return 

def esqueleto(cnv,xi,yi,xf,yf,pedras,linhas):           # monta os retangulos para colocar as chaves e os resultados
    altura=yf-yi
    r = cnv.create_rectangle(5,yi,340,yf,outline='black',state='disabled')   # cria o primeiro retangulo
    for cont in range(pedras):                              # preenche o primeiro retangulo com a chave escondida
        o = cnv.create_oval(xi,20,xf,50,outline='grey',fill='grey')
        xi = xf+10
        xf = xi+30
    yi=yf
    yf+=altura
    cont=0
    while cont < linhas:                                    #cria os retangulos restantes
        r = cnv.create_rectangle(5,yi,270,yf,outline='black',state='disabled')
        q = cnv.create_rectangle(270,yi,340,yf,outline='black',state='disabled') 
        yi=yf
        yf+=altura
        cont+=1
    global fim_tab
    fim_tab=yf-altura                                       #coordenada y do final do tabuleiro, vai ser usada na funcao paleta_de_cores()
    return

def circulos(cnv,xi,yi,xf,yf,pedras,linhas):        #coloca os circulos em cada linha do tabuleiro
    const_xi = xi
    const_xf = xf
    i=0
    while i<linhas:
        for cont in range(pedras):
            o = cnv.create_oval(xi,yi,xf,yf,outline='grey',fill='white')
            xi = xf+10
            xf = xi+30
        xi = const_xi
        xf = const_xf
        yi=yf+20
        yf=yi+30
        i+=1
    return

def paleta_de_cores(cnv,xi,xf,nivel):               # monta a paleta de cores
    lCores = ['red','green','blue','yellow','pink','cyan'] #cores disponiveis no nivel 1
    if nivel != 1:                                          # se nao for nivel 1, acrescenta cor(es)
        lCores.append('brown')
        if nivel == 3:
            lCores.append('purple')
    i=0
    cont=0
    yi = fim_tab+10         # a paleta de cores vai ser posicinada abaixo do final do tabuleiro
    yf = yi+30
    while cont < len(lCores):   # define a paleta e posiciona
        o = cnv.create_oval(xi,yi,xf,yf,outline=lCores[i],fill=lCores[i])
        xi=xf+10
        xf=xi+30
        i+=1
        cont+=1
    return yf       # retorna a ordenada final, usada para posicionar o botao de checagem da chave

'''def menu(top):
    princi = Menu(top)
    opcoes=Menu(princi)
    opcoes.add_command(label='Voltar a janela inicial',command=lambda:[top.destroy(),janela_inicial(True)]) #qnd o usuario sair do jogo pelo menu, a opcao de continuar 
    princi.add_cascade(label='Opcoes',menu=opcoes)                                                      # partida anterior fica habilitada na janela inicial
    top.configure(menu=princi)
    return'''

'''def monta_tabuleiro(nivel, lim, pedras):    # monta todo o tabuleiro, utilizando as funçoes acima
    tabuleiro = Tk()
    tabuleiro.title('Nivel '+str(nivel))
    tabuleiro.geometry('345x800')
    menu(tabuleiro)
    cnv = Canvas(tabuleiro,width=345,height=700)
    cnv.pack()
    senha(cnv,20,50,pedras,nivel)
    esqueleto(cnv,20,10,50,60,pedras,lim)
    yf = paleta_de_cores(cnv,20,50,nivel)
    circulos(cnv,20,70,50,100,pedras,lim)
    checar = Button(tabuleiro,text="Checar",bg='orange',font='Courier 24 bold',state='disabled')    # botao para o usuario testar uma chave
    checar.place(x=100,y=yf+4)      # posiciona o botao abaixo da paleta de cores
    return'''

def monta_tabuleiro(nivel, lim, pedras,cnv,tab):    # monta todo o tabuleiro, utilizando as funçoes acima
    #senha(cnv,20,50,pedras,nivel)
    #menu(tab)
    esqueleto(cnv,20,10,50,60,pedras,lim)
    yf = paleta_de_cores(cnv,20,50,nivel)
    circulos(cnv,20,70,50,100,pedras,lim)
    checar = Button(tab,text="Checar",bg='orange',font='Courier 24 bold',state='disabled')    # botao para o usuario testar uma chave
    checar.place(x=100,y=yf+4)      # posiciona o botao abaixo da paleta de cores
    return checar

def attemptResult(cnv,pretas,brancas,linha,final_tab):
    xi=280
    yi=final_tab-35
    yi-=linha*50
    for i in range(pretas):
        if i==4:
            yi+=15
            xi=280
        o = cnv.create_oval(xi,yi,xi+10,yi+10,outline='black',fill='black',state='disabled')
        xi+=15
    for j in range(brancas):
        if j==4 or j+i==3:
            yi+=15
            xi=280
        o = cnv.create_oval(xi,yi,xi+10,yi+10,fill='white',state='disabled')
        xi+=15
    cnv.pack()
    return
    
        


    















