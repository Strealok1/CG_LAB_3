import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt

label_image = None

images1 = [cv2.imread("images_for_treshhold/1.jpg"), cv2.imread("images_for_treshhold/2.jpg"), cv2.imread("images_for_treshhold/3.jpg"),
          cv2.imread("images_for_treshhold/4.jpg"), cv2.imread("images_for_treshhold/5.jpg")]
images2 = [cv2.imread("images_for_threshold2/1.jpeg"), cv2.imread("images_for_threshold2/2.jpeg"), cv2.imread("images_for_threshold2/3.jpeg"),
          cv2.imread("images_for_threshold2/4.jpeg"), cv2.imread("images_for_threshold2/5.jpg")]
i = 0
j = 0

def image_segmentation(image_path):

    image = cv2.imread(image_path)


    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)


    masked_image = cv2.bitwise_and(image, image, mask=mask)

    corners = cv2.goodFeaturesToTrack(gray_image, maxCorners=100, qualityLevel=0.01, minDistance=10)
    corners = np.int0(corners)


    edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)


    sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
    gradient_magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)


    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(image, (x, y), 3, (0, 255, 0), -1)

    if lines is not None:
        for rho, theta in lines[:, 0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Отрисовка линий красными линиями

    gradient_magnitude = cv2.normalize(gradient_magnitude, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX,
                                       dtype=cv2.CV_8U)


    plt.figure(figsize=(10, 6))
    plt.subplot(131), plt.imshow(edges, cmap='gray'), plt.title('Edges')
    plt.axis('off')
    plt.subplot(132), plt.imshow(gradient_magnitude, cmap='gray'), plt.title('Gradient Magnitude')
    plt.axis('off')
    plt.subplot(133), plt.imshow(masked_image), plt.title('Detected Points')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

image_path = 'images_for_treshhold/1.jpg'
image_segmentation(image_path)


def apply_local_thresholding(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded_image = cv2.adaptiveThreshold(gray_image, 255,
                                              cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, 11, 2)
    return thresholded_image


def apply_local_thresholding_sauvola(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    window_size = 25
    k = 0.2

    
    thresholded_image = np.zeros_like(gray_image)
    for y in range(0, gray_image.shape[0], window_size):
        for x in range(0, gray_image.shape[1], window_size):
            window = gray_image[y:y + window_size, x:x + window_size]
            mean = np.mean(window)
            std = np.std(window)
            threshold = mean * (1 + k * ((std / 128) - 1))
            thresholded_image[y:y + window_size, x:x + window_size] = 255 * (
                        gray_image[y:y + window_size, x:x + window_size] < threshold)

    return thresholded_image

def open_image1():
        global i
        image = images1[i]
        i += 1
        i %= 5
        thresholded_image = apply_local_thresholding(image)
        display_image(thresholded_image)


def open_image2():
    global j
    image = images2[j]
    j += 1
    j %= 5
    thresholded_image = apply_local_thresholding_sauvola(image)
    display_image(thresholded_image)


def display_image(image):
    global label_image

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    photo = ImageTk.PhotoImage(image)

    if label_image:
        label_image.configure(image=photo)
        label_image.image = photo
    else:
        label_image = tk.Label(root, image=photo)
        label_image.image = photo
        label_image.pack()


root = tk.Tk()
root.title("Local Thresholding App")
root.geometry("800x800")

open_button = tk.Button(root, text="Threshold1", command=open_image1)
open_button.pack()

second_treshold = tk.Button(root, text="Threshold2", command=open_image2)
second_treshold.pack()

root.mainloop()



