import PySimpleGUI as sg
import pyperclip
from pynput.keyboard import Listener
import clipboard
import os
import time
os.system('nohup klipper &')


inputLayout = [[sg.Input(key="info")]]
window = sg.Window("SInfo", inputLayout)

ctrl = False
indInfo = 0
Info = []

def recebeInfo():
    global indInfo, Info
    indInfo =0

    dados = clipboard.paste()
    if(len(dados) < 1000): return
    titulo = dados.split("Informar a NF-e\n\n\n")[1].split("\n")[0]
    Info =  4*[""]
    Info[0] = dados.split("NF-e\n")[2].split(" - ")[0]
    if ".\n" in Info[0]:
        Info[0] = Info[0].split(".\n")[1]
    Info[2] = float(dados.split("Total\nR$ ")[1].split("\n")[0].replace(",","."))
    quant = dados.split(" unidade")[0]
    i = 0
    while quant[len(quant) -1 - i] != "\n":
        i+=1
    quant = float(quant[len(quant) - i])
    Info[2] /= quant
    Info[2] = str(Info[2]).replace(".",",")
    if("JAQUETA" in titulo.upper()):
        Info[3] = "42031000"
    elif("NIVEA" in titulo.upper()):
        Info[3] = "33049910"
    elif("NÍVEA" in titulo.upper()):
        Info[3] = "33049910"
    elif("BOINA" in titulo.upper()):
        Info[3] = "65050019"
    elif("BONE" in titulo.upper()):
        Info[3] = "65050019"
    elif("BONÉ" in titulo.upper()):
        Info[3] = "65050019"
    elif("DOT" in titulo.upper()):
        Info[3] = "85185000"
    elif("CERVEJA" in titulo.upper()):
        Info[3] = "22089000"
    elif("PERFUME" in titulo.upper()):
        Info[3] = "33030020"
    elif("ML" in titulo.upper()):
        Info[3] = "33030020"
    elif("AZEITE" in titulo.upper()):
        Info[3] = "15092000"
    


    clipboard.copy(Info[indInfo])

def trocaInfo():
    global indInfo, Info
    indInfo +=1
    print(indInfo)
    if(indInfo == len(Info)):
        indInfo = len(Info) -1
    clipboard.copy(Info[indInfo])

def on_press(key):
    global ctrl
    tecla = str(key).replace("'","")
    if(tecla == "Key.ctrl"):
        ctrl = True
    elif(tecla.upper() == "C" and ctrl):
        print("Sim")
        recebeInfo()
    elif(tecla.upper() == "V" and ctrl):
        print("Sim")
        trocaInfo()

def on_release(key):
    global ctrl
    tecla = str(key)
    if(tecla == "Key.ctrl"):
        ctrl = False
    


def run():
    Listener(on_press=on_press).start()
    Listener(on_release=on_release).start()

run()
while 1:
    time.sleep(0.1)
