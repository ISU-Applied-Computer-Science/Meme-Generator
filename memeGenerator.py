import os
import textwrap
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import ImageTk, Image, ImageDraw, ImageFont

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        self.fileName = ""

        self.Button1 = tk.Button(command=self.openImage)
        self.Button1.place(relx=0.787, rely=0.276, height=24, width=157)
        self.Button1.configure(background="#d8eac8")
        self.Button1.configure(cursor="hand1")
        self.Button1.configure(text="Открыть изображение")

        self.Button2 = tk.Button(command=self.genetareImage)
        self.Button2.place(relx=0.787, rely=0.399, height=44, width=157)
        self.Button2.configure(background="#c1e4f0")
        self.Button2.configure(cursor="hand1")
        self.Button2.configure(text="Сгенерировать мем")

        self.Button3 = tk.Button(command=self.saveImage)
        self.Button3.place(relx=0.787, rely=0.583, height=24, width=157)
        self.Button3.configure(background="#f3c9be")
        self.Button3.configure(cursor="hand1")
        self.Button3.configure(text="Сохранить изображение")

        self.Label1 = tk.Label()
        self.Label1.place(relx=0.787, rely=0.0, height=31, width=122)
        self.Label1.configure(text="← Верхняя надпись")

        self.Label2 = tk.Label()
        self.Label2.place(relx=0.787, rely=0.89, height=21, width=122)
        self.Label2.configure(text="← Нижняя надпись")

        self.Entry1 = tk.Entry()
        self.Entry1.place(relx=0.013, rely=0.021,height=20, relwidth=0.754)

        self.Entry2 = tk.Entry()
        self.Entry2.place(relx=0.013, rely=0.89,height=20, relwidth=0.754)

        self.Canvas1 = tk.Canvas(width=400, height=300)
        self.Canvas1.place(relx=0.013, rely=0.089, relheight=0.791, relwidth=0.756)
        self.Canvas1.configure(background="#d1d1d1")
        self.Canvas1.configure(borderwidth="4")
        self.Canvas1.configure(relief="ridge")
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")
        
    def characterLimit(self, entryText):
        if len(entryText.get()) > 30:
            return True
        else:
            return False

    def checkFiles(self):
        print(self.fileName)
        if (self.fileName == ""):
            return True
        else:
            return False

    def openImage(self):
        #print("Вызвана функция openImage()")
        self.fileName = fd.askopenfilename(filetypes=[('JPG картинка','*.jpg'),('PNG картинка','*.png')])
        self.im = Image.open(self.fileName)
        imResize = self.im.resize((590, 252),Image.ANTIALIAS)
        self.Canvas1.image = ImageTk.PhotoImage(imResize)
        self.Canvas1.create_image(0, 0, image=self.Canvas1.image, anchor='nw')

    def genetareImage(self):
        if self.characterLimit(self.Entry1) or self.characterLimit(self.Entry2):
            tk.messagebox.showwarning("Лимит", "Максимальное количество символов на каждую надпись не превышает 30 символов")
            return 0

        if self.checkFiles():
            tk.messagebox.showwarning("Не выбран файл", "Откройте картинку, чтобы сгенерировать мем")
            self.openImage()
            return 0

        self.Canvas1.delete("all")
        
        self.im = Image.open(self.fileName)
        draw = ImageDraw.Draw(self.im)
        imageWidth, imageHeight = self.im.size
        topText = self.Entry1.get()
        bottomText = self.Entry2.get()

        font = ImageFont.truetype(font="./font/Attractive-Heavy.ttf", size=int(imageHeight/10))
        
        topText = topText.upper()
        bottomText = bottomText.upper()

        charWidth, charHeight = font.getsize('A')
        charsPerLine = imageWidth // charWidth

        topLines = textwrap.wrap(topText, width=charsPerLine)
        bottomLines = textwrap.wrap(bottomText, width=charsPerLine)

        y = 10
        for line in topLines:
            line_width, line_height = font.getsize(line)
            x = (imageWidth - line_width)/2
            draw.text((x,y), line, fill='white', font=font, stroke_fill='black', stroke_width=2)
            y += line_height

        # draw bottom lines
        y = imageHeight - charHeight * len(bottomLines) - 15
        for line in bottomLines:
            line_width, line_height = font.getsize(line)
            x = (imageWidth - line_width)/2
            draw.text((x,y), line, fill='white', font=font, stroke_fill='black', stroke_width=2)
            y += line_height

        imResize = self.im.resize((590, 252),Image.ANTIALIAS)
        self.Canvas1.image = ImageTk.PhotoImage(imResize)
        self.Canvas1.create_image(0, 0, image=self.Canvas1.image, anchor='nw')
        #print("Вызвана функция genetareImage()")

    def saveImage(self):
        if self.checkFiles():
            tk.messagebox.showwarning("Не выбран файл", "Откройте картинку, чтобы сохранить мем")
            self.openImage()
            return 0
            
        self.fileName = fd.asksaveasfilename(defaultextension=".jpg",initialfile = "Мем",filetypes=[('JPG картинка','*.jpg')])
        self.im.save(self.fileName, 'JPEG')

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Генератор мемов")
    root.geometry("788x326+640+280")
    root.resizable(False, False)
    root.mainloop()
