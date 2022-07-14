nome_pannello_di_controllo = "Pannello di controllo"

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

Flusso di lavoro dell'applicazione
1 - accetta messaggi da PLC
2 - se il messaggio ricevuto contiene come primo carattere una 'f' allora scatta foto
3 - elabora foto attraverso il sistema di computer vision per evidenziare difetti
4 - restituisci la presenza o meno del difetto al PLC indicando l'id del pezzo di produzione


'''
