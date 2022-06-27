import numpy as np
import cv2

def save_img(path_img, img):
    """ 
    Salvare le immagini indicandone il path e l'estensione della foto
    prendendo in input gli oggetti immagine di opencv
    path_img = sys.path[0]+"\\photo\\take_{}.png".format(processed_images)
    print(path_img)
    """
    cv2.imwrite(path_img, img)


def cartoonize(img,a=20,b=200,c=250):
    '''
    Modifica l'immagine rendendola come un cartone.
    permette di eliminare il rumore di fondo e fare smoothing, 
    così da visualizzare meglio l'oggetto e separarlo dallo sfondo. 
    '''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),-1)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,9,10)
    color = cv2.bilateralFilter(img, a, b, c)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon


def trova_imperfezioni(img, min_canny=40, max_canny=200, min_canny2=150, max_canny2=220):
    '''
    processa immagine al fine di visualizzare piu imperfezioni possibili
    all'interno della pelle.
    parametri default:  min_canny=40, max_canny=200, min_canny2=150, max_canny2=220
    '''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, min_canny, max_canny)
    edges_high_thresh = cv2.Canny(edges, min_canny2, max_canny2)
    return edges_high_thresh


def disegna_contorni(image):
    '''
    trova imperfezioni in un immagine evidenziandole con un colore.
    '''
    immagine_con_imperfezioni = trova_imperfezioni(image, min_canny = 40, max_canny = 150, min_canny2 = 150, max_canny2 = 250 )
    image = cv2.cvtColor(immagine_con_imperfezioni, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    contour, hier = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #print("Count of Contours  = " + str(len(contour)))
    return cv2.drawContours(image, contour, -1, (50,255,0),2)


def inverti_maschera(img,mask):
    mask2 = cv2.bitwise_not(mask)
    return cv2.bitwise_or(img, img, mask = mask2).copy()


def median_blurr(img, kernel_size=9):
    '''
    permette di fare Blur (sfocatura) dell'immagine con l'algoritmo medianBlur di opencv
    il kernel_size può essere = 3, 9, 15
    '''
    blurred = cv2.medianBlur(img, kernel_size)
    return blurred


def RGB_to_HSV(nome_immagine):
    '''
    converti l'immagine da formato opencv BGR (opposto di RGB) a grayscale (scala di grigi)
    '''
    return cv2.cvtColor(nome_immagine ,cv2.COLOR_RGB2HSV)


def disegna_difetti(img):
    '''
    disegna linee in maniera automatica sull'immagine
    '''
    out = img.copy()
    gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 90, 120)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, minLineLength=5, maxLineGap=20)
    if np.array(lines).any():  
        for line in lines: # Draw lines on the image
            x1, y1, x2, y2 = line[0]
            cv2.line(out, (x1, y1), (x2, y2), (0,0,255), 3)
    return out


def BGR_to_HSV(nome_immagine):
    '''
    converti l'immagine da formato opencv BGR (opposto di RGB) a grayscale (scala di grigi)
    '''
    return cv2.cvtColor(nome_immagine ,cv2.COLOR_BGR2HSV)


def computer_vision_system(immagine, params):
    
    # rendi l'immagine blurred attraverso GaussianBlur
    immagine_cartone = cartoonize(img = immagine, a=params['cartoon_x'],b=params['cartoon_y'],c=params['cartoon_z'])
    
    # trasforma immagine da BGR a HSV
    immagine_hsv = BGR_to_HSV(nome_immagine = immagine)
    
    # crea una maschera
    hsv_color1 = np.asarray([0, 0, 0])
    hsv_color2 = np.asarray([60, 255, 255])
    
    mask = cv2.inRange( immagine_hsv, hsv_color1, hsv_color2)

    # inverti i pixel della maschera
    img_senza_background = inverti_maschera( immagine_cartone, mask)

    # disegna i difetti con un determinato colore nell'immagine senza background
    immagine_forte_contrasto = disegna_difetti( img = img_senza_background)
    
    # restituisci il risultato
    return immagine_forte_contrasto