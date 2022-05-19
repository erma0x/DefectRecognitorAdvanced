import socket

def main():
    '''
    simula un client socket che invia un singolo messaggio e chiude la connessione
    '''

    MESSAGE = b'hello world'

    IP_SERVER = '127.0.0.1'
    PORT_SERVER = 65432

    # inizializza il socket con IPv4 e socket stream
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.connect((IP_SERVER, PORT_SERVER))

    s.send(MESSAGE)
    
    s.close()


if __name__ == "__main__":
    main()
