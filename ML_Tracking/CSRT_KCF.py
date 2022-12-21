'''Neste momento o código apenas considera a deteção dos marcadores no primeiro frame
isto faz comm que não "valha a pena" treinar a deteção em várias condições
em velocidades mais altas vai-se perder o tracking porque não está a ir buscar a informação
que foi treinada para detetar o "desfoque" dos marcadores emm velocidades maiores

Além disto, se o marcador for perdido ao longo da marcha é difícil que o tracker
consiga voltar a encontra-lo porque só deteta o objeto no primeiro frame e, neste caso, 
ja nao estamos no primeiro frame

Para resolver isso talvez seja bom tentar fazer com que o código vá buscar a deteção 
automática apenas quando perder o tracking do objeto

Assim, o objetivo é fazer com que a deteção entre em ação quando as bounding boxes desaparecerem por x tempo
Para assegurar que estão a ser acompanhados todos os marcadores talvez seja bom dizer qual terá de ser o número de 
marcadores que se pretende analisar. assim se algum falhar aparece algum aviso ou o tracking
para. 

Testar o seguinte:
- Especificar quantos marcadores se pretende analisar
- Com essa informação temos o numero de boxes que tem de ser analisada no primeiro frame
        - usar o "len(boxes)" para recolher essa informação
- Se não forem encontradas todas as boxes necessárias o código deve correr outra vez até que sejam encontradas
todas as boxes
        - Usar um ciclo "for" para isto. Talvez um ciclo no inicio de todo o código!?
- Se no inicio estiver tudo certo, então o tracking começa a correr
- Durante o tracking o numero de boxes nunca pode ser inferior ao numero de marcadores
que foi estipulado no inicio
        - De notar que o numero de marcadores na versão final vai ser um 
        valor fixo, mas para já vai ser usada uma variável uma vez que 
        pode ser mais fácil testar com menos marcadores
- Tentar diminuir os casos onde, no mesmo marcador, aparecem duas boxes
- Caso o numero de boxes ao longo do tracking seja menor que o numero de marcadores
o detetor terá de entrar e o "ciclo de tracking" deve "reiniciar" uma vez que terá
de se encontrar novas bounding boxes iniciais
        - Pensar numa forma mais eficiente
            - Isto pode fazer com que no "reinicio" se perca o tracking de outros marcadores

-> Identificação dos marcadores
- Pode-se usar o ID de cada marcador, mas tem de se garantir que:
        - O ID se mantém constante ao longo dda análise. 
            - Para isto vamos tentar testar em condições mais semelhantes à marcha
            ao invés de andar a testar com marcadores em locais aleatórios
            - Maior previsibilidade de posição do marcador vai facilitar o tracking
- Se se conseguir manter sempre o mesmo ID vai ser mais fácil fazer o processamento dos dados
        - Mas como é que se garante que cada marcador tem sempre o mesmo ID em qualquer
        vez que se use o program?
        - Talvez seja segmentar a imagem e atribuir um marcador a áreas especificas da imagem
        - Ou ir pelas suas coordenadas
            - Por exemplo o marcador do ombro é o que tem o y mais baixo, o joelho tem o y mais alto
                - Mas há o problema ddos marcadores colocados no tornozelo e metatarsus
                    - Ainda assim parece ser a melhor solução para garantir que estamos 
                    sempre a usar o mesmo marcador em qualquer análise
- Não esquecer que vai ser usado o centro da bounding box para fazer o tracking dos marcadores'''

#? Para usar este código os marcadores têm de estar visíveis no primeiro frame. 
#? Após isso é feito o tracking com os marcadores que foram considerados 
#? nesse primeiro frame. Caso o tracking seja feito não é possível voltar a
#?  detetar os marcadores porque só foram detetados no primeiro frame. 

import cv2
import numpy as np
from time import time
from detector_function import markerDetection, firstBBox

camera = cv2.VideoCapture("/Users/tiagocoutinho/Desktop/3markers.mov")
camera = cv2.VideoCapture(0)

loop_time = time()
ret, frame = camera.read()

# Method to detect the markers on the first frame
frame, boxes, indexes = markerDetection(frame)

# Method to draw the bounding boxes in each detected marker
firstBBox(frame, boxes, indexes)

# Create the multiTracker to track multiple markers
multiTracker = cv2.legacy.MultiTracker_create()

# Add a tracker to each bounding box
for box in boxes:
    multiTracker.add(cv2.legacy.TrackerCSRT_create(), frame, box)

# If there are any boxes on the first frame it raises an error
if boxes == []:
    print("\nERROR: There are no initial bounding boxes\nMake sure that all markers are visible in the first frame\n")

while camera.isOpened():

    if boxes == []:
        break

    success, frame = camera.read()

    if success == False:
        break
    
    # Analyze the FPS rate
    fps = 1/(time() - loop_time)
    loop_time = time()
    
    # Update the tracker on the next frame
    tracking, boxes = multiTracker.update(frame)

    # Get the x, y coordinates, width and heigh of each bounding box
    for i, newbox in enumerate(boxes):
        x = int(newbox[0])
        y = int(newbox[1])
        w = int(newbox[2])
        h = int(newbox[3])
        # Get the center point of each bounding box 
        center = (x + w//2, y + h//2)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
        cv2.circle(frame, center, 6, (255, 0, 0), -1)
        cv2.putText(frame, f"Marker: {str(i)}", (x, y - 20), 1, cv2.FONT_HERSHEY_COMPLEX, (255, 100, 0), 2)

    cv2.putText(frame, f"FPS: {str(round(fps, 2))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 3)
    cv2.imshow('MultiTracker', frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break 

camera.release()
cv2.destroyAllWindows()