import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class IRCClient:
    def __init__(self, server, port, nickname, channel):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.channel = channel
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.connect((self.server, self.port))
        self.client.send(f"NICK {self.nickname}\r\n".encode('utf-8'))
        self.client.send(f"USER {self.nickname} 0 * :{self.nickname}\r\n".encode('utf-8'))
        self.client.send(f"JOIN {self.channel}\r\n".encode('utf-8'))

    def receive_messages(self, display_message_callback):
        while True:
            message = self.client.recv(2048).decode('utf-8')
            if message.startswith('PING'):
                self.client.send("PONG :pingis\n".encode('utf-8'))
            else:
                display_message_callback(message)

class IRCClientGUI:
    def __init__(self, root, irc_client):
        self.root = root
        self.root.title("IRC Client")
        self.irc_client = irc_client

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        self.entry_field = tk.Entry(self.root)
        self.entry_field.pack(padx=10, pady=10, fill=tk.X)
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        self.receive_thread = threading.Thread(target=self.irc_client.receive_messages, args=(self.display_message,))
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def send_message(self, event=None):
        message = self.entry_field.get()
        if message:
            self.irc_client.client.send(f"PRIVMSG {self.irc_client.channel} :{message}\r\n".encode('utf-8'))
            self.display_message(f"You: {message}")
            self.entry_field.delete(0, tk.END)

    def display_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    server = "irc.libera.chat"
    port = 6667
    nickname = "isnejd"
    channel = "#termux"

    irc_client = IRCClient(server, port, nickname, channel)
    irc_client.connect()

    root = tk.Tk()
    gui = IRCClientGUI(root, irc_client)
    root.mainloop()
