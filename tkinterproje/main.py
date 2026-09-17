from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox, Treeview, Notebook

window = Tk()
window.geometry("1280x720")
window.title("Kapsamlı Tkinter Kontrol Paneli")

#menü çubuğu
menubar = Menu(window)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="çıkış",command = window.quit)
menubar.add_cascade(label="Dosya", menu=file_menu)
window.config(menu=menubar)

#ana pained window yatay bölme
main_pw = PanedWindow(window,orient="horizontal" )
main_pw.pack(fill="both",expand=True)

left_frame = Frame(main_pw,bg="#f0f0f0")
main_pw.add(left_frame)

right_pw = PanedWindow(main_pw,orient="vertical")
main_pw.add(right_pw)

top_right_frame = Frame(right_pw,bg="white")
bottom_right_frame = Frame(right_pw,bg="#f9f9f9")
right_pw.add(top_right_frame)
right_pw.add(bottom_right_frame)

#sol panele label , entry , button , combobox , radiobutton , checkbutton ekliyoruz
Label(left_frame,text="Veri Girişi:",fg="black",bg="#f0f0f0").grid(row=0,column=0,padx=10,pady=5,sticky=W)
user_entry = Entry(left_frame,width=25,bg="gray")
user_entry.grid(row=1,column=0,padx=10,pady=5,sticky=W)

#filedialog ve messagebox
def dosya_yukle():
    dosya_yolu = filedialog.askopenfilename(filetypes=[("CSV Dosyaları", "*.csv"), ("Tüm Dosyalar", "*.*")])
    if dosya_yolu:
        text_editor.insert(END, f"Dosya Açıldı : {dosya_yolu}\n")

        #CSV dosyasını pandas ile oku
        df = pd.read_csv(dosya_yolu)

        #Mevcut grafiği temizle
        ax.clear()

        #Dosyadaki veriyi grafiğe çizdir (Örneğin 'Close' sütunu varsa)
        if 'Close' in df.columns:
            ax.plot(range(len(df)), df['Close'], color="blue")
            ax.set_title(dosya_yolu.split("/")[-1])  # Grafik başlığına dosya adını yaz
        else:
            # Eğer 'Close' sütunu yoksa ilk sayısal sütunu baz al
            ax.plot(range(len(df)), df.iloc[:, 0], color="green")
            ax.set_title("Yüklenen Veri")

        # 4. Eksenleri yeniden hesapla ve grafiği ekranda yenile (draw)
        ax.relim()
        ax.autoscale_view()
        canvas.draw()
Button(left_frame,text="Dosya Seç:",bg="white",command=dosya_yukle).grid(row=2,column=0,padx=10,pady=5,sticky=W)

#combobox
def piyasa_degisti(event):
    secilen_piyasa = combo.get()
    text_editor.insert(END, f"Piyasa değiştirildi: {secilen_piyasa}\n")
combo = Combobox(left_frame,values=["BIST100", "EUR/USD", "BTC/USDT"],state="readonly")
combo.bind("<<ComboboxSelected>>", piyasa_degisti)
combo.grid(row=3,column=0,padx=10,pady=5,sticky=W)
combo.current(0)

#radiobutton
def modu_kontrol_et():
    secilen_mod = radio_var.get()
    print(f"Aktif mod : {secilen_mod}")
    text_editor.insert(END,f"Mod : {secilen_mod}\n")

radio_var = StringVar(value="Mod 1")
Radiobutton(left_frame,text="Mod 1",fg="black",variable=radio_var,value="Mod 1",bg="#f0f0f0",command=modu_kontrol_et).grid(row=4,column=0,padx=10,pady=5,sticky=W)
Radiobutton(left_frame,text="Mod 2",fg="black",variable=radio_var,value="Mod 2",bg="#f0f0f0",command=modu_kontrol_et).grid(row=5,column=0,padx=10,pady=5,sticky=W)

#checkbutton
def bildirim_ayar_degisti():
    if check_var.get() == "1":
        messagebox.showinfo("Bildirimler", "Bildirimler aktif hale getirildi.")
    else:
        messagebox.showinfo("Bildirimler", "Bildirimler kapatıldı.")
check_var = StringVar(value="1")
Checkbutton(left_frame,text="Bildirimleri Aç",variable=check_var,fg="black",bg="#f0f0f0",command=bildirim_ayar_degisti).grid(row=6,column=0,padx=10,pady=5,sticky=W)

#sol panelin altına verileri listelemek için treeview ve listbox yerleştiriyoruz
#treeview
tree = Treeview(left_frame,columns=("İşlem","Durum"),show="headings",height=4)
tree.heading("İşlem",text="İşlem")
tree.heading("Durum",text="Durum")
tree.insert("",0,values=("Bağlantı","Aktif"))
tree.grid(row=7,column=0,padx=10,pady=5)

#listbox
listbox = Listbox(left_frame,height=3,width=30)
listbox.grid(row=8,column=0,padx=10,pady=5)
listbox.insert(END,"Sistem Başlatıldı")
listbox.insert(END,"Sistem Kapatıldı")
listbox.insert(END,"Sistem Açıldı")

#Sağ üst kısma Notebook (Tabs) koyup içine Matplotlib grafiği (Plot) gömüyoruz.
#Grafiğe tıklandığında ise Mouse Event çalışıyor.

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

notebook = Notebook(top_right_frame)
notebook.pack(fill="both",expand=True,padx=10,pady=10)

tab_line = Frame(notebook)
notebook.add(tab_line,text="Grafik Sekmesi")

#matplotlib plot
# Başlangıçta boş ve bilgilendirici bir grafik alanı oluşturuyoruz
fig, ax = plt.subplots(figsize=(4.5, 2.8), dpi=100)
ax.set_title("Grafik yüklemek için dosya seçiniz")
ax.set_xticks([])
ax.set_yticks([])

canvas = FigureCanvasTkAgg(fig, master=tab_line)
canvas.draw()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

#mouse event
def on_click(event):
    if event.xdata and event.ydata:
        messagebox.showinfo("Mouse tıklaması",f"Koordinat X={event.xdata:.2f} Y={event.ydata:.2f}")
fig.canvas.mpl_connect('button_press_event', on_click)

#text editor ve scrollbar
text_frame = Frame(bottom_right_frame)
text_frame.pack(fill="both",expand=True,padx=10,pady=10)

text_editor = Text(text_frame,wrap="word")
text_editor.pack(side="left",fill="both",expand=True)
text_editor.insert(END,"Loglar ve notlar burada görünecek\n")

scrollbar = Scrollbar(text_frame,command=text_editor.yview,orient="vertical")
scrollbar.pack(side="right",fill="y")
text_editor.config(yscrollcommand=scrollbar.set)

#işlevler
def veri_isle():
    girilen_deger = user_entry.get()
    if girilen_deger:
        text_editor.insert(END,f"Girilen değer:{girilen_deger}\n")
        messagebox.showinfo("Başarılı", f"'{girilen_deger} sisteme kaydedildi.")
    else:
        messagebox.showwarning("Uyarı", "Lütfen bir şeyler yazın!")
Button(left_frame, text="Veriyi Kaydet", command=veri_isle).grid(row=1,column=1)

window.mainloop()
