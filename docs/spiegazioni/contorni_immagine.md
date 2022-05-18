## **Contorni dell'immagine**

<br>

## Cosa sono i contorni

I contorni possono essere spiegati semplicemente come una curva che unisce tutti i punti continui (lungo il confine), aventi lo stesso colore o intensità. I contorni sono uno strumento utile per l'analisi della forma e il rilevamento e il riconoscimento di oggetti.

Per una migliore precisione, utilizzare immagini binarie. Quindi, prima di trovare i contorni, applica il rilevamento della soglia o del bordo intelligente.
Da OpenCV, _findContours()_ non modifica più l'immagine di origine.
In OpenCV, trovare i contorni è come trovare un oggetto bianco da uno sfondo nero. Quindi ricorda, l'oggetto da trovare dovrebbe essere bianco e lo sfondo dovrebbe essere nero.


Vedi, ci sono tre argomenti nella funzione cv.findContours(), il primo è l'immagine sorgente,
il secondo è la modalità di recupero del contorno, il terzo è il metodo di approssimazione del contorno.
E restituisce i contorni e la gerarchia. Contours è un elenco Python di tutti i contorni nell'immagine.
Ogni singolo contorno è un array Numpy di coordinate (x,y) di punti limite dell'oggetto.

<br>

### Come disegnare i contorni?

Per disegnare i contorni, viene utilizzata la funzione cv.drawContours.
Può anche essere usato per disegnare qualsiasi forma a condizione che tu abbia i suoi punti limite.
Il suo primo argomento è l'immagine sorgente, il secondo argomento sono i contorni che dovrebbero essere passati come un elenco Python,
il terzo argomento è l'indice dei contorni (utile quando si disegna un contorno individuale.
Per disegnare tutti i contorni, passa -1) e gli argomenti rimanenti sono colore, spessore ecc.

<br>

### Metodo di approssimazione del contorno

Questo è il terzo argomento nella funzione cv.findContours.

Sopra, abbiamo detto che i contorni sono i confini di una forma con la stessa intensità. Memorizza le coordinate (x,y) del confine di una forma.
Se si inserisce cv.CHAIN_APPROX_NONE, tutti i punti limite vengono memorizzati. 
Ma in realtà abbiamo bisogno di tutti i punti? Ad esempio, hai trovato il contorno di una linea retta. Hai bisogno di tutti i punti sulla linea per rappresentare quella linea? No, abbiamo bisogno solo di due estremi di quella linea. Questo è ciò che fa cv.CHAIN_APPROX_SIMPLE. Rimuove tutti i punti ridondanti e comprime il contorno, risparmiando così memoria.

Disegna semplicemente un cerchio su tutte le coordinate nell'array del contorno (disegnato in colore blu). La prima immagine mostra i punti che ho ottenuto con cv.CHAIN_APPROX_NONE (734 punti) e la seconda immagine mostra quella con cv.CHAIN_APPROX_SIMPLE (solo 4 punti). Vedi, quanta memoria risparmia!!!


<br>

## findContours()
### Trova i contorni in un'immagine binaria


cv.findContours( immagine, modalità, metodo[, contorni[, gerarchia[, offset]]] ) -> immagine, contorni, gerarchia


**Parametri**

-    Immagine

Sorgente, un'immagine a canale singolo a 8 bit. I pixel diversi da zero vengono trattati come 1. Zero pixel rimangono 0, quindi l'immagine viene trattata come
binario. È possibile utilizzare compare, inRange, threshold , adaptiveThreshold, Canny e altri per creare un'immagine binaria da un'immagine in scala di grigi o a colori. Se mode è uguale a RETR_CCOMP o RETR_FLOODFILL, l'input può anche essere un'immagine intera a 32 bit di etichette (CV_32SC1).

- contorni

Contorni rilevati. Ogni contorno è memorizzato come vettore di punti.


- gerarchia

Vettore di output opzionale, contenente informazioni sulla topologia dell'immagine. Ha tanti elementi quanti sono i contorni. Per ogni i-esimo profilo di contorno[i], gli elementi gerarchia[i][0] , gerarchia[i][1] , gerarchia[i][2] e gerarchia[i][3] sono impostati su 0- indici basati nei contorni dei contorni successivi e precedenti allo stesso livello gerarchico, rispettivamente del primo contorno figlio e del contorno padre. Se per il contorno i non ci sono contorni successivi, precedenti, principali o annidati, gli elementi corrispondenti della gerarchia[i] saranno negativi.

In python, la gerarchia è nidificata all'interno di un array di livello superiore. Usa la gerarchia[0][i] per accedere agli elementi gerarchici dell'i-esimo contorno.