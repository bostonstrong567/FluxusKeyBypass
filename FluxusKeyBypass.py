import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk, scrolledtext
import threading

class Response:
    def __init__(self, url, content):
        self.url = url
        self.content = content

async def request(session, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Referer": "https://linkvertise.com/"
    }
    async with session.get(url, headers=headers) as resp:
        content = await resp.text()
    return Response(url, content)

def start_request():
    hwid = hwid_entry.get()
    urls = [f"https://flux.li/windows/start.php?updated_browser=true&HWID={hwid}", "https://fluxteam.net/windows/checkpoint/check1.php", "https://fluxteam.net/windows/checkpoint/check2.php", "https://fluxteam.net/windows/checkpoint/main.php"]

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [request(session, url) for url in urls]
            responses = await asyncio.gather(*tasks)

            for response in responses:
                result_area.insert(END, f"Bypassed {response.url}\n")

            document = BeautifulSoup((await request(session, urls[-1])).content, 'html.parser')
            key = document.select_one("main code:nth-of-type(2)")
            result_area.insert(END, f"\nYour key is: {key.get_text().strip() if key else 'Error! Try closing fluxus browser tabs'}\n")

    threading.Thread(target=asyncio.run, args=(main(),)).start()

root = Tk()
root.title("HWID Bypass")
root.configure(background='#333')

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background='#333')
style.configure("TLabel", background='#333', foreground='white')
style.configure("TEntry", fieldbackground='#555', foreground='white')
style.configure("TButton", background='#555', foreground='white')

frame = ttk.Frame(root, padding="10")
frame.pack(fill=BOTH, expand=True)

hwid_label = ttk.Label(frame, text="Enter your HWID:")
hwid_label.pack()
hwid_entry = ttk.Entry(frame)
hwid_entry.pack(fill=X, pady=10)

bypass_button = ttk.Button(frame, text="Start Bypass", command=start_request)
bypass_button.pack(pady=10)

result_area = scrolledtext.ScrolledText(frame, bg='#555', fg='white', height=10)
result_area.pack(fill=BOTH, expand=True)

root.mainloop()