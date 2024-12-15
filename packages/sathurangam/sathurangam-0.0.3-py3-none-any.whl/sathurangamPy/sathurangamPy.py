import cv2
import numpy as np
import os

def display_image(filename):
    cap = cv2.imread(str(filename))
    cv2.imshow('image', cap)

    cv2.waitKey()
    cv2.destroyAllWindows()

def grayscale_converter(filename):

    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def resize_image(filename, width, height):
    image = cv2.imread(filename)

    resized = cv2.resize(image, (width,height), interpolation=cv2.INTER_CUBIC)
    return resized

def rotate_image(filename, angle):
    
    def rotate(image, angle, rotPoint=None):
        (height,width) = image.shape[:2]
        if rotPoint is None:
            rotPoint = (width//2,height//2)
    
        rotMat = cv2.getRotationMatrix2D(rotPoint, angle, 1.0)
        dimensions = (width,height)

        return cv2.warpAffine(image, rotMat, dimensions)
    
    image = cv2.imread(filename)
    rotated = rotate(image, angle)
    return rotated

def blur_image(filename, kernel):
    image = cv2.imread(filename)
    if kernel % 2 == 0:
        return print("Error: Kernel size must be an odd number.")
    blur = cv2.GaussianBlur(image, (kernel,kernel), cv2.BORDER_DEFAULT)
    return blur

def crop_image(filename, x, y, width, height):
    image = cv2.imread(filename)
    crop = image[y:y+height, x:x+width]
    cv2.imshow('Croped', crop)
    return crop

def canny_edge(filename, kernel, low_threshold, high_threshold):
    image = cv2.imread(filename)
    blur = cv2.GaussianBlur(image, (kernel,kernel), cv2.BORDER_DEFAULT)
    canny = cv2.Canny(blur, low_threshold, high_threshold)
    return canny

def dilate_image(filename, kernel, low_threshold, high_threshold, iterations):
    image = cv2.imread(filename)
    blur = cv2.GaussianBlur(image, (kernel,kernel), cv2.BORDER_DEFAULT)
    canny = cv2.Canny(blur, low_threshold, high_threshold)
    dilated = cv2.dilate(canny, (kernel,kernel), iterations)
    return dilated

def erode_image(filename, kernel, low_threshold, high_threshold, dilate_iterations,erode_iterations ):
    image = cv2.imread(filename)
    blur = cv2.GaussianBlur(image, (kernel,kernel), cv2.BORDER_DEFAULT)
    canny = cv2.Canny(blur, low_threshold, high_threshold)
    dilated = cv2.dilate(canny, (kernel,kernel), dilate_iterations)
    eroded = cv2.erode(dilated, (kernel,kernel), erode_iterations)
    return eroded

def threshold_image(filename, threshold):
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return img

def contour_count(filename, kernel, low_threshold, high_threshold):
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(image, (kernel,kernel), cv2.BORDER_DEFAULT)
    canny = cv2.Canny(blur, low_threshold, high_threshold)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return print(f'{len(contours)} contour(s) found!')

def draw_contour(filename, kernel, low_threshold, high_threshold, thickness, color=()*3):
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(image, (kernel,kernel), cv2.BORDER_DEFAULT)
    canny = cv2.Canny(blur, low_threshold, high_threshold)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    blank = np.zeros(image.shape, dtype='uint8')
    cv2.drawContours(blank, contours, -1, color, thickness)
    return blank

def draw_specific_contour(filename, kernel, low_threshold, high_threshold,contourIdx, thickness, color=()*3):
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(image, (kernel,kernel), cv2.BORDER_DEFAULT)
    canny = cv2.Canny(blur, low_threshold, high_threshold)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    blank = np.zeros(image.shape, dtype='uint8')
    cv2.drawContours(blank, contours, contourIdx, color, thickness)
    return blank

def draw_blank_image(height,width):
    blank = np.zeros((height,width), dtype='uint8')
    return blank

def draw_color_image(height,width,color=()*3):
    blank = np.zeros((height,width,3), dtype='uint8')
    blank[:] = color
    return blank

def draw_rectangle(filename,thickness, start_point=()*2, end_point=()*2, color=()*3):
    image = cv2.imread(filename)
    cv2.rectangle(image, start_point, end_point, color, thickness)
    return image

def draw_circle(filename, thickness,radius, center_point=()*2, color=()*3):
    image = cv2.imread(filename)
    cv2.circle(image, center_point, radius, color, thickness)
    return image

def draw_line(filename, thickness, start_point=()*2, end_point=()*2, color=()*3):
    image = cv2.imread(filename)
    cv2.line(image, start_point, end_point, color, thickness)
    return image

def draw_text(filename, text,fontScale, position=()*2, color=()*3):
    image = cv2.imread(filename)
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_COMPLEX, fontScale, color)
    return image

def draw_custom_text(filename, text,fontstyle, fontScale, position=()*2, color=()*3):
    image = cv2.imread(filename)
    cv2.putText(image, text, position, fontstyle, fontScale, color)
    return image

def read_video(filename):
    cap = cv2.VideoCapture(filename)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Video', frame)
        if cv2.waitKey(2000) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def detect_face(filename,haarfile, scaleFactor, minNeighbors):
    image = cv2.imread(filename)
    if image is None:
        print(f"Error loading image from {filename}")
        return None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(haarfile)
    if face_cascade.empty():
        print("Error loading Haar cascade classifier!")
        return None
    faces = face_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)
    print(f'Number of faces found = {len(faces)}')
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imshow('Faces found', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_face(videocap, datasets,sub_data, haar_file, total):

    path = os.path.join(datasets, sub_data)
    if not os.path.isdir(path):
        os.mkdir(path)
    (width, height) = (130,100)

    face_cascade = cv2.CascadeClassifier(haar_file)

    webcam = cv2.VideoCapture(videocap)

    count = 1
    while count < total:
        print(count)
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3,4)
        for (x,y,w,h) in faces:
            cv2.rectangle(im, (x,y), (x+w,y+h), (255,0,0),2)
            face = gray[y:y +h, x:x +w]
            face_resize = cv2.resize(face, (width, height))
            cv2.imwrite('%s/%s.png' % (path,count), face_resize)
        count += 1
        cv2.imshow('opencv', im)
        key = cv2.waitKey(10)
        if key == 27:
            break
    webcam.release()
    cv2.destroyAllWindows()