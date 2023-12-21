import time
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import tkinter as tk

class PDFViewer:
    def __init__(self, master, pdf_path):
        self.master = master
        self.master.title("PDF Viewer")

        self.doc = fitz.open(pdf_path)
        self.current_page = 0

        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.master, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.prev_button = tk.Button(self.master, text="Previous", command=self.show_prev_page)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.master, text="Next", command=self.show_next_page)
        self.next_button.pack(side=tk.RIGHT)

        self.img_tk = None  # Initialize img_tk as an instance variable
        self.show_page()

    def show_page(self):
        page = self.doc[self.current_page]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        self.img_tk = ImageTk.PhotoImage(img)

        self.canvas.delete("all")  # Clear previous content
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
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

    def perform_scrolling(self):
        # Schedule scrolling after a delay
        self.scroll_down()
        self.master.after(1000, self.scroll_down)  # 1000 milliseconds (1 second) delay
        self.master.after(2000, self.scroll_down)  # 2000 milliseconds (2 seconds) delay
        self.master.after(3000, self.scroll_down)  # 3000 milliseconds (3 seconds) delay

if __name__ == "__main__":
    pdf_path = "sample.pdf"
    root = tk.Tk()
    viewer = PDFViewer(root, pdf_path)
    viewer.perform_scrolling()
    viewer.run()

