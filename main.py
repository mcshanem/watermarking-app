from tkinter import Tk, NSEW, filedialog, ttk, messagebox, StringVar
from PIL import ImageTk, Image, ImageDraw, UnidentifiedImageError, ImageFont


def on_click(event):
    global original_img_file, current_img_file, img, watermark_text, watermark_size, watermark_opacity

    if current_img_file:
        txt = Image.new("RGBA", current_img_file.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        d.text(xy=(event.x-(int(watermark_size.get()) // 10), event.y-int(watermark_size.get())),
               text=watermark_text.get(),
               font_size=int(watermark_size.get()),
               fill=(255, 255, 255, int(watermark_opacity.get())))
        current_img_file = Image.alpha_composite(current_img_file, txt)
        img = ImageTk.PhotoImage(current_img_file)
        img_label['image'] = img

        current_img_file.save('./output-images/watermarked-output.png')


def open_image():
    global window, img_frame, img_label, original_img_file, current_img_file, img

    # Ask the user to select a file
    filename = filedialog.askopenfilename()

    if filename:
        # Attempt to open the file
        try:
            original_img_file = current_img_file = Image.open(filename).convert(mode='RGBA')
        except UnidentifiedImageError:
            messagebox.showerror(message='Unable to open file.')

        # Display the image
        img = ImageTk.PhotoImage(current_img_file)
        img_label['image'] = img
        img_label.grid()
        window.update()
        img_label.place(x=(img_frame.winfo_width() // 2) - (img_label.winfo_width() // 2),
                        y=(img_frame.winfo_height() // 2) - (img_label.winfo_height() // 2))


def reset_watermark():
    global original_img_file, current_img_file, img

    if current_img_file:
        current_img_file = original_img_file
        img = ImageTk.PhotoImage(current_img_file)
        img_label['image'] = img


# Create window
window = Tk()
window.title('Watermarking App')
window.geometry('1400x750')
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# Configure styles
s = ttk.Style()
s.configure('TButton', font='TkDefaultFont 16')
s.configure('TFrame')
s.configure('Image.TFrame', background='black', relief='sunken')

# Create main frame
mainframe = ttk.Frame(window)
mainframe.grid(column=0, row=0, sticky=NSEW)
mainframe.columnconfigure((0, 3), weight=1)
mainframe.columnconfigure((1, 2), weight=9)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=18)
mainframe.rowconfigure(2, weight=1)
mainframe.rowconfigure(3, weight=1)
mainframe.rowconfigure(4, weight=1)

# Create image frame
img_frame = ttk.Frame(mainframe, style='Image.TFrame')
img_frame.grid(column=1, row=1, columnspan=2, sticky=NSEW)

# Create empty image label
original_img_file = current_img_file = img = None
img_label = ttk.Label(img_frame, cursor='plus')
img_label.grid(column=1, row=1)
img_label.grid_remove()
img_label.bind('<Button-1>', on_click)

# Create Add Image button
add_image_btn = ttk.Button(mainframe, text='Add Image...', command=open_image)
add_image_btn.grid(column=1, row=2)

# Create Add Image button
reset_watermark_btn = ttk.Button(mainframe, text='Reset Watermark', command=reset_watermark)
reset_watermark_btn.grid(column=2, row=2)

# Create Watermark Text Input
watermark_text_frame = ttk.Frame(mainframe)
watermark_text_frame.grid(column=1, row=3)

watermark_text_label = ttk.Label(watermark_text_frame, text='Watermark Text:')
watermark_text_label.grid(column=0, row=0)

watermark_text = StringVar()
watermark_text_entry = ttk.Entry(watermark_text_frame, textvariable=watermark_text)
watermark_text_entry.grid(column=1, row=0)

# Create Watermark Size and Opacity Input
watermark_so_frame = ttk.Frame(mainframe)
watermark_so_frame.grid(column=2, row=3)

watermark_size_label = ttk.Label(watermark_so_frame, text='Watermark Size:')
watermark_size_label.grid(column=0, row=0)

watermark_size = StringVar(value='16')
watermark_size_combo = ttk.Spinbox(watermark_so_frame, textvariable=watermark_size, state='readonly', from_=2, to=120,
                                   increment=2)
watermark_size_combo.grid(column=1, row=0)

watermark_opacity_label = ttk.Label(watermark_so_frame, text='Watermark Opacity:')
watermark_opacity_label.grid(column=0, row=1)

watermark_opacity = StringVar(value='100')
watermark_opacity_spin = ttk.Spinbox(watermark_so_frame, textvariable=watermark_opacity, state='readonly', from_=0,
                                     to=255, increment=5)
watermark_opacity_spin.grid(column=1, row=1)

window.mainloop()
