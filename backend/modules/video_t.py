import asyncio
import json
import os

import cv2
import base64

import face_recognition
import requests
import websockets

from backend.modules.face import loadFacesModels, loadFaces

face_encodings = []

async def detect_faces_in_video():
    global face_encodings
    # Загрузите изображение и получите его кодировку
    face_encodings = loadFaces()

    # Получите видеопоток с веб-камеры
    video_capture = cv2.VideoCapture('http://192.168.0.12:8080/video')#0


    while True:
        # Захватите один кадр видео
        ret, frame = video_capture.read()
        # Найдите все лица на кадре и их кодировки
        face_locations = face_recognition.face_locations(frame)
        unknown_face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in unknown_face_encodings:
            # Проверяем, есть ли лица на изображении
            if len(face_encoding) > 0:
                name = "Unknown"
                # Сравните известные кодировки лиц с кодировкой неизвестного лица
                for userId, known_face_encodings in face_encodings.items():
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    # Если есть совпадение, используем первое совпадение
                    if True in matches:
                        name = userId

                        if name != "Unknown":
                            requests.post("http://127.0.0.1:5000/user_event", json={'id': name.split(".")[0]})
                        break

                # Рисуем прямоугольник вокруг лица и подписываем его именем
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)


        # Показываем результат
        cv2.imshow('Video', frame)

        # Если пользователь нажал 'q', выйдите из цикла

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        _, buffer = cv2.imencode('.jpg', frame)
        video = base64.b64encode(buffer).decode()
        #await asyncio.sleep(0.5)
        yield video

    # Освободите ресурсы и закройте окна
    video_capture.release()
    cv2.destroyAllWindows()


async def video_sender(uri):
    global websocket_client

    async with websockets.connect(uri + "/video") as websocket:
        await websocket.send(json.dumps({
            'apiId': apiId
        }))

        # Создаем задачи для отправки и получения видео
        send_video_task = asyncio.create_task(send_video(websocket))
        receive_video_task = asyncio.create_task(receive_video(websocket))

        # Запускаем задачи параллельно
        await asyncio.gather(send_video_task, receive_video_task)

async def send_video(websocket):
    async for video in detect_faces_in_video():
        await websocket.send(video)

async def receive_video(websocket):
    print('start recive')
    global face_encodings
    async for message in websocket:
        # Обрабатываем полученное видео
        print('get',message)
        userdata = json.loads(message)
        if userdata.get("name"):
            dir_path = f"./userdata"
            os.makedirs(dir_path, exist_ok=True)

            # Получаем расширение файла из photo_path
            _, file_extension = os.path.splitext(userdata.get('photo_path'))

            # Сохраняем файл в папку
            print(userdata.get('_id'),file_extension)
            file_path = f"{dir_path}/{userdata.get('_id')}{file_extension}"
            print('dir path', file_path)
            with open(file_path, 'wb') as f:
                photo_data = base64.b64decode(userdata.get('photo'))
                f.write(photo_data)

            face_encodings = loadFaces()

apiId = "65d9aa434419fb3469da9ce5"
wsUrl = 'ws://127.0.0.1:5001'

asyncio.run(video_sender(wsUrl))