import socket
import time
import random as rnd
from datetime import datetime
from colorama import Fore, Style
from params import IP_SERVER, PORTA_SERVER, IP_PLC, PORTA_PLC
'''
SIMULATORE socket di PLC

socket ad utilizzo di test come sostituto al PLC.
Invia messaggi ogni tot di tempo randomico
    
'''
    
def testing_socket():
    # parametri per generare intervalli di tempo per simulare il socket PLC
    minimo_intervallo_di_secondi = 2
    massimo_intervallo_di_secondi = 8
    intervallo_di_secondi_per_disconnessione = 3

    while True: # all'infinito
        
        # messaggio randomico per simulare il messaggio PLC
        MESSAGE = bytes('f,'+str(rnd.randint(0,5))+','+str(rnd.randint(1,100))+',' +str(rnd.randint(1,100)),'utf-8') 
        # estrai orario di adesso
        current_time = datetime.now().strftime("%H:%M:%S")

        # try:
                
        # inizializza il socket con IPv4 e straming socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.bind((IP_PLC, PORTA_PLC))
        #sock.bind((IP_SERVER, PORTA_SERVER))

        # connetti il socket al server della applicazione
        sock.connect((IP_SERVER, PORTA_SERVER))

        # manda un messaggio test
        sock.send(MESSAGE)

        # chiudi il socket
        sock.close()
        
        # dormi un numero randomico di secondi
        #time.sleep(rnd.randint(minimo_intervallo_di_secondi, massimo_intervallo_di_secondi+1))
        
        time.sleep(1)

        # stampa logs
        print('🆗 '+ Fore.GREEN +' [running socket]'+ Style.RESET_ALL+' al server IP: '+IP_SERVER+':'+str(PORTA_SERVER)+'  messaggio: ' + Fore.BLUE  +str(MESSAGE)  + Style.RESET_ALL + ' alle ore '+  Fore.YELLOW  +str(current_time) + Style.RESET_ALL)

    # except: 
    #     # quando succede un qualsiasi errore eseguisci le linee qui sotto 
    #     print('Errore 🔥',Fore.RED +current_time+Style.RESET_ALL,f'Connessione al server {IP_SERVER}:{PORTA_SERVER} non riuscita ') 
    #     time.sleep(intervallo_di_secondi_per_disconnessione)


if __name__ == "__main__":
    testing_socket()#IP_SERVER,PORTA_SERVER)
 
    
