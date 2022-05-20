import socket
import sys
import cv2

def manda_dati_al_PLC(dati: str,IP_PLC: str,PORTA_PLC : int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_PLC, PORTA_PLC))
    msg = s.send(dati)
    print(msg.decode("utf-8") ) 


def fai_una_foto(porta_usb = 0):
    cam = cv2.VideoCapture(porta_usb)
    # reading the input using the camera
    result, image = cam.read()
    if result:
        return image
    else:
        print('Errore nel fare una foto')
        return None

def main():
    '''
    filtra i messaggi che arrivano dal socket
    e se il primo carattere del messaggio contine una f
    allora fai partire una fotografia.
    '''
    PORTA_SERVER = 1234
    IP_SERVER = socket.gethostname()

    contatore = 1

    # TCP server basato su IPv4 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa l'indirizzo IP e il numero di porta
    s.bind((IP_SERVER, PORTA_SERVER))

    # il numero di porta può essere compreso tra 0-65535 (di solito le porte non privilegiate sono > 1023)
    s.listen(PORTA_SERVER)

    while True:
        
        clt, address = s.accept() # accetta connessioni

        print(f"Connesso al seguente indirizzo {address}")
        
        messaggio_plc = s.recv(1024).decode('utf-8')

        if messaggio_plc: 
            # se hai ricevuto dati

            if str(messaggio_plc)[2]== b'f': 
                # se il messaggio ha come primo carattere una 'f'
                
                print(messaggio_plc)   # stampa messaggio

                contatore += 1
                output_foto_path = sys.path[0] + '/img/foto_'+ contatore +'.png'
                fotografia =  fai_una_foto() 
                if fotografia:
                    cv2.imwrite(output_foto_path, fotografia)

if __name__ == '__main__':
    main()
