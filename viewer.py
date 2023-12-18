import fitz  # PyMuPDF
from PIL import Image, ImageTk
import tkinter as tk

class PDFViewer:
    def __init__(self, master, pdf_path):
        self.master = master
        self.master.title("PDF Viewer")

        self.doc = fitz.open(pdf_path)
        self.current_page = 0

        self.label = tk.Label(self.master)
        self.label.pack()

        self.prev_button = tk.Button(self.master, text="Previous", command=self.show_prev_page)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.master, text="Next", command=self.show_next_page)
        self.next_button.pack(side=tk.RIGHT)

        self.show_page()

    def show_page(self):
        page = self.doc[self.current_page]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        img_tk = ImageTk.PhotoImage(img)

        self.label.config(image=img_tk)
        self.label.image = img_tk

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

if __name__ == "__main__":
    pdf_path = "sample.pdf"
    root = tk.Tk()
    viewer = PDFViewer(root, pdf_path)
    viewer.run()

