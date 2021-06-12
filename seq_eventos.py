import desenha_canvas as draw
import regras_do_jogo as rules
from tkinter import *
from tkinter import messagebox

def menu(top):
    princi = Menu(top)
    opcoes=Menu(princi)
    opcoes.add_command(label='Sair sem salvar',command=exit)
    opcoes.add_command(label='Salvar e sair',command=lambda:[salvarPartida(progresso),exit])
    princi.add_cascade(label='Opcoes',menu=opcoes)
    top.configure(menu=princi)
    return

def changeState(btn,new_state):     # muda o estado de um botao
    btn['state']=new_state
    return

def abre_jogo(niv,lim,ped):
    global checar
    tab= Tk()
    tab.geometry('345x800')
    menu(tab)
    cnv = Canvas(tab,width=345,height=700)
    cnv.bind('<ButtonRelease-1>',funcao)
    checar = draw.monta_tabuleiro(niv,lim,ped,cnv,tab)
    cnv.pack()
    monta_tentativa()
    return
    
def defineVariables(n):         # 
    global nivel,lim,pedras,senha,progresso
    tupla = rules.escolha_do_nivel(n)
    nivel=tupla[0]
    lim=tupla[1]
    pedras=tupla[2]
    senha=rules.define_senha(nivel)
    progresso=[]
    return
        

def iniciar_novo_jogo():    # abre uma janela para o usuario escolher entre os niveis I, II e III e define as regras de acordo com o nivel escolhido pelo usuario
    janela = Tk()
    janela.geometry('300x250')
    janela.config(bg='white')
    msg = Label(janela,bg='white',text='Escolha o nível da próxima partida',font='Courier 10 bold')
    msg.pack()
    nivelI = Button(janela, bg='lightblue',text='I',font='Times 24 bold',width=3,command=lambda:[janela.destroy(),defineVariables(1),abre_jogo(nivel,lim,pedras)])
    nivelI.pack()
    nivelII = Button(janela, bg='lightblue',text='II',font='Times 24 bold',width=3,command=lambda:[janela.destroy(),defineVariables(2),abre_jogo(nivel,lim,pedras)])
    nivelII.pack()
    nivelIII = Button(janela, bg='lightblue',text='III',font='Times 24 bold',width=3,command=lambda:[janela.destroy(),defineVariables(3),abre_jogo(nivel,lim,pedras)])
    nivelIII.pack()
    return

def janela_inicial():       # abre a janela inicial do jogo, onde o jogador escolhe iniciar uma nova partida ou continuar uma partida antiga
    ini = Tk()
    ini.geometry('400x200')
    ini.config(bg='white')
    l = Label(ini,bg='lightblue',text='BEM VINDO AO MASTERMIND',font='Courier 20 bold')
    l.pack()
    novoJogo = Button(ini,bg='lightpink',text='INICIAR NOVA PARTIDA',font='Courier 14 bold',command=lambda:[ini.destroy(),iniciar_novo_jogo()]) # se o usuario escolher iniciar uma nova partida,
    #                                                                                                                   abre uma janela para a escolha do nivel
    novoJogo.pack()
    continuar = Button(ini,bg='lightpink',text='CONTINUAR PARTIDA ANTERIOR',font='Courier 14 bold',state='disabled',command=continuarPartida) #desabilitado na primeira jogada

    arq = open("jogo_salvo.txt","r")
    if arq.readline() != '':
        changeState(continuar,'normal')
    arq.close()

    continuar.pack()
    mainloop()
    
    return

def funcao(evento):
    x=evento.x
    y=evento.y
    
    global cor, yf_linha, yi_linha, attempts, final_tab

    attempts=len(progresso)             #qtd de tentativas ate entao = tamanho do vetor com o progresso

    

    final_tab = 450+100*(nivel-1)       #final do tabuleiro

    yf_linha=final_tab-50*attempts      #limites da linha do tabuleiro
    yi_linha=yf_linha-50                #para cada tentativa

    if y >= final_tab and y <= final_tab+40:        #limitando onde fica a paleta de cores
        cor = evento.widget.itemcget(CURRENT,'fill')
    
    if cor != '' and y<yf_linha and y>yi_linha:                 #limitando na linha da jogada atual
        evento.widget.itemconfig(CURRENT,fill=cor)
        xi_linha=20
        for i in range(pedras):             # procura em qual posicao foi colocada a pedra
            if xi_linha < x < xi_linha+35:
                break
            xi_linha+=40
        tentativa[i]=cor                #preenche o vetor com as tentativas na posicao em que foi colocado no canvas

        if 0 not in tentativa:          #se o vetor com as tentativas está preenchido de cores, habilita o botao para checar a chave
            changeState(checar,'normal')
            checar.configure(command=lambda:[rules.compara(tentativa,progresso),changeState(checar,'disabled'),monta_tentativa(),draw.attemptResult(evento.widget,progresso[-1][1][0],progresso[-1][1][1],attempts,final_tab),resultado(progresso,evento.widget)])
            
            

            
        # compara a chave c a senha, guarda a tentativa no vetor com o progresso, desabilita o botao ate a prox tentativa
                                                                                                                      
                                                                                                                                 
        #if len(progresso)==lim-1: # se so houver mais 1 tentativa disponivel, ao final dela a senha vai ser revelada
            #checar.configure(command=lambda:draw.mostra_senha(evento.widget,pedras,nivel,senha))
            
    return    
        
def monta_tentativa():          # vetor para armazenar cada chave
    global tentativa
    tentativa=[]
    for i in range(pedras):
        tentativa.append(0)
    return

def salvarPartida(progresso):
    arq = open("jogo_salvo.txt", "w")
    niv = len(progresso[0][0])-3        #nivel = qtd de pedras da tentativa - 3 
    arq.write(str(niv)+'\n')            # 1 linha do arquivo tem o nivel da partida
    for tent in progresso:              # escreve as cores de cada linha do tabuleiro e a qtd de pedras pretas e brancas (respectivamente) dessa linha
        for cor in tent[0]:
            arq.write(cor+';')
        arq.write(str(tent[1][0])+';'+str(tent[1][1]))
    arq.close()
    return

def continuarPartida():             # INCOMPLETA
    arq = open("jogo_salvo.txt","r")
    progr = []
    niv = arq.readline()        # nivel é a primeira linha do arquivo
    niv = int(niv)
    for linha in arq:
        lista = linha.split(';')
        #print(lista)
        tup = (lista[-2],lista[-1])     # pedras pretas e brancas
        lista.remove(tup[0])
        lista.remove(tup[1])
        progr.append([lista,tup])

    arq.close()

    defineVariables(niv)
    abre_jogo(nivel,lim,pedras)
    
    
    
    return 

def resultado(progresso,cnv): # envia mensagem ao final do jogo se ganhou ou perdeu
    if progresso[-1][1][0] == pedras:   # mesma qtd e bolas pretas e pedras
        messagebox.showinfo("Resultado","Voce venceu!",icon='info')
        draw.mostra_senha(cnv,pedras,nivel,senha)

    elif len(progresso)==lim:       
        messagebox.showinfo("Resultado","Voce perdeu",icon='info')
        draw.mostra_senha(cnv,pedras,nivel,senha)
    
    return





