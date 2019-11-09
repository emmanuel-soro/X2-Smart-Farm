""" Para el desarrollo del procesamiento de imagenes, se opto utilizar la libreria OPENCV (desarrollada por intel)
    dado que se encuentra muy bien optimizada. Se obtuvieron tiempos de procesamiento mucho mas bajos que los algoritmos
    implementados con la libreria Image. 
    SW utilizado:
        -IDE Eclipse
        -Python 3.7.5
        -Libreria opencv 4.1.1"""

import time #Para saber tiempo de procesamiento
import cv2
import numpy as np

# DECLARACION DE FUNCIONES

def reducir_ruido_gauss(rutaRoot, imgName):
    
    """ Esta funcion lo que hace es reducir el ruido de la imagen en cuanto a los pixeles,
        el objetivo es quitar detalles que no son de importancia y que generan conflictos. """
        
    img = cv2.imread(rutaRoot + imgName)
    img_sinRuido = cv2.GaussianBlur(img,(5,5),0)
    cv2.imwrite(rutaRoot + "sinruido.jpg", img_sinRuido)

def separar_verde(rutaRoot, imgName):
    
    """ Esta funcion recorta los pixeles que se encuentran en la gama del verde. Lo que
        no se encuentre en dicha gama, se pisa con negro. """
        
    img = cv2.imread(rutaRoot + imgName) 
    #Convertimos a hsv 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #El verde se encuentra entre (36,25,25) y (86, 255,255) aprox
    mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    #Sacamos solo lo que no este dentro del rango verde 
    imask = mask>0 
    green = np.zeros_like(img, np.uint8) 
    green[imask] = img[imask] 
    #Guardamos 
    cv2.imwrite(rutaRoot + "soloverde.jpg", green)

def escalado_a_grises_y_bin(rutaRoot, imgName):
    
    """ Esta funcion pasa la imagen de color RBG a una escala de grises. Luego, se binariza
        la imagen con un umbral determinado. El umbral fue calculado de manera experimental,
        realizando pruebas con distintos umbrales y determinando el mas apropiado. """
        
    umbral = 27.8
    umbralMax = 255
    gray = cv2.imread(rutaRoot + imgName, cv2.IMREAD_GRAYSCALE)
    t, dst = cv2.threshold(gray, umbral, umbralMax, cv2.THRESH_BINARY)
    cv2.imwrite(rutaRoot + "binarizada.jpg", dst)
    cv2.imwrite(rutaRoot + "a_grises.jpg", gray)

def obtener_cantidad_blanco(rutaRoot, imgName):
    
    """ Esta funcion cuenta la cantidad de pixeles en blanco y devuelve el porcentaje
        de pixeles blancos contra el total de pixeles de la imagen. """
        
    img = cv2.imread(rutaRoot + imgName, 0)
    #cv2.imwrite(rutaRoot + "imagenPrueba.jpg", img)
    cant_pix_blancos = cv2.countNonZero(img) #Obtengo la cantidad de pixeles blancos
    cant_pix_totales = img.size
    print("Cantidad de pixeles blancos:", cant_pix_blancos)
    print("Cantidad total de pixeles:", cant_pix_totales)
    return (cant_pix_blancos * 100) / cant_pix_totales


def procesar_imagen(ruta):
    
    #Separamos verde
    img = cv2.imread(ruta) 
    #Convertimos a hsv 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #El verde se encuentra entre (36,25,25) y (86, 255,255) aprox
    mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    #Sacamos solo lo que no este dentro del rango verde 
    imask = mask>0 
    green = np.zeros_like(img, np.uint8) 
    green[imask] = img[imask] 
    
    #Reducimos ruido con el metodo de gauss
      
    img_sinRuido = cv2.GaussianBlur(green,(5,5),0)

    #Escalamos a grises y binarizamos
    
    umbral = 27.8
    umbralMax = 255
    gray = cv2.cvtColor(img_sinRuido, cv2.COLOR_BGRA2GRAY)
    t, binaria = cv2.threshold(gray, umbral, umbralMax, cv2.THRESH_BINARY)
    
    #Obtenemos follaje por la relacion pixesles blancos (verde) con negros

    cant_pix_blancos = cv2.countNonZero(binaria) #Obtengo la cantidad de pixeles blancos
    cant_pix_totales = binaria.size
    print("Cantidad de pixeles blancos:", cant_pix_blancos)
    print("Cantidad total de pixeles:", cant_pix_totales)
    
    #Retornamos el % de follaje
    
    return (cant_pix_blancos * 100) / cant_pix_totales


# FIN DECLARACION DE FUNCIONES.

# FUNCION MAIN

""" Se produciran las imagenes paso por paso. Esto tiene solo uso para realizar tests y evidenciar que
    esta haciendo el algoritmo de procesamiento. """

#Para saber tiempo de procesamiento
tiempoIn = time.time() 

#Sera la ruta a donde se encuentra la imagen
ruta = "C:/Users/rnsal/Documents/imagenes/" 
#Nombre de la imagen a procesar
imgName = "img.jpg"

#Main paso por paso

print("********COMENZANDO********")
separar_verde(ruta, imgName) 
print("******FINALIZANDO SEPARAR VERDE******")
reducir_ruido_gauss(ruta, "soloverde.jpg")
print("******FINALIZANDO REDUCIR RUIDO CON METODO GAUSSIANO*******")
escalado_a_grises_y_bin(ruta, "soloverde.jpg")
print("********FINALIZANDO ESCALADO A GRISES Y POSTERIOR BINARIZACION CON UMBRAL********")
nvl_follaje_porc = obtener_cantidad_blanco(ruta , "binarizada.jpg")
print("El nivel de follaje es de", nvl_follaje_porc, "%")

#Main final

print("El nivel de follaje es de", procesar_imagen(ruta + imgName), "%.")

#Para Saber tiempo de procesamiento
tiempoFin = time.time()
print('El Proceso Tardo: ', tiempoFin - tiempoIn, 'Segundos')

# FIN FUNCION MAIN