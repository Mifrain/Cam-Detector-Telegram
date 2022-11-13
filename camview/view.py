import asyncio
from datetime import datetime, timedelta
import cv2 as cv
import numpy as np
from PIL import Image 


from bot.bot import send_info
from config import cam_token


cap = cv.VideoCapture(cam_token)  # Домашняя камера

# faces = cv.CascadeClassifier('camview/ai/face_detector.xml') лица (Временно отключено)
body = cv.CascadeClassifier('camview/ai/body_detector.xml') # подгрузка нейронки тела



async def send_photo(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    path = f'camview/images/image-{datetime.utcnow()}.jpg' # сохраняем картинку в указанную директорию
    # !Обязательно сохраняем полученную матрицу в виде картинки, тк aiogram не поддерживает отправку матрицы
    Image.fromarray(img).save(path) 
    await send_info(path)
    


def check_cam():
    next_message = datetime.utcnow() #Разрешенное время для отправки (понадобится дальше)
    while True:
        img = cap.read()[1]  #берем кадр с камеры
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  #приводим к чб для более точного поиска
        
        result_body = body.detectMultiScale(gray_img, scaleFactor=1.37, minNeighbors=1) #Поиск по подобранным значениям
        # Делаем обводку вокруг объекта
        if len(result_body) != 0 and datetime.utcnow() > next_message:
                for (x, y, w, h) in result_body:
                    cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 130), thickness=3)  #Обводим человека в квадрат
                
                next_message = datetime.utcnow() + timedelta(0, 90) #следующую картинку будем отправлять через n секунд
                asyncio.run(send_photo(img)) # Отправляем фотографию через бота
        
        if cv.waitKey(1):
            continue


    

# Подбор ScaleFactor (работоспособность функции не гарантируется)

# резы от 1.2 до 2 [70, 67, 70, 45, 60, 45, 59, 52, 35, 27, 18, 31, 29, 25, 32, 58, 61, 47, 30, 12, 17, 15, 12, 9, 9, 9, 8, 3, 6, 16, 18, 23, 29, 12, 27, 28, 18, 19, 9, 12]
# def f(i):
#     try:
#         # Домашняя камера
#         # cap = cv.VideoCapture('cam_token')
#         cap = cv.VideoCapture('videos/cams.mp4')

#         # faces = cv.CascadeClassifier('face_detector.xml')
#         body = cv.CascadeClassifier('body_detector.xml')
#         k = 0

#         while True:
#             img = cap.read()[1]
#             gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


#             # result_faces = faces.detectMultiScale(gray_img, scaleFactor=1.4, minNeighbors=3)
#             result_body = body.detectMultiScale(gray_img, scaleFactor=i, minNeighbors=1)

#             # for (x, y, w, h) in result_faces:
#             #     cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 180, 0), thickness=2)
#             #     cv.putText(img, 'Face', (x, y), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=2, color=(0, 210, 0), thickness=2)
                
#             for (x, y, w, h) in result_body:
#                 cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 130), thickness=3)
#                 cv.putText(img, 'Body', (x, y), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=2, color=(0, 0, 160), thickness=2)

#             # cv.imshow('Image', img)
#             if result_body != ():
#                 k += 1
#                 # cv.imshow('Image', img)
#                 # new_img = cv.imwrite(f'images/new_im{num}.jpg', img, [])
        
#             if cv.waitKey(1) & 0xFF == ord('q'):
#                 break
#     except:
#         return k    
# m = []    
# print('start')
# i = 1.2
# while i <= 2:  
#     print(f'i = {i}')
#     m.append(f(i))
#     print(m)
#     i+=0.02
    
# print(m)