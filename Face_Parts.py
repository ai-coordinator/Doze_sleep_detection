import cv2
import numpy as np
import dlib

def eye_point(img, parts, left=True):
    if left:
        eyes = [
                parts[36],
                min(parts[37], parts[38], key=lambda x: x.y),
                max(parts[40], parts[41], key=lambda x: x.y),
                parts[39],
                ]
    else:
        eyes = [
                parts[42],
                min(parts[43], parts[44], key=lambda x: x.y),
                max(parts[46], parts[47], key=lambda x: x.y),
                parts[45],
                ]
    org_x = eyes[0].x
    org_y = eyes[1].y
    if is_close(org_y, eyes[2].y):
        return True

def is_close(y0, y1):
    if abs(y0 - y1) < 23:
        print(abs(y0 - y1))
        return True
    print("open ",abs(y0 - y1))
    return False

def main():
    sleep_flg = 0
    while True:
        #webcam
        success,img = cap.read()

        imgOriginal = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(imgGray)

        for face in faces:
            landmarks = predictor(imgGray,face).parts()
            # myPoints =[]
            # for n in range(68):
            #     x = landmarks.part(n).x
            #     y = landmarks.part(n).y
            #     myPoints.append([x,y])
            #     cv2.circle(imgOriginal,(x,y),5,(50,50,255),cv2.FILLED)
            #     cv2.putText(imgOriginal,str(n),(x,y-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.9,(0,0,255),1)
            #
            # print(np.array(myPoints))

            left_eye = eye_point(imgGray, landmarks)
            right_eye = eye_point(imgGray, landmarks, False)

            print(left_eye,right_eye)

            if left_eye == True or right_eye == True:
                # cv2.putText(img, "sleeping", (rect.left(), rect.top()-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                sleep_flg += 1
            else:
                cv2.putText(imgOriginal, "", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                sleep_flg = 0

            imgOriginal = cv2.rectangle(imgOriginal, pt1=(face.left(), face.top()), pt2=(face.right(), face.bottom()),
                            color=(150, 0, 150), lineType=cv2.LINE_AA, thickness=5)

            print("sleep_flg ",sleep_flg)
            if sleep_flg >= 100:
                cv2.putText(imgOriginal, "sleeping", (face.left(), face.top()), cv2.FONT_HERSHEY_SIMPLEX, 7, (0, 0, 255), 10)
            elif sleep_flg >= 35:
                cv2.putText(imgOriginal, "sleepy", (face.left(), face.top()), cv2.FONT_HERSHEY_SIMPLEX, 7, (0, 100, 255), 9)
            else:
                cv2.putText(imgOriginal, "Wake Up", (face.left(), face.top()), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 7)

        cv2.imshow("Original",imgOriginal)
        c = cv2.waitKey(1)
        if c == 27:#ESCを押してウィンドウを閉じる
            break

if __name__ == '__main__':

    cap = cv2.VideoCapture("13.mp4")

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    main()
