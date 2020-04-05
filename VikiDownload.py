#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 00:30:05 2020

@author: sebastianmoyano
"""

import requests
import re
from bs4 import BeautifulSoup
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
    
mainpage=input("ingrese link general, (eg. https://www.viki.com/tv/34479c-fight-my-way?locale=es):  ")    
newr=requests.get(mainpage)
soup=BeautifulSoup(newr.text,features="html.parser")
epis=soup.findAll('small',{'class','item-count'})
link=soup.findAll('div',{'class','row-inline episode-widget'})
link=link[0].a['href']
important="-".join(link.split("-")[1:-1])
print(link)
numero=int(link.split('/')[-1].split("-")[0][:-1])

titulo_serie=soup.h1.text.strip()

for x in range(0,int(epis[0].text)):
    link=important +"-"+str(x+1)
    
    auxiliar=numero+x
  
    linkarreglado='https://www.viki.com/videos/'+str(auxiliar)+'v-'+link
    print(linkarreglado)
    lastbit=linkarreglado.split("/")[-1]
    number=lastbit.split('-')[0]
    
    r = requests.get('https://www.tubeoffline.com/downloadFrom.php?host=Viki&video=https%3A%2F%2Fwww.viki.com%2Fvideos%2F'+lastbit)
    print("\nlink a convertir: "+'https://www.tubeoffline.com/downloadFrom.php?host=Viki&video=https%3A%2F%2Fwww.viki.com%2Fvideos%2F'+lastbit)
    allVids=re.findall(r'_high_(.*?)\"',r.text)
    print("\nfound:",len(allVids)," in total")
    Linkvideo= "https://v4.viki.io/"+number+"/"+number+"_high_"+allVids[-1]
    print("\nLink Video: ", Linkvideo)
    print("\nDescargando Video...\n")
    descargar(requests.get(Linkvideo),titulo_serie,titulo_serie+" s01e"+str(x+1)+".mp4")
        
    subs = re.search(r'es.srt\?(.*?)\"',r.text)
    text="https://api.viki.io/v4/videos/" + number+"/subtitles/es.srt?"+subs.group(1)
    print("\nsubtitulos: ",text)
    print("\nDescargando subtitulos...\n")
    descargar(requests.get(text),titulo_serie,titulo_serie+" s01e"+str(x+1)+".spa.srt")
  
    
    
    
