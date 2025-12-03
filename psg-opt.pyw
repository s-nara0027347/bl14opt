import sys
import time                 #時間設定
import datetime             #日付時刻
import socket               #ソケット通信
import re                   #正規表現
import csv                  #csvファイル
import threading            #スレッド
import PySimpleGUI as sg    #pysimplegui GUIの作成
#外部設定ファイルインポート
import optconst

####################################### Variable definition #################################################
#GUI全体のテーマ
sg.theme('Light Blue 3')
#正規表現
numre = r'([+-]?[0-9]+\.?[0-9]*)'
#BL-WS IPアドレス値,ポート番号'172.24.242.17''192.168.179.6'
ip = '172.24.242.17'
port = 10101
#WaitTime
wait = 1
movewait = 0.5
bgcolor = 'black'

####################################### Function #################################################
#soket関数
def ipsock(comstr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip,port))
        s.sendall(comstr.encode())
        data = repr(s.recv(1024))
        window['ipmessage'].update(data)
        return(data)

#数値を抜き取る関数
def reget(reg):
    get_text = reg.rsplit('/',2)[1]
    r=re.compile(numre)
    get_retext=r.match(get_text)
    if get_retext is None:
        rettex='Not match'
    else:
        rettex=get_retext.group(0)
    return(rettex)

#リミットチェック関数
def checklim(obj,value):
    if  float(optconst.lowlimit[obj]) <= float(value) <= float(optconst.highlimit[obj]) :
        return(True)
    else :
        return(False)

#全ての値取得(リロード)関数
def reload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
        so.connect((ip,port))
        for i in optconst.svoc_get:           
            send_text=optconst.svoc_get[i]
            so.sendall(send_text.encode())
            get_text = reget(repr(so.recv(1024)))
            window['get_' + str(i)].update(get_text) 

#表示値更新関数
def waitmove(axobj):
    window['axis_status'].update('Axis moving')
    window['axis_status'].Update(text_color='red')
    while ('ok' not in ipsock(optconst.svoc_query[axobj])) and ('inactive'  not in ipsock(optconst.svoc_query[axobj])):   
        #軸移動中ラベル変更   
        sett=reget(ipsock(optconst.svoc_get[axobj]))
        window['get_' + str(axobj)].update(sett) 
        #Netplaneのみalpha1,alpha2の値を取得し続ける
        if 'netplane' in axobj:
            alpha1 = reget(ipsock(optconst.svoc_get['stmono_1_alpha1']))
            alpha2 = reget(ipsock(optconst.svoc_get['stmono_1_alpha2']))
            window['get_stmono_1_alpha1'].update(alpha1)
            window['get_stmono_1_alpha2'].update(alpha2)         
        time.sleep(movewait)
    else:
        window['get_' + str(axobj)].update(reget(ipsock(optconst.svoc_get[axobj]))) 
    window['axis_status'].update('Axis stop')
    window['axis_status'].Update(text_color='black')
#軸移動関数
def axismv(axobj,axvalue):
    try:
        if values[axobj + '_ch'] == False:
            return()  
        #ABS REL 判断
        if axobj + '_rel' in values:
            if values[axobj + '_rel']:
                axvalue = float(reget(ipsock(optconst.svoc_get[axobj]))) + float(axvalue) 
        #パルスの場合、intへキャスト
        if 'pulse' in optconst.svoc_unit[axobj]:
            axvalue = int(axvalue)
        #リミットチェック
        if checklim(axobj,axvalue) == False:
            sg.popup('Limit Check')
            return()
        #軸移動前のクエリチェックを変数へ格納
        movequery = ipsock(optconst.svoc_query[axobj])
        if ('inactive' in movequery) or ('ok' in movequery):
            ipsock(optconst.svoc_put[axobj] + str(axvalue) + optconst.svoc_unit[axobj])
            waitmove(axobj)
    except Exception:
        return()    

#ミラー挿入、位置変更関数
def mirrortilt():
    #tcslit1 height move
    tilt = float(window['mirrorcombo'].get())
    ipsock(optconst.svoc_put['slit_1_height'] + str(optconst.mirror_tcslit[tilt]) + optconst.svoc_unit['slit_1_height'])
    waitmove('slit_1_height')
    time.sleep(wait)
    # M1_zが-5mmより小さいとき(退避している場合)は、M1_z基準位置0へ動かす
    # ミラー挿入時はzを動かす必要がないため
    # 2021.6.16修正
    if float(reget(ipsock(optconst.svoc_get['m100v_1_z']))) < -5.0:
        ipsock(optconst.svoc_put['m100v_1_z'] + '0' + optconst.svoc_unit['m100v_1_z'])
        waitmove('m100v_1_z')
        time.sleep(wait)
    #M1_tyを傾ける
    ipsock(optconst.svoc_put['m100v_1_ty'] + str(tilt + optconst.mirror_offset) + optconst.svoc_unit['m100v_1_ty'])
    waitmove('m100v_1_ty')    
    time.sleep(wait)
    #M1bendのみ、一旦5000にする(バックラッシュ)
    #2021.6.16 0パルスから+5000パルスへ変更
    ipsock(optconst.svoc_put['m100v_1_bend'] + '5000' + optconst.svoc_unit['m100v_1_bend'])
    waitmove('m100v_1_bend')  
    time.sleep(wait)
    #M1bendを曲げる
    ipsock(optconst.svoc_put['m100v_1_bend'] + str(optconst.m1_bend[tilt]) + optconst.svoc_unit['m100v_1_bend'])
    waitmove('m100v_1_bend') 
    time.sleep(wait)
    # M2_zが+5mmより大きいとき(退避している場合)は、M2_z基準位置0へ動かす
    # ミラー挿入時はzを動かす必要がないため
    # 2021.6.16修正
    if float(reget(ipsock(optconst.svoc_get['m100v_2_z']))) > 5.0:
        ipsock(optconst.svoc_put['m100v_2_z'] + '0' + optconst.svoc_unit['m100v_2_z'])
        waitmove('m100v_2_z') 
        time.sleep(wait)
    #M2_tyを傾ける
    ipsock(optconst.svoc_put['m100v_2_ty'] + str(tilt + optconst.mirror_offset) + optconst.svoc_unit['m100v_2_ty'])
    waitmove('m100v_2_ty') 
    time.sleep(wait)
    #M2bendを曲げる
    ipsock(optconst.svoc_put['m100v_2_bend'] + str(optconst.m2_bend[tilt]) + optconst.svoc_unit['m100v_2_bend'])
    waitmove('m100v_2_bend') 

#ミラー退避関数
def mirrorevacuation():
    #tcslit1の縦幅を1mmにする
    ipsock(optconst.svoc_put['slit_1_height'] + str(optconst.mirror_evacuation['slit_1_height']) + optconst.svoc_unit['slit_1_height'])
    waitmove('slit_1_height')
    time.sleep(wait)
    #M1bend曲げ癖をとるため、+5000にまず動かす
    ipsock(optconst.svoc_put['m100v_1_bend'] + '5000' + optconst.svoc_unit['m100v_1_bend'])
    waitmove('m100v_1_bend')
    time.sleep(wait)
    #M1_bend0にする
    ipsock(optconst.svoc_put['m100v_1_bend'] + str(optconst.mirror_evacuation['m100v_1_bend']) + optconst.svoc_unit['m100v_1_bend'])
    waitmove('m100v_1_bend')
    time.sleep(wait)
    #M1_tyを傾ける
    ipsock(optconst.svoc_put['m100v_1_ty'] + str(optconst.mirror_evacuation['m100v_1_ty']) + optconst.svoc_unit['m100v_1_ty'])
    waitmove('m100v_1_ty')
    time.sleep(wait)
    #M1_z基準位置0へ動かす
    ipsock(optconst.svoc_put['m100v_1_z'] + str(optconst.mirror_evacuation['m100v_1_z']) + optconst.svoc_unit['m100v_1_z'])
    waitmove('m100v_1_z')
    time.sleep(wait)
    #M2bend曲げ癖をとるため、+5000にまず動かす
    ipsock(optconst.svoc_put['m100v_2_bend'] + '5000' + optconst.svoc_unit['m100v_2_bend'])
    waitmove('m100v_2_bend')
    time.sleep(wait)
    #M2_bend0にする
    ipsock(optconst.svoc_put['m100v_2_bend'] + str(optconst.mirror_evacuation['m100v_2_bend']) + optconst.svoc_unit['m100v_2_bend'])
    waitmove('m100v_2_bend')
    time.sleep(wait)
    #M1_tyを傾ける
    ipsock(optconst.svoc_put['m100v_2_ty'] + str(optconst.mirror_evacuation['m100v_2_ty']) + optconst.svoc_unit['m100v_2_ty'])
    waitmove('m100v_2_ty')
    time.sleep(wait)
    #M1_z基準位置0へ動かす
    ipsock(optconst.svoc_put['m100v_2_z'] + str(optconst.mirror_evacuation['m100v_2_z']) + optconst.svoc_unit['m100v_2_z'])
    waitmove('m100v_2_z')

def mirrorradio():
    window['slit_1_height_rel'].update(False)
    window['m100v_1_z_rel'].update(False)
    window['m100v_1_ty_rel'].update(False)
    window['m100v_1_bend_rel'].update(False)
    window['m100v_2_z_rel'].update(False)
    window['m100v_2_ty_rel'].update(False)
    window['m100v_2_bend_rel'].update(False)
    time.sleep(0.5)
    window['slit_1_height_abs'].update(True)
    window['m100v_1_z_abs'].update(True)
    window['m100v_1_ty_abs'].update(True)
    window['m100v_1_bend_abs'].update(True)
    window['m100v_2_z_abs'].update(True)
    window['m100v_2_ty_abs'].update(True)
    window['m100v_2_bend_abs'].update(True)

def mirror_rel():
    if values['slit_1_height_rel'] or values['m100v_1_z_rel'] or values['m100v_1_ty_rel'] or values['m100v_1_bend_rel'] or values['m100v_2_z_rel'] or values['m100v_2_ty_rel'] or values['m100v_2_bend_rel']:
        return(False)
    else:
        return(True)   
   

####################################### GUI #################################################
#メニューのレイアウト
menu_def =  ['&File', ['Save', 'reload(F5)']],
#エネルギータブのタブ内レイアウト
energy_tab = [
            [sg.Text('Netplane Change')],
            [sg.Text('Netplane',size=(10,1)),sg.Text('-',size=(10,1),key='get_stmono_1_netplane'),sg.Combo(['311', '111', '511'],size=(10,1),key='netplanecombo',default_value='311'),sg.Button('ChangeNetPlane',key='stmono_1_netplane',size=(14,2)),sg.Checkbox('enable',key='stmono_1_netplane_ch')],
            [sg.Text('')],
            [sg.Text('Axis',size=(10,1)),sg.Text('Value',size=(10,1)),sg.Text('Dest',size=(18,1)),sg.Text('Unit',size=(5,1))],
            [sg.Text('Energy',size=(10,1)),sg.Text('-',size=(10,1),key='get_stmono_1_energy'),sg.InputText(key='stmono_1_energy',size=(20,1),background_color='white'),sg.Text('keV',size=(7,1)),sg.Checkbox('enable',key='stmono_1_energy_ch',default=True)],
            [sg.Text('Wavelength',size=(10,1)),sg.Text('-',size=(10,1),key='get_stmono_1_wavelength'),sg.InputText(key='stmono_1_wavelength',size=(20,1),background_color='white'),sg.Text('angstrom',size=(7,1)),sg.Checkbox('enable',key='stmono_1_wavelength_ch')],
            [sg.Text('Angle',size=(10,1)),sg.Text('-',size=(10,1),key='get_stmono_1_angle'),sg.InputText(key='stmono_1_angle',size=(20,1),background_color='white'),sg.Text('degree',size=(7,1)),sg.Checkbox('enable',key='stmono_1_angle_ch',default=True)],
           ]
#モノクロタブのタブ内レイアウト
mono_tab = [
            [sg.Text('◆ Monochromator')],
            [sg.Text('Axis',size=(10,1)),sg.Text('Value',size=(10,1)),sg.Text('Dest',size=(18,1)),sg.Text('Unit',size=(5,1)),sg.Text('Movemode',size=(10,1))],
            [sg.Text('y1',size=(10,1),key='stmono_1_y1_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_y1'),sg.InputText(key='stmono_1_y1',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',1,key='stmono_1_y1_abs',default=True,enable_events=True),sg.Radio('REL',1,key='stmono_1_y1_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_y1_ch')],
            [sg.Text('theata',size=(10,1),key='stmono_1_theta_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_theta'),sg.InputText(key='stmono_1_theta',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',2,key='stmono_1_theta_abs',default=True,enable_events=True),sg.Radio('REL',2,key='stmono_1_theta_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_theta_ch')],
            [sg.Text('alpha1',size=(10,1),key='stmono_1_alpha1_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_alpha1'),sg.InputText(key='stmono_1_alpha1',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',3,key='stmono_1_alpha1_abs',default=True,enable_events=True),sg.Radio('REL',3,key='stmono_1_alpha1_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_alpha1_ch',default=True)],
            [sg.Text('phi1',size=(10,1),key='stmono_1_phi1_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_phi1'),sg.InputText(key='stmono_1_phi1',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',4,key='stmono_1_phi1_abs',default=True,enable_events=True),sg.Radio('REL',4,key='stmono_1_phi1_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_phi1_ch',default=True)],
            [sg.Text('x1',size=(10,1),key='stmono_1_x1_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_x1'),sg.InputText(key='stmono_1_x1',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',5,key='stmono_1_x1_abs',default=True,enable_events=True),sg.Radio('REL',5,key='stmono_1_x1_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_x1_ch')],
            [sg.Text('dtheta1',size=(10,1),key='stmono_1_dtheta1_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_dtheta1'),sg.InputText(key='stmono_1_dtheta1',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',6,key='stmono_1_dtheta1_abs',default=True,enable_events=True),sg.Radio('REL',6,key='stmono_1_dtheta1_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_dtheta1_ch',default=True)],
            [sg.Text('z1',size=(10,1),key='stmono_1_z1_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_z1'),sg.InputText(key='stmono_1_z1',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',7,key='stmono_1_z1_abs',default=True,enable_events=True),sg.Radio('REL',7,key='stmono_1_z1_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_z1_ch')],
            [sg.Text('alpha2',size=(10,1),key='stmono_1_alpha2_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_alpha2'),sg.InputText(key='stmono_1_alpha2',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',8,key='stmono_1_alpha2_abs',default=True,enable_events=True),sg.Radio('REL',8,key='stmono_1_alpha2_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_alpha2_ch',default=True)],
            [sg.Text('phi2',size=(10,1),key='stmono_1_phi2_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_phi2'),sg.InputText(key='stmono_1_phi2',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',9,key='stmono_1_phi2_abs',default=True,enable_events=True),sg.Radio('REL',9,key='stmono_1_phi2_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_phi2_ch',default=True)],
            [sg.Text('x2',size=(10,1),key='stmono_1_x2_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_x2'),sg.InputText(key='stmono_1_x2',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',10,key='stmono_1_x2_abs',default=True,enable_events=True),sg.Radio('REL',10,key='stmono_1_x2_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_x2_ch')],
            [sg.Text('dtheta2',size=(10,1),key='stmono_1_dtheta2_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_dtheta2'),sg.InputText(key='stmono_1_dtheta2',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',11,key='stmono_1_dtheta2_abs',default=True,enable_events=True),sg.Radio('REL',11,key='stmono_1_dtheta2_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_dtheta2_ch',default=True)],
            [sg.Text('z2',size=(10,1),key='stmono_1_z2_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_z2'),sg.InputText(key='stmono_1_z2',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',12,key='stmono_1_z2_abs',default=True,enable_events=True),sg.Radio('REL',12,key='stmono_1_z2_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_z2_ch')],
            [sg.Text('bend',size=(10,1),key='stmono_1_bend_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_stmono_1_bend'),sg.InputText(key='stmono_1_bend',size=(20,1),background_color='white'),sg.Text('pulse'),sg.Radio('ABS',13,key='stmono_1_bend_abs',default=True,enable_events=True),sg.Radio('REL',13,key='stmono_1_bend_rel',enable_events=True),sg.Checkbox('enable',key='stmono_1_bend_ch')],
           ]
#TCスリットのタブ内レイアウト
tcslit_tab = [
            [sg.Text('◆ TCSlit')],
            [sg.Text('Axis',size=(10,1)),sg.Text('Value',size=(10,1)),sg.Text('Dest',size=(18,1)),sg.Text('Unit',size=(5,1)),sg.Text('Movemode',size=(10,1))],
            [sg.Text('Vertical',size=(10,1),key='slit_1_vertical_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_slit_1_vertical'),sg.InputText(key='slit_1_vertical',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',14,key='slit_1_vertical_abs',default=True,enable_events=True),sg.Radio('REL',14,key='slit_1_vertical_rel',enable_events=True),sg.Checkbox('enable',key='slit_1_vertical_ch',default=True)],
            [sg.Text('Horizontal',size=(10,1),key='slit_1_horizontal_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_slit_1_horizontal'),sg.InputText(key='slit_1_horizontal',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',15,key='slit_1_horizontal_abs',default=True,enable_events=True),sg.Radio('REL',15,key='slit_1_horizontal_rel',enable_events=True),sg.Checkbox('enable',key='slit_1_horizontal_ch',default=True)],            
            [sg.Text('Height',size=(10,1),key='slit_1_height_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_slit_1_height'),sg.InputText(key='slit_1_height',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',16,key='slit_1_height_abs',default=True,enable_events=True),sg.Radio('REL',16,key='slit_1_height_rel',enable_events=True),sg.Checkbox('enable',key='slit_1_height_ch',default=True)],
            [sg.Text('Width',size=(10,1),key='slit_1_width_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_slit_1_width'),sg.InputText(key='slit_1_width',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',17,key='slit_1_width_abs',default=True,enable_events=True),sg.Radio('REL',17,key='slit_1_width_rel',enable_events=True),sg.Checkbox('enable',key='slit_1_width_ch',default=True)],
            ]
#ミラータブのタブ内レイアウト
mirror_tab = [
            [sg.Text('▲ Mirror 1')],
            [sg.Text('Axis',size=(10,1)),sg.Text('Value',size=(10,1)),sg.Text('Dest',size=(18,1)),sg.Text('Unit',size=(5,1)),sg.Text('Movemode',size=(10,1))],
            [sg.Text('M1 y',size=(10,1),key='m100v_1_y_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_m100v_1_y'),sg.InputText(key='m100v_1_y',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',18,key='m100v_1_y_abs',default=True,enable_events=True),sg.Radio('REL',18,key='m100v_1_y_rel',enable_events=True),sg.Checkbox('enable',key='m100v_1_y_ch')],
            [sg.Text('M1 z',size=(10,1),key='m100v_1_z_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_m100v_1_z'),sg.InputText(key='m100v_1_z',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',19,key='m100v_1_z_abs',default=True,enable_events=True),sg.Radio('REL',19,key='m100v_1_z_rel',enable_events=True),sg.Checkbox('enable',key='m100v_1_z_ch',default=True)], 
            [sg.Text('M1 ty',size=(10,1),key='m100v_1_ty_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_m100v_1_ty'),sg.InputText(key='m100v_1_ty',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',20,key='m100v_1_ty_abs',default=True,enable_events=True),sg.Radio('REL',20,key='m100v_1_ty_rel',enable_events=True),sg.Checkbox('enable',key='m100v_1_ty_ch',default=True)],
            [sg.Text('M1 tz',size=(10,1),key='m100v_1_tz_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_m100v_1_tz'),sg.InputText(key='m100v_1_tz',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',21,key='m100v_1_tz_abs',default=True,enable_events=True),sg.Radio('REL',21,key='m100v_1_tz_rel',enable_events=True),sg.Checkbox('enable',key='m100v_1_tz_ch')],  
            [sg.Text('M1 bend',size=(10,1),key='m100v_1_bend_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_m100v_1_bend'),sg.InputText(key='m100v_1_bend',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',22,key='m100v_1_bend_abs',default=True,enable_events=True),sg.Radio('REL',22,key='m100v_1_bend_rel',enable_events=True),sg.Checkbox('enable',key='m100v_1_bend_ch',default=True)],
            [sg.Text('▼ Mirror 2')],
            [sg.Text('Axis',size=(10,1)),sg.Text('Value',size=(10,1)),sg.Text('Dest',size=(18,1)),sg.Text('Unit',size=(5,1)),sg.Text('Movemode',size=(10,1))],
            [sg.Text('M2 y',size=(10,1),key='m100v_2_y_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_m100v_2_y'),sg.InputText(key='m100v_2_y',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',23,key='m100v_2_y_abs',default=True,enable_events=True),sg.Radio('REL',23,key='m100v_2_y_rel',enable_events=True),sg.Checkbox('enable',key='m100v_2_y_ch')],
            [sg.Text('M2 z',size=(10,1),key='m100v_2_z_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_m100v_2_z'),sg.InputText(key='m100v_2_z',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',24,key='m100v_2_z_abs',default=True,enable_events=True),sg.Radio('REL',24,key='m100v_2_z_rel',enable_events=True),sg.Checkbox('enable',key='m100v_2_z_ch',default=True)], 
            [sg.Text('M2 ty',size=(10,1),key='m100v_2_ty_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_m100v_2_ty'),sg.InputText(key='m100v_2_ty',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',25,key='m100v_2_ty_abs',default=True,enable_events=True),sg.Radio('REL',25,key='m100v_2_ty_rel',enable_events=True),sg.Checkbox('enable',key='m100v_2_ty_ch',default=True)],
            [sg.Text('M2 tz',size=(10,1),key='m100v_2_tz_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_m100v_2_tz'),sg.InputText(key='m100v_2_tz',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',26,key='m100v_2_tz_abs',default=True,enable_events=True),sg.Radio('REL',26,key='m100v_2_tz_rel',enable_events=True),sg.Checkbox('enable',key='m100v_2_tz_ch')],  
            [sg.Text('M2 bend',size=(10,1),key='m100v_2_bend_name',text_color=bgcolor),sg.Text('-',size=(10,1),key='get_m100v_2_bend'),sg.InputText(key='m100v_2_bend',size=(20,1),background_color='white'),sg.Text('mm'),sg.Radio('ABS',27,key='m100v_2_bend_abs',default=True,enable_events=True),sg.Radio('REL',27,key='m100v_2_bend_rel',enable_events=True),sg.Checkbox('enable',key='m100v_2_bend_ch',default=True)],
            ]
#ミラーチルトのレイアウト
mirror_move = [
            [sg.Text('Mirror Insert,ChangeAngle')],
            [sg.Text('')],
            [sg.Text('Mirror Angle'),sg.Combo(['1.0','1.5','2.0','2.5','3.0','3.5','4.0','4.5','5.0','5.5','6.0','6.5','7.0','7.5','8.0'],size=(10,1),key='mirrorcombo',default_value='1.0'),sg.Text('mrad',size=(17,1)),sg.Button('MirrorMove',key='mirrorchange',size=(18,2))],
#ミラー退避のレイアウト
            [sg.Text('')],
            [sg.Text('Mirror Evacuation')],
            [sg.Text('▼ Destposition M1_z -10mm , M1_ty 0mrad , M1_bend 0pulse')],
            [sg.Text('▼ Destposition M2_z +10mm , M2_ty 0mrad , M2_bend 0pulse')],
            [sg.Text('',size=(40,1)),sg.Button('Evacuation',key='mirrorevacuation',size=(18,2))]
             ]
#全体のレイアウト
layout = [
            [sg.Menu(menu_def)],
            [sg.TabGroup([[sg.Tab('Netplane-Energy', energy_tab), sg.Tab('MonoChromator', mono_tab),sg.Tab('TCSlit',tcslit_tab),sg.Tab('Mirror',mirror_tab),sg.Tab('MirrorMove',mirror_move)]])],
            [sg.Text('Axis Stop',key='axis_status',size=(10,2)),sg.Button('Stop',key='stop',size=(10,2)),sg.Button('Em Stop',key='emstop',button_color=('black', 'red'),size=(10,2)),sg.Button('Test',key='test')],
            [sg.Text('ip_message',key='ipmessage',size=(60,1))]          
         ]


#Windowのインスタンス化
window = sg.Window("Opt_Move", layout ,return_keyboard_events=True,text_justification='center',element_padding=(10,6),finalize=True)

for i in optconst.svoc_get:
    if 'netplane' not in i:
        window[i].bind('<FocusIn>', '_in')
        window[i].bind('<FocusOut>', '_out')

####################################### Event Loop #################################################
while True:
    event, values = window.Read()
    #event, values = sg.read_all_windows()    
    if event is None:
        break

    if 'in' in event :
        window[event.replace('_in','')].update(background_color='khaki')
    
    if 'out' in event:
        window[event.replace('_out','')].update(background_color='white')

    if '_abs' in event:
        sendabs = event.replace('_abs','')
        window[sendabs + '_name'].Update(text_color=bgcolor)
    
    if '_rel' in event:
        sendabs = event.replace('_rel','')
        #2021.06.16 clor red from green
        window[sendabs + '_name'].Update(text_color='red')

    if event == 'reload(F5)':
        thre=threading.Thread(target=reload)
        thre.start()

    if event == 'F5:116':
        thre=threading.Thread(target=reload)
        thre.start()

    if event == '\x0D':
        send = str(window.FindElementWithFocus().Key)
        val = str(values[window.FindElementWithFocus().Key])        
        axisth=threading.Thread(target=axismv,args=(send,val))
        axisth.start()

    if event == 'stmono_1_netplane':
        accept = sg.popup_ok_cancel('Move Netplane Ok?')
        if accept == 'OK' :
            axisth=threading.Thread(target=axismv,args=('stmono_1_netplane',str(window['netplanecombo'].get())))
            axisth.start()

    if event == 'mirrorchange':
        accept = sg.popup_ok_cancel('Move Mirror Ok?')
        if accept == 'OK' :
            mirrorth=threading.Thread(target=mirrortilt)
            mirrorth.start()


    if event == 'mirrorevacuation':
        accept = sg.popup_ok_cancel('Mirror evacuation Ok?')
        if accept == 'OK' :
            mirrorevth=threading.Thread(target=mirrorevacuation)
            mirrorevth.start()

    if event == 'stop':
        send = str(window.FindElementWithFocus().Key)
        if 'netplanecombo' in send:
            send = send.replace('netplanecombo','stmono_1_netplane')
        ipsock(optconst.svoc_put[send] + 'stop')
    
    if event == 'emstop':
        send = str(window.FindElementWithFocus().Key)
        accept = sg.popup_ok_cancel('Emargency?')
        if accept == 'OK' :
            if 'stmono_1' in send:
                ipsock('put/bl_14b1_tc1_stmono_1/emstop')
            elif 'slit_1' in send:
                ipsock('put/bl_14b1_tc1_slit_1/emstop')
            elif 'm100v_1' in send:
                ipsock('put/bl_14b1_tc1_m100v_1/emstop')
            elif 'm100v_2' in send:
                ipsock('put/bl_14b1_tc1_m100v_2/emstop')

    if event == 'Save':
        save_path = sg.PopupGetFile('savefile',no_window = True, save_as = True,file_types=(('csv', '.csv'),('txt', '.txt')))
        if save_path != '':          
            with open(save_path, mode='w') as f:
                wfile = csv.writer(f)
                dt_now = datetime.datetime.now()
                wfile.writerow([dt_now.date(),dt_now.time()])
                for i in optconst.svoc_get:
                    wfile.writerow([i,window['get_' + i].DisplayText])
    
    if event == 'test':
        window['stmono_1_y1_abs'].update(False)
        window['get_stmono_1_y1'].Update(background_color='red')

    if event == None:
        #window[window.FindElementWithFocus().Key].update(background_color='red')
        break

window.Close()
