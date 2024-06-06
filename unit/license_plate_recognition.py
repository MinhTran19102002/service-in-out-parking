from paddleocr import PaddleOCR,draw_ocr
from PIL import Image
import cv2
import numpy as np

from PIL import ImageTk, Image, ImageDraw


def select_image(file_storage):

    file_data = file_storage.read()
    np_data = np.frombuffer(file_data, np.uint8)

    image = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    if image is None:
        return "Error: Unable to read image.", ''
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray =  cv2.bilateralFilter(img_gray, 11,17,17)

    edged = cv2.Canny(img_gray, 190, 200)
    contours , new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    contour_license_plate = None
    license_plate = None
    w= None
    h = None
    x= None
    y = None
    res = ''
    for contour in contours:
        perimeter =  cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018* perimeter, True)
        if len(approx) == 4:
            contour_license_plate = approx
            x,y,w,h = cv2.boundingRect(contour_license_plate)
            print(x, y, w, h)
            license_plate = img_gray[y: y+h, x:x+w]
            # cv2.imshow("Result2",license_plate)
            ocr = PaddleOCR(use_angle_cls=True, lang='en')
            result = ocr.ocr(license_plate, cls=True)
            res = result[0]
            # txts = [line[1][0] for line in res]
            if(res):
                break

    file_path = ''
    if res:
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        
        result = ocr.ocr(license_plate, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                print(line)


        result = result[0]

        img = image

        
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        # scores = [line[1][1] for line in result]

        for line in result:
            if len(line[1][0]) == 10:
                print(line[1][0])
        im_show = draw_ocr(img, boxes)
        im_show = Image.fromarray(im_show)

        im_show = im_show.resize((300, 300))  # Thay đổi kích thước hình ảnh
        # im_show = ImageTk.PhotoImage(im_show)

        # image_label.config(image=im_show)
        # image_label.image = im_show 
        license_text = ''
        if(len(txts)==2):
            license_text= txts[0]+ '-' + txts[1]
        if(len(txts)==1):
            license_text= txts[0]
        license_text = license_text.replace(".", "")
        return license_text, image
    elif file_storage:
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        
        result = ocr.ocr(img_gray, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            print(res)
            for line in res:
                print(line)
        result = result[0]

        img = image

        
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        # scores = [line[1][1] for line in result]

        for line in result:
            if len(line[1][0]) == 10:
                print(line[1][0])
        im_show = draw_ocr(img, boxes)
        im_show = Image.fromarray(im_show)

        im_show = im_show.resize((300, 300))  # Thay đổi kích thước hình ảnh
        # im_show = ImageTk.PhotoImage(im_show)
        license_text = ''
        if(len(txts)==2):
            license_text= txts[0]+ '-' + txts[1]
        if(len(txts)==1):
            license_text= txts[0]
        license_text = license_text.replace(".", "")
        return license_text,image
    


def select_image1(img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
    edged = cv2.Canny(blurred, 10, 200)

    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
    contour_license_plate = None
    w= None
    h = None
    x= None
    y = None
    for contour in contours:
        perimeter =  cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01* perimeter, True)
        if len(approx) == 4:
            contour_license_plate = approx
            x,y,w,h = cv2.boundingRect(contour_license_plate)
            break
    if x:
        (x, y, w, h) = cv2.boundingRect(contour_license_plate)
        cv2.putText(img, "bien so xe", (x-10, y -10), cv2.FONT_HERSHEY_SIMPLEX, 1.75, (255, 0, 0), 2)


    # ocr = PaddleOCR(use_angle_cls=True, lang='en')
    # result = ocr.ocr(number_plate, cls=True)
    # res = result[0]

    # if res:
    #     for idx in range(len(result)):
    #         res = result[idx]
    #         for line in res:
    #             print(line)


    return cv2.imencode('.jpg', img)[1].tobytes()#frame
