import socket
# SERVER app.py
IP_SERVER = "192.168.1.84"
IP_SERVER = socket.gethostname()
# CLIENT PLC
IP_PLC = "192.168.1.84"
IP_PLC = socket.gethostname()

PORTA_SERVER = 9101
PORTA_PLC = 9102
# il numero di porta può essere compreso tra 0-65535 (di solito le porte non privilegiate sono > 1023)

# PARAMETRI
KEY_USB = 0 # porta USB videocamera

RISOLUZIONE = (4295,2864) # 12.3 mega pixel

# metti un numero > 1 per diminuire la risoluzione  
# potrebbe crashare con numero minore di 10
fattore_bassa_risoluzione = 15 


nome_pannello_di_controllo = "Pannello di Controllo"

nome_pannello_di_visualizzazione = "Computer Vision System di Systematik s.r.l."

LOGO ="""
  _____                     __         
 / ___/__  __ _  ___  __ __/ /____ ____
/ /__/ _ \/  ' \/ _ \/ // / __/ -_) __/
\___/\___/_/_/_/ .__/\_,_/\__/\__/_/   
              /_/                      
  _   ___     _                        
 | | / (_)__ (_)__  ___                
 | |/ / (_-</ / _ \/ _ \               
 |___/_/___/_/\___/_//_/               

    Systematik s.r.l. 

"""

descrizione ='''
 Applicazione di Computer Vision
    1. inizializza il server
    2. aspetta il messaggio da client plc con socket con ID ricetta e ID pezzo
    3. scatta una foto e salvala
    4. elabora la foto rilevando i difetti
    5. ritorna la foto elaborata in una cartella
    6. ritorna lo status (presenza di errori) e l'ID del pezzo
'''