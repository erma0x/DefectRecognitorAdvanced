from msilib.schema import Error
import socket
import sys
import cv2

def manda_dati_al_PLC(dati: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_PLC, PORTA_PLC))
    msg = s.send(dati)
    print(msg.decode("utf-8") ) 


def fai_una_foto():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    # reading the input using the camera
    result, image = cam.read()
    return image

if __name__ == '__main__':

    PORTA_SERVER = 1234
    IP_SERVER = socket.gethostname()

    IP_PLC = '122.34.21.1'
    PORTA_PLC = 50

    # TCP server basato su IPv4 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Associa l'indirizzo IP e il numero di porta
    s.bind((IP_SERVER, PORTA_SERVER))          
    # il numero di porta può essere compreso tra 0-65535 (di solito le porte non privilegiate sono > 1023)
    s.listen(PORTA_SERVER)

    while True:
        clt, adr = s.accept() # accetta connessioni
        print(f"Connection to {adr} established \n client object {clt}")
        
        messaggio_plc = s.recv(2048).decode('utf-8')

        if messaggio_plc:
            print(messaggio_plc)
            output_foto_path = sys.path[0] + 'take'+ messaggio_plc +'.png'
            #cv2.imwrite(output_foto_path, sk.elabora_foto( sk.fai_una_foto() ))