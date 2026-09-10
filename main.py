import cv2
import numpy as np
import imutils

#from colors.constants import * 
from colors.specific_colors import * 

def color_analyzer(camera, kernel):
    while True: 
        ret, frame = camera.read() #Verifica se a câmera realmente leu o frame com sucesso
        if not ret:
            break

        frame = imutils.resize(frame, width=1000) # redimensionamento
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # conversão para HSV

        for key, value in UPPER_COLORS.items():
            #Converter as tuplas para numpy arrays garante compatibilidade total com o OpenCV
            lower_np = np.array(LOWER_COLORS[key], dtype=np.uint8)
            upper_np = np.array(UPPER_COLORS[key], dtype=np.uint8)

            #Aplica as máscaras
            mask = cv2.inRange(hsv, lower_np, upper_np)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) 
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] 

            if len(cnts) > 0: 
                threshold = 10
                c = max(cnts, key=cv2.contourArea)
                m = cv2.moments(c)
                ((x, y), radius) = cv2.minEnclosingCircle(c) 
                
                if radius > threshold: 
                    cv2.circle(img=frame, center=(int(x), int(y)), radius=int(radius), color=TRIGGER_COLOR[key], thickness=2) 
                    cv2.putText(img=frame, text=key + " object", org=(int(x-radius), int(y-radius)), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.6, color=TRIGGER_COLOR[key], thickness=2)

        cv2.imshow("Frame RGB", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

if __name__ == '__main__':
    try:
        camera = cv2.VideoCapture(0) 
        kernel = np.ones((9, 9), np.uint8) 

        color_analyzer(camera, kernel)
        camera.release()
        cv2.destroyAllWindows()

    except Exception as error:
        camera.release()
        cv2.destroyAllWindows()
        print(error)