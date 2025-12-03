#pip install need
import PySimpleGUI as sg
import pyvisa
from bs4 import BeautifulSoup
#default
import datetime
import requests
import time
import threading
import binascii
import struct

#変数定義(辞書)
change = None
pmch = {'mono':1,'gamma':4}
posdic = {'monoZ_W':-135000, 'monoZ_M':6000, 'gamma_W':-90000,'gamma_M':0}
#pyvisaインスタンス化

try:

    r = pyvisa.ResourceManager()
    #k = r.get_instrument("GPIB0::8::INSTR")
    #2024.10.7 pyvisaのアップデートによりopen_resourceへ変更した
    k = r.open_resource("GPIB0::7::INSTR")
    k.write_termination = '\r\n'
    k.read_termination = '\r\n'

    #PM16C RemoteMode,ch Setting
    k.write("S1R")
    for i in range(2):
        k.write("S111")
        k.write("S124")
        time.sleep(0.2)
except Exception as e:
    sg.popup(str(e))

def htmlget(diname,time):
    #2021.7.4 html adress MDAQ.img to MDAQ
    urlName = 'http://srweb-dmz-03.spring8.or.jp/cgi-bin/MDAQ/mdaq_arcdisp.py?signalname='+diname+'%2Fstatus&time='+ time
    url = requests.get(urlName)
    return(url.content)


def getvalue(chan):
    hexchan = str(hex(chan)).lstrip("0x").upper().zfill(1)
    value = (k.query("S4" + hexchan + "0")).lstrip("R")
    #2の補数表現で取得
    value_2 = int.from_bytes(bytes.fromhex(value.zfill(6)), byteorder='big', signed=True)
    return value_2

def upd():
    while str(k.query("S14")) not in "R00":
        window['-monoz-'].update(getvalue(pmch['mono']))
        window['-gamma-'].update(getvalue(pmch['gamma']))
        time.sleep(0.5)
    else:
        time.sleep(0.05)
        window['-monoz-'].update(getvalue(pmch['mono']))
        window['-gamma-'].update(getvalue(pmch['gamma']))

def amove(ch,chn,pulse):
    if ch == "A":
        com = "2"
        k.write("S11" + str(hex(chn)).lstrip("0x").upper().zfill(1))
    elif ch == "B":
        com = "3"
        k.write("S12" + str(hex(chn)).lstrip("0x").upper().zfill(1))
    else:
        return()
    if pulse == getvalue(chn):
        sg.popup("there is no need")
        return()
    put_pulse = (pulse).to_bytes(3, byteorder="big", signed=True).hex().upper()
    k.write("S1303")
    k.write("S3"+ com + put_pulse + "11")
    update = threading.Thread(target=upd)
    update.start()
    
#現在地取得関数　引数：チャンネル番号　戻り値：パルス整数

#  セクション1 - オプションの設定と標準レイアウト
sg.theme('Dark Blue')
layout = [
    [sg.Text('Mono-White SWitchProgram')],
    [sg.Submit(button_text='update',key='-update-')],
    [sg.Text('▼Component Status')],
    [sg.Text('MBS Status', size=(20,1)),sg.Text('unacquired',size=(10, 1),key='-mbs-')],
    [sg.Text('DSS Status', size=(20,1)),sg.Text('unacquired',size=(10, 1),key='-dss-')],
    [sg.Text('Opt  Hatch Status', size=(20, 1)), sg.Text('unacquired',size=(10, 1),key='-opt_hatch-')],
    [sg.Text('Opt2 Hatch Status', size=(20, 1)), sg.Text('unacquired',size=(10, 1),key='-opt2_hatch-')],
    [sg.Text('Exp Hatch  Status', size=(20, 1)), sg.Text('unacquired',size=(10, 1),key='-exp_hatch-')],
    [sg.Text('▼Axis Position')],
    [sg.Text('MonoZZ Position', size=(20, 1)), sg.Text('unacquired',size=(10, 1),key='-monoz-')],
    [sg.Text('γStopper Position', size=(20, 1)), sg.Text('unacquired',size=(10, 1),key='-gamma-')],
    [sg.Text('')],
    [sg.Submit(button_text='Mono Mode'),sg.Submit(button_text='White Mode')]
]

# セクション 2 - ウィンドウの生成
window = sg.Window('M_W Move', layout)

# セクション 3 - イベントループ
while True:
    event, values = window.read()

    if event is None:
        print('exit')
        break
    
    if event == '-update-':
        #現在時刻の取得、変数格納
        
        dt_now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        #必要なデータを一気に取得、それぞれの変数へ格納(str)        
        soup_hatch = BeautifulSoup(htmlget('bl_plc_14b1_di_25',dt_now), "html.parser")
        soup_shut = BeautifulSoup(htmlget('bl_plc_14b1_di_9',dt_now), "html.parser")
        elems_shut = soup_shut.find_all("td")
        binstr_shut = format(int(elems_shut[2].string,16), '030b')
        binls_shut = list(binstr_shut)[::-1]
        elems_hatch = soup_hatch.find_all("td")
        binstr_hatch = format(int(elems_hatch[2].string,16), '030b')
        binls_hatch = list(binstr_hatch)[::-1]

        #change accept
        change = int(binls_shut[23]) + int(binls_shut[26]) + int(binls_hatch[19]) + int(binls_hatch[20]) + int(binls_hatch[21])

        #print(change)
        #mbs judge
        if binls_shut[23] == '0':
            window['-mbs-'].update('Close')
        elif binls_shut[23] == '1':
            window['-mbs-'].update('Open')
        #dss judge
        if binls_shut[26] == '0':
            window['-dss-'].update('Close')
        elif binls_shut[26] == '1':
            window['-dss-'].update('Open')
        #opt judge
        if binls_hatch[19] == '0':
            window['-opt_hatch-'].update('Open')
        elif binls_hatch[19] == '1':
            window['-opt_hatch-'].update('Nomal Close')
        #opt2 judge
        if binls_hatch[20] == '0':
            window['-opt2_hatch-'].update('Open')
        elif binls_hatch[20] == '1':
            window['-opt2_hatch-'].update('Nomal Close')
        #exp judge
        if binls_hatch[21] == '0':
            window['-exp_hatch-'].update('Open')
        elif binls_hatch[21] == '1':
            window['-exp_hatch-'].update('Nomal Close')
        
        #change = 0
        #axis update
        window['-monoz-'].update(getvalue(pmch['mono']))
        window['-gamma-'].update(getvalue(pmch['gamma']))
        
    if event == 'Mono Mode':
        accept = sg.popup_ok_cancel('Switch White to Mono Ok?')
        if accept == 'OK' and change == 0:
            amove("A",1,posdic['monoZ_M'])
            amove("B",4,posdic['gamma_M'])
            change = None
        elif accept == 'OK':
            sg.popup("It cannot be changed.\r\nPlease check the permit conditions.")


    if event == 'White Mode':
        accept = sg.popup_ok_cancel('Switch Mono to White Ok?')
        if accept == 'OK' and change == 0:
            amove("A",1,posdic['monoZ_W'])
            amove("B",4,posdic['gamma_W'])
            change = None
        elif accept == 'OK':
            sg.popup("It cannot be changed.\r\nPlease check the permit conditions.")


# セクション 4 - ウィンドウの破棄と終了
window.close()
