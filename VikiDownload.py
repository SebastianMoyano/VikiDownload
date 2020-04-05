#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 00:30:05 2020

@author: sebastianmoyano
"""

import requests
import re
# from bs4 import BeautifulSoup
import os
import sys



def descargar(r,nombre,episodio):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    
    lugar=application_path
    nuevo=os.path.join(lugar,nombre)
    season=os.path.join(nuevo,'Season 01')
    if not os.path.exists(season):
        os.makedirs(season)
    print("\nSe descargara en: "+season)
    print("\nComenzando Descarga\n")
    with open(os.path.join(season,episodio), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024*2):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)                
    print("\nDescarga terminada\n")
    
mainpage=input("\nIngrese link, ( eg. https://www.viki.com/videos/1118519v-fight-my-way-episode-1 ):  ")   

serie=mainpage.split('/')[-1]
partes=serie.split("-")
numero=int(partes[0][:-1])
epi=int(partes[-1])
important="-".join(mainpage.split("-")[1:-1])
titulo_serie=" ".join(mainpage.split("-")[1:-2])
loop = 0
s = requests.Session()
while True:
    
    linkarreglado='https://www.viki.com/videos/'+str(numero + loop)+'v-'+important+"-"+str(loop+epi)

    lastbit=linkarreglado.split("/")[-1]
    number=lastbit.split('-')[0]
    newr=s.get(linkarreglado)
    print(8*"#"+"  DESCARGANDO {} {} ".format(titulo_serie,loop+epi)+"#"*8)
    if newr.status_code != 200:
        break
    r = s.get('https://www.tubeoffline.com/downloadFrom.php?host=Viki&video=https%3A%2F%2Fwww.viki.com%2Fvideos%2F'+lastbit)
    print("\nlink a convertir: "+'https://www.tubeoffline.com/downloadFrom.php?host=Viki&video=https%3A%2F%2Fwww.viki.com%2Fvideos%2F'+lastbit)
    allVids=re.findall(r'_high_(.*?)\"',r.text)
    print("\nEncontrados:",len(allVids),"videos en total, eligiendo la mejor calidad")
    Linkvideo= "https://v4.viki.io/"+number+"/"+number+"_high_"+allVids[-1]
    print("\nCargando Video: ", Linkvideo)
    video=s.get(Linkvideo)
    print("\nDescargando Video...\n")
    descargar(video,titulo_serie,titulo_serie+" s01e"+str(loop+epi)+".mp4")
        
    subs = re.search(r'es.srt\?(.*?)\"',r.text)
    text="https://api.viki.io/v4/videos/" + number+"/subtitles/es.srt?"+subs.group(1)
    print("\nsubtitulos esp: ",text)
    print("\nDescargando subtitulos...\n")
    descargar(s.get(text),titulo_serie,titulo_serie+" s01e"+str(loop+epi)+".spa.srt")
    loop += 1    
    

    
    
    
