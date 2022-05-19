import socket

def main():
    '''
    simula un server che invia riceve i dati dal client e li stampa a terminale
    '''
    HOST = "127.0.0.1"  # Indirizzo dell'interfaccia di loopback standard (localhost)
    PORT = 65432  # Porta su cui ascoltare (le porte non privilegiate sono > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)

        connection, client_addresss = s.accept()

        with connection:
            print(f"Connesso con il client : {client_addresss}")

            while True:
                data = connection.recv(1024)

                if data:
                    # stampa i dati ricevuti dal client
                    print('\n',data)

if __name__ == "__main__":
    main()
