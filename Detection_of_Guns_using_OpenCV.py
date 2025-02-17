import numpy as np
import cv2
import imutils
import datetime

# تحميل نموذج الكشف عن السلاح
gun_cascade = cv2.CascadeClassifier('geeksforgeeks/cascade.xml')

def runc():
    # فتح الكاميرا
    camera = cv2.VideoCapture(1)
    firstFrame = None

    while True:
        ret, frame = camera.read()
        if frame is None:
            break
        
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # الكشف عن الأسلحة في الصورة الرمادية
        gun = gun_cascade.detectMultiScale(gray, 1.3, 20, minSize=(100, 100))
        
        gun_exist = len(gun) > 0  # التحقق مما إذا كان هناك سلاح مكتشف
        
        for (x, y, w, h) in gun:
            # رسم مستطيل حول السلاح المكتشف
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        if firstFrame is None:
            firstFrame = gray
            continue

        # إضافة الطابع الزمني على الفيديو
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S %p"),
                    (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)
        
        # طباعة رسالة عند اكتشاف السلاح ولكن بدون إيقاف الحلقة
        if gun_exist:
            print("Guns detected")

        # عرض الفيديو مع التحديثات
        cv2.imshow("Security Feed", frame)

        # كسر الحلقة عند الضغط على "q"
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # تحرير الكاميرا وإغلاق جميع النوافذ
    camera.release()
    cv2.destroyAllWindows()

runc()