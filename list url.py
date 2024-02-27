import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime

class URLScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Scanner")
        self.root.geometry("400x400")

        self.url_label = tk.Label(root, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        self.url_entry.bind("<Control-c>", self.copy_url)
        self.url_entry.bind("<Control-v>", self.paste_url)

        self.scan_button = tk.Button(root, text="Scan URL", command=self.scan_url)
        self.scan_button.pack()

        self.save_button = tk.Button(root, text="Save Links", command=self.save_links)
        self.save_button.pack()

        self.clear_button = tk.Button(root, text="Clear Status", command=self.clear_status)
        self.clear_button.pack()

        self.log_text = scrolledtext.ScrolledText(root, width=50, height=15, wrap=tk.WORD)
        self.log_text.pack()

        self.log_text.bind("<Control-c>", self.copy_status)

        self.scanned_urls = set()

    def scan_url(self):
        initial_url = self.url_entry.get()

        def recursive_scan(url):
            if url in self.scanned_urls:
                return
            self.scanned_urls.add(url)

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    self.log_text.insert(tk.END, f"Scanning: {url}\n")
                    extract_links_and_scan(url, soup)
                else:
                    self.log_text.insert(tk.END, f"Failed to fetch URL: {url}. Status code: {response.status_code}\n")
            except Exception as e:
                self.log_text.insert(tk.END, f"An error occurred while scanning {url}: {e}\n")

        def extract_links_and_scan(base_url, soup):
            for link in soup.find_all('a', href=True):
                absolute_link = urljoin(base_url, link['href'])
                parsed_link = urlparse(absolute_link)
                if parsed_link.netloc == parsed_url.netloc:
                    recursive_scan(absolute_link)

        try:
            parsed_url = urlparse(initial_url)
            recursive_scan(initial_url)
            self.log_text.insert(tk.END, "Scan completed successfully!\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_links(self):
        initial_url = self.url_entry.get()
        parsed_url = urlparse(initial_url)
        filename = f"{parsed_url.netloc}_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(filename, "w") as file:
            for link in self.scanned_urls:
                file.write(link + "\n")
        self.log_text.insert(tk.END, f"Scanned links saved to {filename}\n")

    def clear_status(self):
        self.log_text.delete(1.0, tk.END)

    def copy_url(self, event):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.url_entry.get())

    def paste_url(self, event):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, self.root.clipboard_get())

    def copy_status(self, event):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.log_text.selection_get())

if __name__ == "__main__":
    root = tk.Tk()
    url_scanner = URLScanner(root)
    root.mainloop()
