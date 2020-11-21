from django.shortcuts import render, redirect
from .models import Food
import cv2
import numpy as np
from django.http import JsonResponse
from PIL import Image
import tensorflow.keras
import pandas as pd

# Create your views here.
def test(request):
    print("===========================")
    if request.method == 'POST':

        data = pd.read_csv('labels.txt', sep = " ", header=None)
        labels = list(data[1])
        ingrd_labels = []

        aa = request.FILES['uploadFile']
        img = Image.open(aa)
        img.save('test.jpg')
        # img.save("test.jpg")
        image = cv2.imread('test.jpg')
        image = cv2.resize(image, (1000, 680))
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(image_gray, ksize=(1,1), sigmaX=0)
        ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
        
        edged = cv2.Canny(blur, 10, 250)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total = 0

        contours_xy = np.array(contours)
        contours_xy.shape

        model = tensorflow.keras.models.load_model('keras_model.h5')

        for i in range(len(contours_xy)):
            x_min, x_max = 0,0
            y_min, y_max = 0,0
            value_x = list()
            value_y = list()
            for j in range(len(contours_xy[i])):
                value_x.append(contours_xy[i][j][0][0]) 
                value_y.append(contours_xy[i][j][0][1])
            x_min = min(value_x)
            x_max = max(value_x)

            y_min = min(value_y)
            y_max = max(value_y)

            x = x_min
            y = y_min
            w = x_max-x_min
            h = y_max-y_min
            
            if w * h < 6500:
                continue
            
            img_trim = image[y:y+h, x:x+w]
            cv2.imwrite('org_trim.jpg', img_trim)
            org_image = cv2.imread('org_trim.jpg')
            
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            orf_image = cv2.resize(org_image, dsize=(224, 224), interpolation=cv2.INTER_AREA)
            
        
            
            image_array = np.asarray(orf_image)

            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

            data[0] = normalized_image_array

            prediction = model.predict(data)
            ingrd_labels.append(labels[np.argmax(prediction)])

        ingrd_labels = list(set(ingrd_labels))

        context = {
            'labels' : ingrd_labels
        }
        
        return JsonResponse(context)
    return redirect('food:recoreci')



def randreci(request):

    Foods = Food.objects.all()
    random = set(np.random.randint(0, len(Foods), 20))

    radomFoods = []
    for idx in random:
        reci = ""
        for reciname in Foods[int(idx)].reci.split(','):
            reciname = reciname.strip()
            if reciname == "gaji":
                reci += '가지 '
            elif reciname == "gazzi":
                reci += '갈치 '
            elif reciname == "gamja":
                reci += '감자 '
            elif reciname == "goguma":
                reci += '고구마 '
            elif reciname == "godeunge":
                reci += '고등어 '
            elif reciname == "gochu":
                reci += '고추 '
            elif reciname == "nazzi":
                reci += '낙지 '
            elif reciname == "dangeun":
                reci += '당근 '
            elif reciname == "daepa":
                reci += '대파 '
            elif reciname == "pig":
                reci += '돼지고기 '
            elif reciname == "dubu":
                reci += '두부 '
            elif reciname == "mu":
                reci += '무 '
            elif reciname == "tomato":
                reci += '토마토 ' 
            elif reciname == "baechu":
                reci += '배추 '
            elif reciname == "buchu":
                reci += '부추 '
            elif reciname == "soseji":
                reci += '소세지 '
            elif reciname == "applge":
                reci += '사과 '
            elif reciname == "busut":
                reci += '버섯 '
            elif reciname == "dak":
                reci += '닭 '
            elif reciname == "beef":
                reci += '소고기 '
            elif reciname == "spam":
                reci += '스팸 '
            elif reciname == "eohobak":
                reci += '애호박 '
            elif reciname == "yangbaechu":
                reci += '양배추 '
            elif reciname == "yangpa":
                reci += '양파 '
            elif reciname == "hobak":
                reci += '호박 '
            elif reciname == "oe":
                reci += '오이 '
            elif reciname == "ojinge":
                reci += '오징어 '
            elif reciname == "oksusu":
                reci += '옥수수 '
            elif reciname == "chamchi":
                reci += '참치 '
            elif reciname == "kongnamul":
                reci += '콩나물 '
            elif reciname == "egg":
                reci += '달걀 '

        radomFoods.append({
            'name': Foods[int(idx)].name, 
            'image': Foods[int(idx)].image,
            'cookingOrder': Foods[int(idx)].cookingOrder,
            'reci': reci
        }) 

    context = {
        'Foods': radomFoods,
    }
    return render(request, 'food/randreci.html', context)


def recoreci(request):
    food = Food.objects.all()
    foods = []
    for f in food:
        foods.append({'name':f.name,'reci':f.reci,'a':f.cookingOrder,'img':f.image})
    return render(request, 'food/recoreci.html', {'food':foods})
