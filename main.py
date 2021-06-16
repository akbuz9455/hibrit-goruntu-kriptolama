import tkinter as tk
from tkinter import filedialog as fd
import os
import encrypt as e
import decrypt as d
import threading as thread
import Key as k
import base64

class MainApplication:
    def __init__(self, app, key):
        self.app = app
        self.app.geometry('%sx%s' % (int(self.app.winfo_screenwidth()/2), int(app.winfo_screenheight()/2)))
        self.app.resizable(width=False, height=False)
        self.app.configure(background='#00ACC1')
        ##self.app['background']='#856ff8'
        
        self.listFilenames = []

        self.choose_label_text = tk.StringVar()
        self.choose_label_text.set("Şifrelenecek görüntüleri seçin")
        self.encrypt_text = tk.StringVar()
        self.encrypt_text.set("Encrypt")
        self.app.title("Image "+self.encrypt_text.get()+"ion - Ramazan Şerif Akbuz - Hamza Dağdelen")

        #Mode
        self.selection_value = tk.IntVar()
        self.selection_value.set(1)
        self.mode_label = tk.Label(self.app, text="Mod Seç:", font=('Helvetica', 9))
        self.mode_label.configure(background='#00ACC1')
        self.mode_radio_e = tk.Radiobutton(self.app, text="Şifrele", variable=self.selection_value, value=1, command=self.selection)
        self.mode_radio_d = tk.Radiobutton(self.app, text="Şifre Çöz", variable=self.selection_value, value=2, command=self.selection)

        #Choose
        self.choose_label = tk.Label(self.app, textvariable=self.choose_label_text, font=('Helvetica', 10))
        self.choose_entry = tk.Text(self.app, width=0, height=0)
        self.choose_entry.config(state=tk.DISABLED)
        self.add_button = tk.Button(self.app, text ="Ekle", command=self.chooseImg)
        self.clear_button = tk.Button(self.app, text ="Temizle", command=lambda:[self.choose_entry.config(state=tk.NORMAL), self.choose_entry.delete(1.0, tk.END), self.choose_entry.config(state=tk.DISABLED), self.listFilenames.clear()])

        #Output
        self.output_label = tk.Label(self.app, text="Çıktı hedefini seçin", font=('Helvetica', 10))
        self.output_entry = tk.Entry(self.app)
        self.output_entry.config(state=tk.DISABLED)
        self.output_button = tk.Button(self.app, text="Klasör Seç", command=self.chooseDestination)

        #Key
        self.private_key_label = tk.Label(self.app, text="Özel Anahtarınız: ", font=('Helvetica', 10))
        self.private_key_entry = tk.Entry(app, width=0)
        self.private_key_entry.insert(0, key)
        self.private_key_entry.config(state=tk.DISABLED)
        self.key_label_text = tk.StringVar()
        self.key_label_text.set("Geri Kurtarma Anahtarını Girin ")
        self.public_key_label = tk.Label(self.app, textvariable=self.key_label_text, font=('Helvetica', 10))
        self.public_key_entry = tk.Entry(app, width=0)

        #Progress
        self.progressText = tk.StringVar()
        self.progress_label = tk.Label(self.app, textvariable=self.progressText, font=('Helvetica', 9))
        
        #Encrypt
        self.encrypt_button = tk.Button(self.app, textvariable=self.encrypt_text, command= lambda: thread._start_new_thread(self.beginEncryption, (self.listFilenames, key, self.public_key_entry.get())))
        self.base64_buttpn = tk.Button(self.app, text="Base65 Çevir", font=('Helvetica', 9), command=self.base64isyapma)

        #Grid
        self.app.grid_columnconfigure(2, weight=1)
        self.app.grid_rowconfigure(3, weight=1)

        self.mode_label.grid(row=0, column=0, padx=(8,0), pady=(10,5), sticky='wn')
        self.mode_radio_e.grid(row=0, column=1, padx=(4,0), pady=(10,0), sticky='wn')
        self.mode_radio_d.grid(row=0, column=2, padx=(4,0), pady=(10,0), sticky='wn')

        self.choose_label.grid(row=1, column=0, padx=(8,0), pady=(10,5), sticky='wn', columnspan=3)
        self.choose_entry.grid(row=2, column=0, sticky='wens', padx=(10,5), rowspan=3, columnspan=3)
        self.add_button.grid(row=2, column=3, sticky='wen', padx=(5,10))
        self.clear_button.grid(row=3, column=3, sticky='wes', padx=(5,10), pady=(5,0))
        
        self.output_label.grid(row=5, column=0, padx=(8,0), pady=(10,5), sticky='wn', columnspan=3)
        self.output_entry.grid(row=6, column=0, sticky='wen', padx=(10,5), columnspan=3)
        self.output_button.grid(row=6, column=3, sticky='wen', padx=(5,10))

        self.private_key_label.grid(row=7, column=0, padx=(8,0), pady=(5,5), sticky='wn', columnspan=3)
        self.private_key_entry.grid(row=8, column=0, sticky='wen', padx=10, columnspan=4)
        self.public_key_label.grid(row=9, column=0, padx=(8,0), pady=(5,5), sticky='wn', columnspan=3)
        self.public_key_entry.grid(row=10, column=0, sticky='wen', padx=10, columnspan=4)
        
        self.progress_label.grid(row=11, column=0, sticky='swn', padx=(7,0), pady=(20,10), columnspan=3)

        self.encrypt_button.grid(row=11, column=3, sticky='senw', padx=(0,10), pady=(20,10))
        self.base64_buttpn.grid(row=12, column=3, sticky='senw', padx=(0,10), pady=(0,10))

    def selection(self):
        if self.selection_value.get() == 1:
            self.choose_label_text.set("Şifrelenecek görüntüleri seçin")
            self.encrypt_text.set("Şifrele")
            self.key_label_text.set("Geri Kurtarma Anahtarını Girin: ")
        else:
            self.choose_label_text.set("Şifresi çözülecek görüntüleri seçin")
            self.encrypt_text.set("Şifresini Çöz")
            self.key_label_text.set("Gönderenin Ortak Anahtarını Girin: ")

    def chooseImg(self):
        filename = fd.askopenfilenames(title='Resimleri seçin')
        for i in filename:
            self.listFilenames.append(i)
            self.choose_entry.config(state=tk.NORMAL)
            self.choose_entry.insert(tk.INSERT, i+'\n')
            self.choose_entry.config(state=tk.DISABLED)

    def chooseDestination(self):
        path = fd.askdirectory(title='Çıkış hedefini seçin')
        self.output_entry.config(state=tk.NORMAL)
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(tk.INSERT, path)
        self.output_entry.config(state=tk.DISABLED)

    def beginEncryption(self, listFilenames, private_key, public_key):
        key = k.Key(private_key, public_key)
        self.changeButtonState(tk.DISABLED)
        self.changeTextBoxState(tk.DISABLED)
        for i in listFilenames:
            self.showBar(i, listFilenames.index(i), len(listFilenames))
            if self.selection_value.get() == 1:
                e.encrypt(i, self.output_entry.get(), key)
            if self.selection_value.get() == 2:
                d.decrypt(i, self.output_entry.get(), key)
        self.progressText.set(self.encrypt_text.get()+"ion finished. ("+str(len(listFilenames))+"/"+str(len(listFilenames))+")")
        self.clearAllText()
        self.changeButtonState(tk.NORMAL)

    def showBar(self, filename, index, length):
        self.progressText.set(self.encrypt_text.get()+"ing "+os.path.basename(filename)+" ("+str(index)+"/"+str(length)+")")
        self.app.update_idletasks()

    def changeButtonState(self, s):
        self.add_button.config(state=s)
        self.clear_button.config(state=s)
        self.output_button.config(state=s)
        self.encrypt_button.config(state=s)

    def changeTextBoxState(self, s):
        self.output_entry.config(state=s)
        self.choose_entry.config(state=s)
        self.public_key_entry.config(state=s)

    def clearAllText(self):
        self.changeTextBoxState(tk.NORMAL)
        self.listFilenames.clear()
        self.choose_entry.delete(1.0, tk.END)
        self.output_entry.delete(0, tk.END)
        self.public_key_entry.delete(0,tk.END)
        self.changeTextBoxState(tk.DISABLED)
        self.public_key_entry.config(state=tk.NORMAL)
        

    def base64isyapma(self):
        with open(self.listFilenames, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        with open('resim.txt', 'w') as f:
            f.write(my_string.decode("utf-8"))
       

        
class LoginApp:
    def __init__(self, app):
        self.app = app
        self.app.geometry('%sx%s' % (int(self.app.winfo_screenwidth()/2), int(app.winfo_screenheight()/3)))
        self.app.resizable(width=False, height=False)
        self.app.title("Giriş Sayfası - RAMAZAN ŞERİF AKBUZ - HAMZA DAĞDELEN")
        self.frame = tk.Frame(self.app)
        self.app.configure(background='#00ACC1')
        self.login_label = tk.Label(self.frame, text="Özel Anahtarla Giriş Yapın", font=('Helvetica', 10, 'bold'))
        self.login_entry = tk.Entry(self.frame)
        self.login_button = tk.Button(self.frame, text="Giriş Yap", font=('Helvetica', 9), command=lambda:self.start_intro(self.login_entry.get()))
        self.generate_button = tk.Button(self.frame, text="Yeni Anahtar Çifti Oluştur", font=('Helvetica', 8), command=self.generateKeyPairs)

        self.login_label.grid(pady=(0,8))
        self.login_entry.grid(pady=(0,5), sticky='enw')
        self.login_button.grid(pady=(5,5), ipadx=5, sticky='enw')
        self.generate_button.grid(pady=(5,0), sticky='enw')

        self.frame.place(relx=.5, rely=.5, anchor="c")

    def generateKeyPairs(self):
        files = [('Text Document', '*.txt')]
        f = fd.asksaveasfile(title = "Dizin seçin", initialfile='keypairs', filetypes=files, defaultextension=files)
        if f is None:
            return
        [private, public] = k.genKeyPairs()
        text = "private_key = "+str(private)+"\npublic_key = "+str(public)
        f.write(text)
        f.close()

    def start_intro(self, key):
        self.app.destroy()
        new_app = tk.Tk()
        main_app = MainApplication(new_app, key)
        new_app.mainloop()

app = tk.Tk()
login_app = LoginApp(app)
app.mainloop()