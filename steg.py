import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Convert encoding data into 8-bit binary form using ASCII value of characters
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

# Pixels are modified according to the 8-bit binary data and finally returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1

        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

def select_image():
    img_path = filedialog.askopenfilename()
    if img_path:
        return img_path
    else:
        messagebox.showerror("Error", "No file selected!")
        return None

def save_image(newimg, encoded):
    if encoded:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            newimg.save(save_path)
            messagebox.showinfo("Success", "Image Encoded and Saved Successfully!")
        else:
            messagebox.showerror("Error", "Save operation cancelled!")
    else:
        messagebox.showinfo("No Encoding", "The image was not encoded as no data was provided.")

def encode():
    encode_window = tk.Toplevel(root)
    encode_window.title("Encode Data")
    encode_window.configure(bg="#34495e")

    text_label = tk.Label(encode_window, text="Enter Data to Encode:", font=("Helvetica", 14), fg="#ecf0f1", bg="#34495e")
    text_label.pack(pady=10)

    text_entry = tk.Text(encode_window, height=4, width=50, font=("Helvetica", 14), bg="#ecf0f1", fg="#2c3e50")
    text_entry.pack(pady=10)

    def perform_encoding():
        data = text_entry.get("1.0", tk.END)
        img_path = select_image()
        if img_path:
            image = Image.open(img_path, 'r')
            newimg = image.copy()
            if data.strip():
                encode_enc(newimg, data.strip())
                save_image(newimg, encoded=True)
            else:
                save_image(newimg, encoded=False)

    encode_data_button = tk.Button(encode_window, text="Encode Data", command=perform_encoding, font=("Helvetica", 14), fg="#2c3e50", bg="#ecf0f1")
    encode_data_button.pack(pady=10)

    close_button = tk.Button(encode_window, text="Close", command=encode_window.destroy, font=("Helvetica", 14), fg="#ecf0f1", bg="#e74c3c")
    close_button.pack(pady=10)

def decode():
    img_path = select_image()
    if img_path:
        image = Image.open(img_path, 'r')
        data = ''
        imgdata = iter(image.getdata())

        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]

            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                break

        show_decoded_data(data)
        clear_screen()

def show_decoded_data(data):
    decode_window = tk.Toplevel(root)
    decode_window.title("Decoded Data")
    decode_window.configure(bg="#34495e")

    data_label = tk.Label(decode_window, text="Decoded Data:", font=("Helvetica", 14), fg="#ecf0f1", bg="#34495e")
    data_label.pack(pady=10)

    data_text = tk.Text(decode_window, height=10, width=50, font=("Helvetica", 14), bg="#ecf0f1", fg="#2c3e50")
    data_text.pack(pady=10)
    data_text.insert(tk.END, data)
    data_text.config(state=tk.DISABLED)

    close_button = tk.Button(decode_window, text="Close", command=decode_window.destroy, font=("Helvetica", 14), fg="#ecf0f1", bg="#e74c3c")
    close_button.pack(pady=10)

def clear_screen():
    encode_button.config(state=tk.NORMAL)
    decode_button.config(state=tk.NORMAL)

def exit_program():
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Image Steganography")
root.geometry("600x400")
root.configure(bg="#34495e")

# Main frame
main_frame = tk.Frame(root, bg="#34495e", pady=20)
main_frame.pack()

# Title
title = tk.Label(main_frame, text="Image Steganography", font=("Helvetica", 28), fg="#ecf0f1", bg="#34495e")
title.pack(pady=10)

# Buttons frame
button_frame = tk.Frame(main_frame, bg="#34495e")
button_frame.pack(pady=10)

encode_button = tk.Button(button_frame, text="Encode", command=encode, font=("Helvetica", 16), fg="#34495e", bg="#ecf0f1", width=12)
encode_button.grid(row=0, column=0, padx=10, pady=10)

decode_button = tk.Button(button_frame, text="Decode", command=decode, font=("Helvetica", 16), fg="#34495e", bg="#ecf0f1", width=12)
decode_button.grid(row=0, column=1, padx=10, pady=10)

exit_button = tk.Button(button_frame, text="Exit", command=exit_program, font=("Helvetica", 16), fg="#ecf0f1", bg="#e74c3c", width=12)
exit_button.grid(row=1, column=0, columnspan=2, pady=20)

root.mainloop()