from msilib.schema import Error
import socket


if __name__ == '__main__':

    # TCP server basato su IPv4 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa l'indirizzo IP e il numero di porta
    s.bind((socket.gethostname(),1234))          

    # il numero di porta può essere compreso tra 0-65535 (di solito le porte non privilegiate sono > 1023)
    port_number = 5
    s.listen(port_number)

    while True:
        clt, adr = s.accept() # accetta connessioni
        print(f"Connection to {adr} established \n client object {clt}")
        clt.send(bytes("Connesso al server","utf-8 "))