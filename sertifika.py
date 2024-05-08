import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkfont
from PIL import Image, ImageDraw, ImageFont

import os
import sys

def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.title('Sertifika Oluşturucu')
custom_font = tkfont.Font(family="Helvetica", size=16, weight="bold")

l1 = tk.Label(root, text="Ders Açıklaması:" , font=custom_font)
l1.pack(pady=10, padx=10 )
e1 = tk.Entry(root, width=50 , font=custom_font)
e1.pack(pady=10, padx=10)

l2 = tk.Label(root, text="Sertifika Numarası Statik:" , font=custom_font)
l2.pack(pady=10, padx=10)
e2 = tk.Entry(root, width=50 , font=custom_font)
e2.pack(pady=10, padx=10)

l5 = tk.Label(root, text="Sertifika Numarası Sayısal:" , font=custom_font)
l5.pack(pady=10, padx=10)
e5 = tk.Entry(root, width=50 , font=custom_font)
e5.pack(pady=10, padx=10)

l3 = tk.Label(root, text="İsim ve Soyisim Listesi (virgülle ayrılmış):" , font=custom_font)
l3.pack(pady=10, padx=10)
e3 = tk.Entry(root, width=50 , font=custom_font)
e3.pack(pady=10, padx=10)

l4 = tk.Label(root, text="Tarih:" , font=custom_font)
l4.pack(pady=10, padx=10)
e4 = tk.Entry(root, width=50 , font=custom_font)
e4.pack(pady=10, padx=10)

def create_certificates():
    ders_aciklamasi = e1.get()
    sertifika_numarasi_statik = e2.get()
    isimler = e3.get().split(',')
    tarih = e4.get()
    sertifika_numarasi_sayisal = int(e5.get())

    # Sertifika şablonunu yükle
    template_image_path = get_resource_path('data/sertifika_sablonu.jpg')
    sertifika = Image.open(template_image_path)
    draw = ImageDraw.Draw(sertifika)

    # Fontları yükle
    font_path = "C:\Windows\Fonts\Arial.ttf"
    font_path_bold = "C:\Windows\Fonts\Arialbd.ttf"
    font_Xlarge = ImageFont.truetype(font_path_bold, 80)
    font_large = ImageFont.truetype(font_path, 40)
    font_small_b = ImageFont.truetype(font_path_bold, 16)
    font_small = ImageFont.truetype(font_path, 16)

    for index, isim in enumerate(isimler):
        # Yeni sertifika kopyasını oluştur
        sertifika_copy = sertifika.copy()
        draw = ImageDraw.Draw(sertifika_copy)

        isim_son = isim.strip().split(' ')
        for i , isim_s in enumerate(isim_son):
            if i == 0:
                isim = isim_s.capitalize()
            else:
                isim += ' ' + isim_s.upper()

        # Bilgileri sertifikaya yaz
        isim_bbox = draw.textbbox((0,0), isim , font=font_Xlarge)
        isim_h = isim_bbox[2] - isim_bbox[0]
        
        ders_bbox = draw.textbbox((0,0), ders_aciklamasi, font=font_large)
        ders_h = ders_bbox[2] - ders_bbox[0]
        
        isim_y = (sertifika.width - isim_h) / 2
        ders_y = (sertifika.width - ders_h) / 2
        draw.text((isim_y , 320), isim.strip(), font=font_Xlarge, fill="black")
        draw.text((ders_y, 464), ders_aciklamasi, font=font_large, fill="black")
        draw.text((655 , 854), tarih, font=font_small, fill="black")
        sertifika_numarasi_tam = f"{sertifika_numarasi_statik}{sertifika_numarasi_sayisal + index}"
        draw.text((680, 877), sertifika_numarasi_tam, font=font_small_b, fill="black")

        # Sertifikayı kaydet
        print(sertifika_numarasi_sayisal)
        output_path = os.path.join("sertifikalar", f"{isim.strip().replace(' ', '_')} {sertifika_numarasi_statik}{sertifika_numarasi_tam}.jpg")
        sertifika_copy.save(output_path)

b = tk.Button(root, text='Sertifikaları Oluştur', command=create_certificates , font=custom_font)
b.pack(pady=10, padx=10)

root.mainloop()
