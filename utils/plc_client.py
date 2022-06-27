import socket
import time
import random as rnd
from datetime import datetime
from colorama import Fore, Style

'''
SIMULATORE socket di PLC

socket ad utilizzo di test come sostituto al PLC.
Invia messaggi ogni tot di tempo randomico
    
'''

global IP_SERVER = "127.0.0.1"
global PORT_SERVER = 1234
    
    
def testing_socket(ip = "127.0.0.1", port=1234):
    # parametri per generare intervalli di tempo per simulare il socket PLC
    minimo_intervallo_di_secondi = 2
    massimo_intervallo_di_secondi = 5
    intervallo_di_secondi_per_disconnessione = 2

    while True: # all'infinito
        
        # messaggio randomico per simulare il messaggio PLC
        MESSAGE = bytes('f,' +str(rnd.randint(1,100))+',' +str(rnd.randint(1,100)),'utf-8') 
        
        # estrai orario di adesso
        current_time = datetime.now().strftime("%H:%M:%S")

        try:
            # inizializza il socket con IPv4 e straming socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # connetti il socket al server della applicazione
            sock.connect((ip, port))

            # manda un messaggio test
            sock.send(MESSAGE)

            # dormi un numero randomico di secondi
            time.sleep( rnd.randint(minimo_intervallo_di_secondi, massimo_intervallo_di_secondi+1))
            
            # chiudi il socket
            sock.close()

            # stampa logs
            print('🆗 '+ Fore.GREEN +' [running socket]'+ Style.RESET_ALL+' al server IP: '+IP_SERVER+':'+str(PORT_SERVER)+'  messaggio: ' + Fore.BLUE  +str(MESSAGE)  + Style.RESET_ALL + ' alle ore '+  Fore.YELLOW  +str(current_time) + Style.RESET_ALL)

        except: 
            # quando succede un qualsiasi errore eseguisci le linee qui sotto 
            print(' 🔥','[',Fore.RED +current_time+Style.RESET_ALL,'] Errore: connessione al server non riuscita') 
            time.sleep(intervallo_di_secondi_per_disconnessione)


if __name__ == "__main__":
    testing_socket(IP_SERVER,PORT_SERVER)
 
    
