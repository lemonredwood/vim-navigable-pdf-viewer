import tkinter as tk
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import threading
from pynput import keyboard

class PDFViewer:
    def __init__(self, master, pdf_path):
        self.master = master
        self.master.title("PDF Viewer")

        self.doc = fitz.open(pdf_path)
        self.current_page = 0
        self.pages_to_display = 2  # Number of pages to display vertically

        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.master, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.prev_button = tk.Button(self.master, text="Previous", command=self.show_prev_page)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.master, text="Next", command=self.show_next_page)
        self.next_button.pack(side=tk.RIGHT)

        self.img_tk_list = [None] * self.pages_to_display  # List to store ImageTk instances
        self.show_page()

    def show_page(self):
        for i in range(self.pages_to_display):
            page_index = self.current_page + i
            if page_index < self.doc.page_count:
                page = self.doc[page_index]
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                self.img_tk_list[i] = ImageTk.PhotoImage(img)
            else:
                self.img_tk_list[i] = None

        self.canvas.delete("all")  # Clear previous content
        y_offset = 0
        for img_tk in self.img_tk_list:
            if img_tk:
                self.canvas.create_image(0, y_offset, anchor=tk.NW, image=img_tk)
                y_offset += img_tk.height()

        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def show_next_page(self):
        if self.current_page < self.doc.page_count - 1:
            self.current_page += 1
            self.show_page()

    def run(self):
        self.master.mainloop()
        self.doc.close()

    def scroll_down(self):
        # Programmatically scroll down the canvas
        self.canvas.yview_scroll(1, "units")

    def on_key_event(self, key):
        try:
            char = key.char
            if char == 'j':
                self.scroll_down()
                print(f'\nKey {char} was pressed')
        except AttributeError:
            pass

def key_event_listener(viewer):
    with keyboard.Listener(on_press=viewer.on_key_event) as listener:
        listener.join()

if __name__ == "__main__":
    root = tk.Tk()
    viewer = PDFViewer(root, "sample.pdf")

    # Create a thread for keyboard input detection
    key_listener_thread = threading.Thread(target=key_event_listener, args=(viewer,))
    key_listener_thread.start()

    viewer.run()

