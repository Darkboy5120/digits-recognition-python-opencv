#Ordinario de procesamiento de imagenes
#Profesor: Navarro Alvarez Enernesto
#Alumnos: Maldonado Gonzalez Hilarion Guadalupe
#Semestre y grupo: 7D
#Testeado con exito en windows 10, 12/13/2021 9:35

import cv2
import numpy as np
import digits_ann as ANN

#el sample generado solo se hizo con 200 iteraciones por epoca, solo para depurar
ITERATIONS_BY_EPOCH = 20000
IMAGES = [
    "./images/numbers0.jpg",
    "./images/numbers1.png",
    "./images/numbers2.png"
]

def inside(r1, r2):
    x1, y1, w1, h1 = r1
    x2, y2, w2, h2 = r2
    if (x1 > x2) and (y1 > y2) and (x1+w1 < x2+w2) and (y1+h1 < y2 + h2):
        return True
    else:
        return False
    
def wrap_digit(rect):
    x, y, w, h = rect
    padding = 5
    hcenter = x + w/2
    vcenter = y + h/2

    if (h > w):
        w = h
        x = hcenter - (w/2)
    else:
        h = w
        y = vcenter - (h/2)
    return (int(x-padding), int(y-padding), int(w+padding), int(h+padding))

ann, test_data = ANN.train(ANN.create_ANN(56), ITERATIONS_BY_EPOCH)
font = cv2.FONT_HERSHEY_SIMPLEX

def find_numbers(image_path):
    path = image_path
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bw = cv2.GaussianBlur(bw, (7, 7), 0)
    ret, thbw = cv2.threshold(bw, 127, 255, cv2.THRESH_BINARY_INV)
    thbw = cv2.erode(thbw, np.ones((2, 2), np.uint8), iterations = 2)
    cntrs, hier = cv2.findContours(thbw.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rectangles = []

    for c in cntrs:
        r = x, y, w, h = cv2.boundingRect(c)
        a = cv2.contourArea(c)
        b = (img.shape[0]-3) * (img.shape[1] - 3)

        is_inside = False
        for q in rectangles:
            if inside(r, q):
                is_inside = True
                break
        if not is_inside:
            if not a == b:
                rectangles.append(r)

    for r in rectangles:
        x, y, w, h = wrap_digit(r)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi = thbw[y:y+h,x:x+w]

        try:
            digit_class = int(ANN.predict(ann, roi.copy())[0])
        except:
            continue
        
        cv2.putText(img, "%d" % digit_class, (x, y-1), font, 1, (0, 255, 0))

    cv2.imshow("thbw", thbw)
    cv2.imshow("contorous", img)
    cv2.imwrite("sample.jpg", img)
    cv2.waitKey()

for path in IMAGES:
    find_numbers(path)