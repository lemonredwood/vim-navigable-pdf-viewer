import tkinter as tk
from tkinter import ttk
import fitz  # PyMuPDF

class PDFViewerApp:
    def __init__(self, root, pdf_path):
        self.root = root
        self.root.title("PDF Viewer")

        # Create a Tkinter Text widget to display PDF content
        self.text_widget = tk.Text(root, wrap=tk.WORD, width=80, height=40)
        self.text_widget.pack(expand=tk.YES, fill=tk.BOTH)

        # Create a vertical scrollbar for the Text widget
        self.scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)

        # Open the PDF file
        self.pdf_document = fitz.open(pdf_path)

        # Display the first page
        self.display_page(0)

    def display_page(self, page_number):
        # Get the page
        page = self.pdf_document[page_number]

        # Extract text from the page
        text = page.get_text()

        # Clear the Text widget and insert the new text
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert(tk.END, text)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    pdf_path = "sample.pdf"  # Replace with the path to your PDF file

    root = tk.Tk()
    app = PDFViewerApp(root, pdf_path)
    app.run()

