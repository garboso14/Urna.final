import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
import sqlite3 as sqltor
# import matplotlib.pyplot as plt
conn=sqltor.connect('main.db') #main database
cursor=conn.cursor() #main cursor
cursor.execute("""CREATE TABLE IF NOT EXISTS poll
                    (name)""")

def pollpage(): #page for polling
    def proceed():
        chose=choose.get()
        print(chose)
        command='update polling set votes=votes+1 where name=?'
        pd.execute(command,(chose,))
        pd.commit()
        messagebox.showinfo('Successo!','Você votou com sucesso')
    choose=StringVar()
    names=[]
    pd=sqltor.connect(plname+'.db') #poll database
    pcursor=pd.cursor() #poll cursor
    pcursor.execute('select name from polling')
    data=pcursor.fetchall()
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        names.append(ndata)
    print(names)
    ppage=Toplevel()
    ppage.geometry('300x300')
    ppage.title('Poll')


    Label(ppage,text='Vote em qualquer um').grid(row=1,column=3)
    for i in range(len(names)):
        Radiobutton(ppage,text=names[i],value=names[i],variable=choose).grid(row=2+i,column=1)
    Button(ppage,text='Vote',command=proceed).grid(row=2+i+1,column=2)


def polls(): #mypolls
    def proceed():
        global plname
        plname=psel.get()
        if plname=='-selecionar-':
            return messagebox.showerror('Error','Selecione uma votação')
        else:
            mpolls.destroy()
            pollpage()
    cursor.execute('select name from poll')
    data=cursor.fetchall()
    pollnames=['-selecionar-']
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        pollnames.append(ndata)
    psel=StringVar()
    mpolls=Toplevel()
    mpolls.geometry('300x300')
    mpolls.title('programa de votação')
    Label(mpolls,text='Selecione a votação',font='Helvetica 12 bold').grid(row=1,column=3)
    select=ttk.Combobox(mpolls,values=pollnames,state='readonly',textvariable=psel)
    select.grid(row=2,column=3)
    select.current(0)
    Button(mpolls,text='avançar',command=proceed).grid(row=2,column=4)



def create():
    def proceed():
        global pcursor
        pname=name.get() #pollname
        can=cname.get()   #candidatename
        if pname=='':
            return messagebox.showerror('Error','Coloque o nome das votações')
        elif can=='':
            return messagebox.showerror('Error','Coloque o nome dos candidatos')
        else:
            candidates=can.split(',') #candidate list
            command='insert into poll (name) values (?);'
            cursor.execute(command,(pname,))
            conn.commit()
            pd=sqltor.connect(pname+'.db') #poll database
            pcursor=pd.cursor() #poll cursor
            pcursor.execute("""CREATE TABLE IF NOT EXISTS polling
            (name TEXT,votes INTEGER)""")
            for i in range(len(candidates)):
                command='insert into polling (name,votes) values (?, ?)'
                data=(candidates[i],0)
                pcursor.execute(command,data)
                pd.commit()
            pd.close()
            messagebox.showinfo('Successo!','Sua eleição foi criada')
            cr.destroy()

    name=StringVar()
    cname=StringVar()
    cr=Toplevel()
    cr.geometry('1000x800')
    cr.title('Criando uma nova eleição')
    Label(cr,text='Esreva os detalhes',font='Helvetica 12 bold').grid(row=1,column=2)
    Label(cr,text='Escreva o nome da eleição ').grid(row=2,column=1)
    Entry(cr,width=30,textvariable=name).grid(row=2,column=2) #poll name
    Label(cr,text='(ex:elegendo presidente da turma)').place(x=354,y=25)
    Label(cr,text='Nome dos candidatos: ').grid(row=3,column=1)
    Entry(cr,width=45,textvariable=cname).grid(row=3,column=2) #candidate name
    Label(cr,text='Nota: Insira os nomes dos candidatos um por um cada um seguido de virgula ').grid(row=4,column=2)
    Label(cr,text='ex: candidato1,candidato2,candidato3....').grid(row=5,column=2)
    Button(cr,text='Prossiguir',command=proceed).grid(row=6,column=2)
def selpl(): #pollresults
    def results():
        sel=sele.get()  #selected option
        if sel=='-selecionar-':
            return messagebox.showerror('Error','Selecione a votação')
        else:
            pl.destroy()
            def project():
                names=[]
                votes=[]
                for i in range(len(r)):
                    data=r[i]
                    names.append(data[0])
                    votes.append(data[1])
                #     plt.title('Resultado da votação')
                # plt.pie(votes,labels=names,autopct='%1.1f%%',shadow=True,startangle=140)
                # plt.axis('equal')
                # plt.show()

            res=Toplevel() #result-page
            res.geometry('1000x800')
            res.title('Results!')
            Label(res,text='Esse é o resultado!',font='Helvetica 12 bold').grid(row=1,column=2)
            con=sqltor.connect(sel+'.db')
            pcursor=con.cursor()
            pcursor.execute('select * from polling')
            r=pcursor.fetchall() #data-raw
            for i in range(len(r)):
                data=r[i]
                Label(res,text=data[0]+': '+str(data[1])+' votes').grid(row=2+i,column=1)
            Button(res,text='Project Results',command=project).grid(row=2+i+1,column=2)


    cursor.execute('select name from poll')
    data=cursor.fetchall()
    pollnames=['-select-']
    for i in range(len(data)):
        data1=data[i]
        ndata=data1[0]
        pollnames.append(ndata)
    sele=StringVar()
    pl=Toplevel()
    pl.geometry('1000x800')
    pl.title('Voting System')
    Label(pl,text='Select Poll',font='Helvetica 12 bold').grid(row=1,column=1)
    sel=ttk.Combobox(pl,values=pollnames,state='readonly',textvariable=sele)
    sel.grid(row=2,column=1)
    sel.current(0)
    Button(pl,text='Resultados',command=results).grid(row=2,column=2)
def about():
    messagebox.showinfo('Sobre','Desenvolvido por:Iago Cardoso do nascimento')


home=Tk()
home.geometry('400x400')
home.title('Urna Eletronica')
home['bg'] = '#49A'
Label(home,text='voting program made in python',font='Helvetica 12 bold',bg='#49A').grid(row=1,column=2)
Button(home,text='Crie uma nova votação +',command=create).grid(row=3,column=2)
Button(home,text='Votação',command=polls).grid(row=4,column=2)
Button(home,text='Resultados da votação',command=selpl).grid(row=5,column=2)
Label(home,text='GitHub:https://github.com/garboso14/Urna.final.git',bg='#49A').grid(row=6,column=2)
Button(home,text='Sobre',command=about).grid(row=1,column=3)
home.mainloop()