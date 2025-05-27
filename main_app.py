
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from manual_tools import apply_multi_region_blur, apply_freehand_blur, apply_redaction, apply_crop

original_image = None
adjusted_image = None

def load_image():
    global original_image, adjusted_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if not file_path:
        return
    original_image = cv2.imread(file_path)
    adjusted_image = original_image.copy()
    update_image()

def update_image(*args):
    global adjusted_image
    if original_image is None:
        return
    alpha = contrast_scale.get() / 100.0
    beta = brightness_scale.get() - 100
    adjusted_image = cv2.convertScaleAbs(original_image, alpha=alpha, beta=beta)
    show_image(adjusted_image)

def show_image(img):
    bgr_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(bgr_image)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    image_label.imgtk = img_tk
    image_label.config(image=img_tk)

def save_image():
    if adjusted_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if file_path:
            cv2.imwrite(file_path, adjusted_image)

def apply_region_blur():
    global adjusted_image
    if adjusted_image is not None:
        result = apply_multi_region_blur(adjusted_image.copy())  # important to use .copy()
        if result is not None:
            adjusted_image = result
            show_image(adjusted_image)

def apply_freehand():
    global adjusted_image
    if adjusted_image is not None:
        adjusted_image = apply_freehand_blur(adjusted_image)
        show_image(adjusted_image)

def apply_redact():
    global adjusted_image
    if adjusted_image is not None:
        adjusted_image = apply_redaction(adjusted_image)
        show_image(adjusted_image)

def apply_crop_tool():
    global adjusted_image
    if adjusted_image is not None:
        adjusted_image = apply_crop(adjusted_image)
        show_image(adjusted_image)

root = Tk()
root.title("PrivacyGuard: Image Tool")

btn_frame = Frame(root)
btn_frame.pack(pady=10)

Button(btn_frame, text="Load Image", command=load_image).pack(side=LEFT, padx=5)
Button(btn_frame, text="Save Image", command=save_image).pack(side=LEFT, padx=5)
Button(btn_frame, text="Multi-Region Blur", command=apply_region_blur).pack(side=LEFT, padx=5)
Button(btn_frame, text="Freehand Blur", command=apply_freehand).pack(side=LEFT, padx=5)
Button(btn_frame, text="Redact (Solid Fill)", command=apply_redact).pack(side=LEFT, padx=5)
Button(btn_frame, text="Crop Tool", command=apply_crop_tool).pack(side=LEFT, padx=5)

contrast_scale = Scale(root, from_=50, to=300, orient=HORIZONTAL, label="Contrast x100", command=update_image)
contrast_scale.set(100)
contrast_scale.pack(fill=X, padx=10)

brightness_scale = Scale(root, from_=0, to=200, orient=HORIZONTAL, label="Brightness", command=update_image)
brightness_scale.set(100)
brightness_scale.pack(fill=X, padx=10)

image_label = Label(root)
image_label.pack(padx=10, pady=10)

root.mainloop()
