import mysql.connector as mariadb
from tkinter import *
from openpyxl import *
import shutil, os
from datetime import datetime, timedelta
from random import randrange
import logging
import os.path

meses={1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}

fechas={"semana 1":((1,0,0,0),(7,23,59,59)),"semana 2":((8,0,0,0),(14,23,59,59)),"semana 3":((15,0,0,0),(21,23,59,59)),"semana 4":((22,0,0,0),(28,23,59,59)),"semana 5":((29,0,0,0),(31,23,59,59))}

febrero=["febrero","Febrero"]

fotos=["FOTOS","fotos","Fotos"]

def orden66():
    tabla=tablaV.get()
    años=os.listdir(".")
    años.remove("ejecutablemariaDB.py")
    #años.remove("instrucciones.pdf")
    crear_carpetas_brutas()
    crear_carpetas_limpias()
    mesesalimpiar=mesesalimpiarV.get()
    mesesalimpiar=mesesalimpiar.split(";")
    aps={}
    for i in mesesalimpiar:
        i=i.split()
        aps[i[0]]=i[1].split("-")
    for año in años:
        for mes in os.listdir(".\\"+año):
            if año in aps:
                if mes not in aps[año]:
                    continue
            else:
                continue
            numeromes=0
            for i,j in meses.items():
                if j==mes:
                    numeromes=i
            lugares_maquinas={}
            for semana in os.listdir(".\\"+año+"\\"+mes):
                ruido=semana.split()
                fecha=ruido[2].split("-")
                ruido="Ruido tronaduras "+ruido[2]
                for ubicacion in os.listdir(".\\"+año+"\\"+mes+"\\"+semana+"\\"+ruido):
                    if ubicacion not in fotos:
                        for archivo in os.listdir(".\\"+año+"\\"+mes+"\\"+semana+"\\"+ruido+"\\"+ubicacion):
                            excel=archivo.split(".")
                            numero=len(excel)-1
                            tipo=excel[numero]
                            try:
                                nombre=excel[0].split("-")
                                lugari=nombre[0]
                                maquinai=nombre[1]
                                if tipo=="xls":
                                    try:
                                        lugares_maquinas[lugari].add(maquinai)
                                    except:
                                        lugares_maquinas[lugari]={maquinai}
                            except:
                                #print("error en archivo xls",archivo)
                                pass
            for lugar,maquinas in lugares_maquinas.items():
                for maquina in maquinas:
                    try: #en caso de que el archivo no existe
                        ruta=".\\"+año+"\\"+mes+"\\"+semana+"\\"+ruido+"\\"+lugar
                        archivoxls=lugar+"-"+maquina+".xls"
                        archivotxt=lugar+"-"+maquina+".txt"
                        if os.path.exists(archivoxls):
                            copiar_xls(archivo,ruta,tabla)#copio el archivo deseado en la tabla de la base de datos
                        elif os.path.exists(archivotxt):
                            copiar_txt(archivo,ruta,tabla)#copio el archivo deseado en la tabla de la base de datos
                    except:
                        print("el archivo",lugar+"-"+maquina+".xls", "no existe")
                        pass
            print("datos de",mes,"del año",año,"copiados en la tabla exitosamente")

    for año in años:
        for mes in os.listdir(".\\"+año):
            numeromes=0
            for i,j in meses.items():
                if j==mes:
                    numeromes=i
            lugares_maquinas={}
            for semana in os.listdir(".\\"+año+"\\"+mes):
                ruido=semana.split()
                fecha=ruido[2].split("-")
                ruido="Ruido tronaduras "+ruido[2]
                for ubicacion in os.listdir(".\\"+año+"\\"+mes+"\\"+semana+"\\"+ruido):
                    if ubicacion not in "FOTOS":
                        for archivo in os.listdir(".\\"+año+"\\"+mes+"\\"+semana+"\\"+ruido+"\\"+ubicacion):
                            excel=archivo.split(".")
                            numero=len(excel)-1
                            tipo=excel[numero]
                            try:
                                nombre=excel[0].split("-")
                                lugari=nombre[0]
                                maquinai=nombre[1]
                                if tipo=="xls":
                                    try:
                                        lugares_maquinas[lugari].add(maquinai)
                                    except:
                                        lugares_maquinas[lugari]={maquinai}
                            except:
                                #print("error en archivo xls",archivo)
                                pass
            for lugar,maquinas in lugares_maquinas.items():
                for maquina in maquinas:
                    for fechitas,tuplas in fechas.items():
                        if mes in febrero and fechitas=="semana 5":
                            if int(año)%4==0:
                                fecha_inicio=datetime(int(año),numeromes,tuplas[0][0],tuplas[0][1],tuplas[0][2],tuplas[0][3])
                                fecha_termino=datetime(int(año),numeromes,29,tuplas[1][1],tuplas[1][2],tuplas[1][3])
                            else:
                                continue
                        elif fechitas!="semana 5":
                            fecha_inicio=datetime(int(año),numeromes,tuplas[0][0],tuplas[0][1],tuplas[0][2],tuplas[0][3])
                            fecha_termino=datetime(int(año),numeromes,tuplas[1][0],tuplas[1][1],tuplas[1][2],tuplas[1][3])
                        else:
                            if mes not in febrero:
                                try:
                                    fecha_inicio=datetime(int(año),numeromes,tuplas[0][0],tuplas[0][1],tuplas[0][2],tuplas[0][3])
                                    fecha_termino=datetime(int(año),numeromes,tuplas[1][0],tuplas[1][1],tuplas[1][2],tuplas[1][3])
                                except:
                                    fecha_inicio=datetime(int(año),numeromes,tuplas[0][0],tuplas[0][1],tuplas[0][2],tuplas[0][3])
                                    fecha_termino=datetime(int(año),numeromes,30,tuplas[1][1],tuplas[1][2],tuplas[1][3])
                                    
                        crear_txt_bruto(lugar,maquina,año,mes,tabla,fecha_inicio,fecha_termino)
                        crear_txt_limpio(lugar,maquina,año,mes,tabla,fecha_inicio,fecha_termino)
    ventana_fin()
    #falta rellenar los archivos
                        




def crear_carpetas_brutas():
    años=os.listdir(".")
    os.mkdir("archivos brutos")
    años.remove("ejecutablemariaDB.py")
    #años.remove("instrucciones.pdf")
    febrero=["febrero","Febrero"]
    for i in años:
        os.mkdir("archivos brutos\\"+i)
        for j in os.listdir(".\\"+i):
            os.mkdir("archivos brutos\\"+i+"\\"+j)
            if j not in febrero:
                for k in range(5):
                    os.mkdir("archivos brutos\\"+i+"\\"+j+"\\"+"semana "+str(k+1))
            else:
                for k in range(4):
                    os.mkdir("archivos brutos\\"+i+"\\"+j+"\\"+"semana "+str(k+1))


def crear_carpetas_limpias():
    años=os.listdir(".")
    os.mkdir("archivos limpios")
    años.remove("ejecutablemariaDB.py")
    #años.remove("instrucciones.pdf")
    años.remove("archivos brutos")
    febrero=["febrero","Febrero"]
    for i in años:
        os.mkdir("archivos limpios\\"+i)
        for j in os.listdir(".\\"+i):
            os.mkdir("archivos limpios\\"+i+"\\"+j)
            if j not in febrero:
                for k in range(5):
                    os.mkdir("archivos limpios\\"+i+"\\"+j+"\\"+"semana "+str(k+1))
            else:
                for k in range(4):
                    os.mkdir("archivos limpios\\"+i+"\\"+j+"\\"+"semana "+str(k+1))



def semana_del_mes(fecha_inicio,fecha_termino):
    if fecha_inicio.day==1 and fecha_termino.day==7:
        x="1"
    elif fecha_inicio.day==8 and fecha_termino.day==14:
        x="2"
    elif fecha_inicio.day==15 and fecha_termino.day==21:
        x="3"
    elif fecha_inicio.day==22 and fecha_termino.day==28:
        x="4"
    elif fecha_inicio.day==29 and fecha_termino.day<=31:
        x="5"
    return(x)


def copiar_xls(archivo,ruta,tabla): #deberia poner quizas algo que referencie la tabla
    aaaa=archivo.split(".")
    lugar=aaaa[0].split("-")[0]
    maquina=aaaa[0].split("-")[1]
    
    ruta1 = ruta + os.sep
    origen = ruta1 + archivo 
    destino = ruta1 + 'copia.txt'
    try:
        archivo2 = shutil.copy2(origen, destino)
        #print("copiado")
    except:
        print('Error en la copia del archivo', archivo+",","este no existe" )

    # ¡¡¡¡¡MODIFICAR SIGUIENTE LINEA PARA CONECTAR AL SERVIDOR!!!!!
    mariadb_conexion = mariadb.connect(host='localhost', port='3307',user='omar', password='oherrera.1117', database='proyecto1')
    cursor = mariadb_conexion.cursor()

    
    archivo1=open(destino)
    nlinea=1
    verificador=0
    for linea in archivo1:
        if nlinea>3 :
            
            linea=linea.split()
            fechaa=linea[0]
            horaa=linea[2]
            #fechita=fechaa+"-"+linea[1]
            año=int(linea[0].split("/")[0])
            mes=linea[0].split("/")[1]
            dia=linea[0].split("/")[2]
            hora=linea[1].split(":")[0]
            minuto=linea[1].split(":")[1]
            segundo=""
            contadorS=0
            for i in linea[1].split(":")[2]:
                if contadorS<2:
                    segundo +=i
                contadorS+=1
            #segundo=int(segundo)
            #fecha=datetime(año,mes,dia,hora,minuto,segundo)  
            fechita=fechaa+"-"+hora+":"+minuto+":"+segundo

            
            #posfecha="A"+str(nfilas)
            #posdato1="B"+str(nfilas)
            #posdato2="C"+str(nfilas)
            #posdato3="D"+str(nfilas)
            #hoja[posfecha]=linea[0]+" - "+linea[1]
            #hoja[posdato1]=linea[2]
            #hoja[posdato2]=linea[3]
            #hoja[posdato3]=linea[4]
            

            #hago la consulta e ingreso la fila
            try:
                registro1 = "INSERT INTO {6} VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(lugar,maquina,fechita,linea[2],linea[3],linea[4],tabla)
                cursor.execute(registro1)
                #print(linea)
            
            except:
                #logging.exception("message")
                break #si hay un dato ya copiado, voy a dejar de copiar el archivo en la base de datos
                        
                        
        nlinea+=1
    archivo1.close()
    try:
        os.remove(destino)
    except:
        logging.exception("message")
        pass
    mariadb_conexion.commit()
    mariadb_conexion.close()
    print("datos de",archivo,"traspasados a base de datos, cuya ruta es", ruta)





def copiar_txt(archivo,ruta,tabla):
    aaaa=archivo.split(".")
    lugar=aaaa[0].split("-")[0]
    maquina=aaaa[0].split("-")[1]
    
    ruta1 = ruta + os.sep
    origen = ruta1 + archivo 
    
    # ¡¡¡¡¡MODIFICAR SIGUIENTE LINEA PARA CONECTAR AL SERVIDOR!!!!!
    mariadb_conexion = mariadb.connect(host='localhost', port='3307',user='omar', password='oherrera.1117', database='proyecto1')
    cursor = mariadb_conexion.cursor()

    
    archivo1=open(origen)
    nlinea=1
    for linea in archivo1:
        if nlinea>3 :
            linea=linea.split()
            fechaa=linea[0]
            horaa=linea[2]
            #fechita=fechaa+"-"+linea[1]
            año=int(fechaa.split("/")[0])
            mes=fechaa.split("/")[1]
            dia=fechaa.split("/")[2]
            hora=horaa.split(":")[0]
            minuto=linea[1].split(":")[1]
            segundo=""
            contadorS=0
            for i in linea[1].split(":")[2]:
                if contadorS<2:
                    segundo +=i
                contadorS+=1
            #fecha=datetime(año,mes,dia,hora,minuto,segundo) 
            fechita=fechaa+"-"+hora+":"+minuto+":"+segundo

            #hago la consulta e ingreso la fila
            try:
                registro1 = "INSERT INTO {6} VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(lugar,maquina,fechita,linea[2],linea[3],linea[4],tabla)
                cursor.execute(registro1)
                #print(linea)
            
            except:
                #logging.exception("message")
                break
        nlinea+=1
                
    archivo1.close()
    mariadb_conexion.commit()
    mariadb_conexion.close()
    print("datos de",archivo,"traspasados a base de datos")




    

def crear_txt_limpio(lugar,maquina,año,mes,tabla,fecha_inicio,fecha_termino):
    # ¡¡¡¡¡MODIFICAR SIGUIENTE LINEA PARA CONECTAR AL SERVIDOR!!!!!
    mariadb_conexion = mariadb.connect(host='localhost', port='3307',user='omar', password='oherrera.1117', database='proyecto1')
    cursor = mariadb_conexion.cursor()
    n=semana_del_mes(fecha_inicio,fecha_termino)
    if len(str(fecha_inicio.month))==1:
        mess="0"+str(fecha_inicio.month)
    else:
        mess=str(fecha_inicio.month)
    if len(str(fecha_inicio.day))==1:
        diai="0"+str(fecha_inicio.day)
    else:
        diai=str(fecha_inicio.day)
    if len(str(fecha_inicio.hour))==1:
        horai="0"+str(fecha_inicio.hour)
    else:
        horai=str(fecha_inicio.hour)
    if len(str(fecha_inicio.minute))==1:
        minutoi="0"+str(fecha_inicio.minute)
    else:
        minutoi=str(fecha_inicio.minute)
    if len(str(fecha_inicio.second))==1:
        segundoi="0"+str(fecha_inicio.second)
    else:
        segundoi=str(fecha_inicio.second)
    if len(str(fecha_termino.day))==1:
        diat="0"+str(fecha_termino.day)
    else:
        diat=str(fecha_termino.day)
    if len(str(fecha_termino.hour))==1:
        horat="0"+str(fecha_termino.hour)
    else:
        horat=str(fecha_termino.hour)
    if len(str(fecha_termino.minute))==1:
        minutot="0"+str(fecha_termino.minute)
    else:
        minutot=str(fecha_termino.minute)
    if len(str(fecha_termino.second))==1:
        segundot="0"+str(fecha_termino.second)
    else:
        segundot=str(fecha_termino.second)
    k=range(fecha_inicio.day,fecha_termino.day+1)
    k=list(map(str,k))
    #try:
    #orden="SELECT lugar,maquina,fecha,dato2 FROM `{10}` WHERE fecha>='{0}/{1}/{2}-{3}:{4}:{5}' and fecha<='{0}/{1}/{6}-{7}:{8}:{9}'".format(año,mess,diai,horai,minutoi,segundoi,diat,horat,minutot,segundot,tabla)
    orden="SELECT lugar,maquina,fecha,dato2 FROM `{11}` WHERE `fecha` LIKE '%{0}/{1}/{2}%' or 'fecha' LIKE '%{0}/{1}/{3}%' or 'fecha' LIKE '%{0}/{1}/{4}%' or 'fecha' LIKE '%{0}/{1}/{5}%' or 'fecha' LIKE '%{0}/{1}/{6}%' or 'fecha' LIKE '%{0}/{1}/{7}%' or 'fecha' LIKE '%{0}/{1}/{8}%' AND 'maquina'='{9}' AND 'lugar'='{10}' ".format(año,mess,diai,k[1],k[2],k[3],k[4],k[5],k[6],maquina,lugar,tabla)
    #print(orden)
    cursor.execute(orden)
    filas = cursor.fetchall()
    titulo=lugar+"-"+maquina+"-limpio.txt"
    archivo=open(titulo,'w')
    for fila in filas:
        contador=0
        fecha_anterior=datetime(1900,1,1,0,0,0)
        for i in fila:
            if contador==2:
                #archivo.write(i+" ")
                jiji=i
                i=i.split("-")
                lafecha=i[0].split("/")
                lafecha=list(map(int,lafecha))
                lahora=i[1].split(":")
                lahora=list(map(int,lahora))
                fecha_actual=datetime(lafecha[0],lafecha[1],lafecha[2],lahora[0],lahora[1],lahora[2])
                diferencia=fecha_actual-fecha_anterior
                dif=diferencia.seconds+diferencia.days*3600*24
                if dif>1 and fecha_anterior!=datetime(1900,1,1,0,0,0):
                    #tengo que rellenar aqui
                    if dif>2:
                        for i in range(dif-2):
                            fechaa=fecha_actual+timedelta(0,1)
                            fechaa=str(fechaa).replace("-","/").replace(" "," - ")
                            archivo.write(fechaa+" "+str(dato_anterior+randrange(1,5))+"\n") #AQUI RELLENO DATOS, CAMBIAR LIMITES DE RANDRANGE SI SE DESEA
                        archivo.write(jiji+" ")
                    else:
                        fechaa=fecha_actual+timedelta(0,1)
                        fechaa=str(fechaa).replace("-","/").replace(" "," - ")
                        archivo.write(fechaa+" "+str(dato_anterior+randrange(1,5))+"\n") #AQUI RELLENO DATOS, CAMBIAR LIMITES DE RANDRANGE SI SE DESEA
                        archivo.write(jiji+" ")
                else:
                    archivo.write(i+" ")
                    dato_anterior=float(i) #asumo que este dato viene como string
            if contador==3:
                archivo.write(str(i)+"\n") #escribo dato
            contador+=1
    archivo.close()
    shutil.move(".\\"+titulo,".\\archivos limpios\\"+año+"\\"+mes+"\\semana "+n)

    mariadb_conexion.commit()
    mariadb_conexion.close()

    print("archivo limpio de ", lugar+"-"+maquina," de la semana "+n,"de",mes,"del",año,"creado y movido donde corresponde")
    #except:
        #pass



def crear_txt_bruto(lugar,maquina,año,mes,tabla,fecha_inicio,fecha_termino):
    # ¡¡¡¡¡MODIFICAR SIGUIENTE LINEA PARA CONECTAR AL SERVIDOR!!!!!
    mariadb_conexion = mariadb.connect(host='localhost', port='3307',user='omar', password='oherrera.1117', database='proyecto1')
    cursor = mariadb_conexion.cursor()
    n=semana_del_mes(fecha_inicio,fecha_termino)
    if len(str(fecha_inicio.month))==1:
        mess="0"+str(fecha_inicio.month)
    else:
        mess=str(fecha_inicio.month)
    if len(str(fecha_inicio.day))==1:
        diai="0"+str(fecha_inicio.day)
    else:
        diai=str(fecha_inicio.day)
    if len(str(fecha_inicio.hour))==1:
        horai="0"+str(fecha_inicio.hour)
    else:
        horai=str(fecha_inicio.hour)
    if len(str(fecha_inicio.minute))==1:
        minutoi="0"+str(fecha_inicio.minute)
    else:
        minutoi=str(fecha_inicio.minute)
    if len(str(fecha_inicio.second))==1:
        segundoi="0"+str(fecha_inicio.second)
    else:
        segundoi=str(fecha_inicio.second)
    if len(str(fecha_termino.day))==1:
        diat="0"+str(fecha_termino.day)
    else:
        diat=str(fecha_termino.day)
    if len(str(fecha_termino.hour))==1:
        horat="0"+str(fecha_termino.hour)
    else:
        horat=str(fecha_termino.hour)
    if len(str(fecha_termino.minute))==1:
        minutot="0"+str(fecha_termino.minute)
    else:
        minutot=str(fecha_termino.minute)
    if len(str(fecha_termino.second))==1:
        segundot="0"+str(fecha_termino.second)
    else:
        segundot=str(fecha_termino.second)
    k=range(fecha_inicio.day,fecha_termino.day+1)
    k=list(map(str,k))
    #try:
    #orden="SELECT lugar,maquina,fecha,dato2 FROM `{10}` WHERE fecha>='{0}/{1}/{2}-{3}:{4}:{5}' and fecha<='{0}/{1}/{6}-{7}:{8}:{9}'".format(año,mess,diai,horai,minutoi,segundoi,diat,horat,minutot,segundot,tabla)
    orden="SELECT lugar,maquina,fecha,dato2 FROM `{11}` WHERE `fecha` LIKE '%{0}/{1}/{2}%' or 'fecha' LIKE '%{0}/{1}/{3}%' or 'fecha' LIKE '%{0}/{1}/{4}%' or 'fecha' LIKE '%{0}/{1}/{5}%' or 'fecha' LIKE '%{0}/{1}/{6}%' or 'fecha' LIKE '%{0}/{1}/{7}%' or 'fecha' LIKE '%{0}/{1}/{8}%' AND 'maquina'='{9}' AND 'lugar'='{10}' ".format(año,mess,diai,k[1],k[2],k[3],k[4],k[5],k[6],maquina,lugar,tabla)
    #print(orden)
    cursor.execute(orden)
    filas = cursor.fetchall()
    titulo=lugar+"-"+maquina+"-limpio.txt"
    archivo=open(titulo,'w')
    for fila in filas:
        contador=0
        fecha_anterior=datetime(1900,1,1,0,0,0)
        for i in fila:
            if contador==2:
                #archivo.write(i+" ")
                jiji=i
                i=i.split("-")
                lafecha=i[0].split("/")
                lafecha=list(map(int,lafecha))
                lahora=i[1].split(":")
                lahora=list(map(int,lahora))
                fecha_actual=datetime(lafecha[0],lafecha[1],lafecha[2],lahora[0],lahora[1],lahora[2])
                diferencia=fecha_actual-fecha_anterior
                dif=diferencia.seconds+diferencia.days*3600*24
                if dif>1 and fecha_anterior!=datetime(1900,1,1,0,0,0):
                    #tengo que rellenar aqui
                    if dif>2:
                        for i in range(dif-2):
                            fechaa=fecha_actual+timedelta(0,1)
                            fechaa=str(fechaa).replace("-","/").replace(" "," - ")
                            archivo.write(fechaa+" "+str(dato_anterior+randrange(1,5))+"\n") #AQUI RELLENO DATOS, CAMBIAR LIMITES DE RANDRANGE SI SE DESEA
                        archivo.write(jiji+" ")
                    else:
                        fechaa=fecha_actual+timedelta(0,1)
                        fechaa=str(fechaa).replace("-","/").replace(" "," - ")
                        archivo.write(fechaa+" "+str(dato_anterior+randrange(1,5))+"\n") #AQUI RELLENO DATOS, CAMBIAR LIMITES DE RANDRANGE SI SE DESEA
                        archivo.write(jiji+" ")
                else:
                    archivo.write(i+" ")
                    dato_anterior=float(i) #asumo que este dato viene como string
            if contador==3:
                archivo.write(str(i)+"\n") #escribo dato
            contador+=1
    archivo.close()
    shutil.move(".\\"+titulo,".\\archivos brutos\\"+año+"\\"+mes+"\\semana "+n)
    
    mariadb_conexion.commit()
    mariadb_conexion.close()

    print("archivo bruto de ", lugar+"-"+maquina," de la semana "+n,"de",mes,"del",año,"creado y movido donde corresponde")
    #except:
        #pass

def crear_txt_limpio2(lugar,maquina,año,mes,tabla,fecha_inicio,fecha_termino):
    # ¡¡¡¡¡MODIFICAR SIGUIENTE LINEA PARA CONECTAR AL SERVIDOR!!!!!
    mariadb_conexion = mariadb.connect(host='localhost', port='3307',user='omar', password='oherrera.1117', database='proyecto1')
    cursor = mariadb_conexion.cursor()
    if len(str(fecha_inicio.month))==1:
        mess="0"+str(fecha_inicio.month)
    else:
        mess=str(fecha_inicio.month)
    if len(str(fecha_inicio.day))==1:
        diai="0"+str(fecha_inicio.day)
    else:
        diai=str(fecha_inicio.day)
    if len(str(fecha_inicio.hour))==1:
        horai="0"+str(fecha_inicio.hour)
    else:
        horai=str(fecha_inicio.hour)
    if len(str(fecha_inicio.minute))==1:
        minutoi="0"+str(fecha_inicio.minute)
    else:
        minutoi=str(fecha_inicio.minute)
    if len(str(fecha_inicio.second))==1:
        segundoi="0"+str(fecha_inicio.second)
    else:
        segundoi=str(fecha_inicio.second)
    if len(str(fecha_termino.day))==1:
        diat="0"+str(fecha_termino.day)
    else:
        diat=str(fecha_termino.day)
    if len(str(fecha_termino.hour))==1:
        horat="0"+str(fecha_termino.hour)
    else:
        horat=str(fecha_termino.hour)
    if len(str(fecha_termino.minute))==1:
        minutot="0"+str(fecha_termino.minute)
    else:
        minutot=str(fecha_termino.minute)
    if len(str(fecha_termino.second))==1:
        segundot="0"+str(fecha_termino.second)
    else:
        segundot=str(fecha_termino.second)
    k=range(fecha_inicio.day,fecha_termino.day+1)
    k=list(map(str,k))
    #try:
    #orden="SELECT lugar,maquina,fecha,dato2 FROM `{10}` WHERE fecha>='{0}/{1}/{2}-{3}:{4}:{5}' and fecha<='{0}/{1}/{6}-{7}:{8}:{9}'".format(año,mess,diai,horai,minutoi,segundoi,diat,horat,minutot,segundot,tabla)
    orden="SELECT lugar,maquina,fecha,dato2 FROM `{11}` WHERE `fecha` LIKE '%{0}/{1}/{2}%' or 'fecha' LIKE '%{0}/{1}/{3}%' or 'fecha' LIKE '%{0}/{1}/{4}%' or 'fecha' LIKE '%{0}/{1}/{5}%' or 'fecha' LIKE '%{0}/{1}/{6}%' or 'fecha' LIKE '%{0}/{1}/{7}%' or 'fecha' LIKE '%{0}/{1}/{8}%' AND 'maquina'='{9}' AND 'lugar'='{10}' ".format(año,mess,diai,k[1],k[2],k[3],k[4],k[5],k[6],maquina,lugar,tabla)
    #print(orden)
    cursor.execute(orden)
    filas = cursor.fetchall()
    titulo=lugar+"-"+maquina+"-limpio.txt"
    archivo=open(titulo,'w')
    for fila in filas:
        contador=0
        fecha_anterior=datetime(1900,1,1,0,0,0)
        for i in fila:
            if contador==2:
                #archivo.write(i+" ")
                jiji=i
                i=i.split("-")
                lafecha=i[0].split("/")
                lafecha=list(map(int,lafecha))
                lahora=i[1].split(":")
                lahora=list(map(int,lahora))
                fecha_actual=datetime(lafecha[0],lafecha[1],lafecha[2],lahora[0],lahora[1],lahora[2])
                diferencia=fecha_actual-fecha_anterior
                dif=diferencia.seconds+diferencia.days*3600*24
                if dif>1 and fecha_anterior!=datetime(1900,1,1,0,0,0):
                    #tengo que rellenar aqui
                    if dif>2:
                        for i in range(dif-2):
                            fechaa=fecha_actual+timedelta(0,1)
                            fechaa=str(fechaa).replace("-","/").replace(" "," - ")
                            archivo.write(fechaa+" "+str(dato_anterior+randrange(1,5))+"\n") #AQUI RELLENO DATOS, CAMBIAR LIMITES DE RANDRANGE SI SE DESEA
                        archivo.write(jiji+" ")
                    else:
                        fechaa=fecha_actual+timedelta(0,1)
                        fechaa=str(fechaa).replace("-","/").replace(" "," - ")
                        archivo.write(fechaa+" "+str(dato_anterior+randrange(1,5))+"\n") #AQUI RELLENO DATOS, CAMBIAR LIMITES DE RANDRANGE SI SE DESEA
                        archivo.write(jiji+" ")
                else:
                    archivo.write(i+" ")
                    dato_anterior=float(i) #asumo que este dato viene como string
            if contador==3:
                archivo.write(str(i)+"\n") #escribo dato
            contador+=1
    archivo.close()
    #shutil.move(".\\"+titulo,".\\archivos limpios\\"+año+"\\"+mes+"\\semana "+n)

    mariadb_conexion.commit()
    mariadb_conexion.close()

    print("limpio listo")
    #print("archivo limpio de ", lugar+"-"+maquina,"desde",str(fecha_inicio),"hasta",+str(fecha_termino),"creado")
    #except:
        #pass


def crear_txt_bruto2(lugar,maquina,año,mes,tabla,fecha_inicio,fecha_termino):
    # ¡¡¡¡¡MODIFICAR SIGUIENTE LINEA PARA CONECTAR AL SERVIDOR!!!!!
    mariadb_conexion = mariadb.connect(host='localhost', port='3307',user='omar', password='oherrera.1117', database='proyecto1')
    cursor = mariadb_conexion.cursor()
    if len(str(fecha_inicio.month))==1:
        mess="0"+str(fecha_inicio.month)
    else:
        mess=str(fecha_inicio.month)
    if len(str(fecha_inicio.day))==1:
        diai="0"+str(fecha_inicio.day)
    else:
        diai=str(fecha_inicio.day)
    if len(str(fecha_inicio.hour))==1:
        horai="0"+str(fecha_inicio.hour)
    else:
        horai=str(fecha_inicio.hour)
    if len(str(fecha_inicio.minute))==1:
        minutoi="0"+str(fecha_inicio.minute)
    else:
        minutoi=str(fecha_inicio.minute)
    if len(str(fecha_inicio.second))==1:
        segundoi="0"+str(fecha_inicio.second)
    else:
        segundoi=str(fecha_inicio.second)
    if len(str(fecha_termino.day))==1:
        diat="0"+str(fecha_termino.day)
    else:
        diat=str(fecha_termino.day)
    if len(str(fecha_termino.hour))==1:
        horat="0"+str(fecha_termino.hour)
    else:
        horat=str(fecha_termino.hour)
    if len(str(fecha_termino.minute))==1:
        minutot="0"+str(fecha_termino.minute)
    else:
        minutot=str(fecha_termino.minute)
    if len(str(fecha_termino.second))==1:
        segundot="0"+str(fecha_termino.second)
    else:
        segundot=str(fecha_termino.second)

    k=range(fecha_inicio.day,fecha_termino.day+1)
    k=list(map(str,k))
    #try:
    #orden="SELECT lugar,maquina,fecha,dato2 FROM `{10}` WHERE fecha>='{0}/{1}/{2}-{3}:{4}:{5}' and fecha<='{0}/{1}/{6}-{7}:{8}:{9}'".format(año,mess,diai,horai,minutoi,segundoi,diat,horat,minutot,segundot,tabla)
    orden="SELECT lugar,maquina,fecha,dato2 FROM `{11}` WHERE `fecha` LIKE '%{0}/{1}/{2}%' or 'fecha' LIKE '%{0}/{1}/{3}%' or 'fecha' LIKE '%{0}/{1}/{4}%' or 'fecha' LIKE '%{0}/{1}/{5}%' or 'fecha' LIKE '%{0}/{1}/{6}%' or 'fecha' LIKE '%{0}/{1}/{7}%' or 'fecha' LIKE '%{0}/{1}/{8}%' AND 'maquina'='{9}' AND 'lugar'='{10}' ".format(año,mess,diai,k[1],k[2],k[3],k[4],k[5],k[6],maquina,lugar,tabla)
    #print(orden)
    cursor.execute(orden)
    filas = cursor.fetchall()
    titulo=lugar+"-"+maquina+"-bruto.txt"
    archivo=open(titulo,'w')
    for fila in filas:
        contador=0
        fecha_anterior=datetime(1900,1,1,0,0,0)
        for i in fila:
            if contador==2:
                #archivo.write(i+" ")
                jiji=i
                i=i.split("-")
                lafecha=i[0].split("/")
                lafecha=list(map(int,lafecha))
                lahora=i[1].split(":")
                lahora=list(map(int,lahora))
                fecha_actual=datetime(lafecha[0],lafecha[1],lafecha[2],lahora[0],lahora[1],lahora[2])
                diferencia=fecha_actual-fecha_anterior
                dif=diferencia.seconds+diferencia.days*3600*24
                if dif>1 and fecha_anterior!=datetime(1900,1,1,0,0,0):
                    #tengo que rellenar aqui
                    if dif>2:
                        for i in range(dif-2):
                            fechaa=fecha_actual+timedelta(0,1)
                            fechaa=str(fechaa).replace("-","/").replace(" "," - ")
                            archivo.write(fechaa+" "+str(dato_anterior+randrange(1,5))+"\n") #AQUI RELLENO DATOS, CAMBIAR LIMITES DE RANDRANGE SI SE DESEA
                        archivo.write(jiji+" ")
                    else:
                        fechaa=fecha_actual+timedelta(0,1)
                        fechaa=str(fechaa).replace("-","/").replace(" "," - ")
                        archivo.write(fechaa+" "+str(dato_anterior+randrange(1,5))+"\n") #AQUI RELLENO DATOS, CAMBIAR LIMITES DE RANDRANGE SI SE DESEA
                        archivo.write(jiji+" ")
                else:
                    archivo.write(i+" ")
                    dato_anterior=float(i) #asumo que este dato viene como string
            if contador==3:
                archivo.write(str(i)+"\n") #escribo dato
            contador+=1
    archivo.close()
    #shutil.move(".\\"+titulo,".\\archivos limpios\\"+año+"\\"+mes+"\\semana "+n)
    
    mariadb_conexion.commit()
    mariadb_conexion.close()

    print("bruto listo")
    #print("archivo bruto de ", lugar+"-"+maquina,"desde",str(fecha_inicio),"hasta",+str(fecha_termino),"creado")
    #except:
        #pass





def limpiar_uno():
    tabla=tablaV.get()
    lugar=puntoV.get()
    maquina=modeloV.get()
    lugar=lugar.upper()
    maquina=maquina.upper()
    fi=fiV.get()
    fi=fi.split()
    
    fechai=fi[0].split("/")
    añoi=int(fechai[0])
    mesi=int(fechai[1])
    diai=int(fechai[2])
    horai=fi[2].split(":")
    horaii=int(horai[0])
    minutoi=int(horai[1])
    segundoi=int(horai[2])
    fecha_inicio=datetime(añoi,mesi,diai,horaii,minutoi,segundoi)
    
    ft=ftV.get()
    ft=ft.split()
    
    fechat=ft[0].split("/")
    añot=int(fechat[0])
    mest=int(fechat[1])
    diat=int(fechat[2])
    horat=ft[2].split(":")
    horatt=int(horat[0])
    
    minutot=int(horat[1])
    segundot=int(horat[2])
    fecha_termino=datetime(añot,mest,diat,horatt,minutot,segundot)
    
    
    mes=meses[mesi]
    año=str(añoi)

    
    
    crear_txt_bruto2(lugar,maquina,año,mes,tabla,fecha_inicio,fecha_termino)
    crear_txt_limpio2(lugar,maquina,año,mes,tabla,fecha_inicio,fecha_termino)
    print("archivos limpio y brutos creados")
    ventana_fin()









def ventana_fin():
    ventana2=Tk()
    ventana2.title("Proceso finalizado")
    etiqueta=Label(ventana2,text="Los archivos han sido analizados y limpiados").grid(row=0,column=0)
    ejecutar=Button(ventana2, text="Cerrar", command=ventana2.destroy).grid(row=1,column=0)
    ventana2.mainloop()





#Ventana:
ventana=Tk()
ventana.title("Filtro de datos")


#Variables:
puntoV=StringVar()
modeloV=StringVar()
fiV=StringVar()
ftV=StringVar()
mesesalimpiarV=StringVar()
tablaV=StringVar()

#Etiquetas:
tabla=Label(ventana,text="ingrese tabla").grid(row=0,column=0)
etiqueta=Label(ventana,text="Ingrese datos:").grid(row=1,column=0)
punto=Label(ventana,text="Punto:").grid(row=2,column=0)
modelo=Label(ventana,text="Modelo:").grid(row=3,column=0)
fi=Label(ventana,text="fecha inicio (y/m/d - h:m:s):").grid(row=4,column=0)
ft=Label(ventana,text="fecha término (y/m/d - h:m:s):").grid(row=5,column=0)
mesesalimpiar=Label(ventana,text="meses a limpiar:").grid(row=7,column=0)


#Entradas:
tablaVcaja=Entry(ventana,textvariable=tablaV).grid(row=0,column=1)
puntoVcaja=Entry(ventana,textvariable=puntoV).grid(row=2,column=1)
modeloVcaja=Entry(ventana,textvariable=modeloV).grid(row=3,column=1)
fiVcaja=Entry(ventana,textvariable=fiV).grid(row=4,column=1)
ftVcaja=Entry(ventana,textvariable=ftV).grid(row=5,column=1)
mesesalimpiarVcaja=Entry(ventana,textvariable=mesesalimpiarV).grid(row=7,column=1)



#botones:
ejecutar=Button(ventana, text="Limpieza total", command=orden66).grid(row=8,column=0)
limpiar=Button(ventana, text="Limpieza individual", command=limpiar_uno).grid(row=6,column=0)

ventana.mainloop()
