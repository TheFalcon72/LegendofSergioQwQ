import socket
from _thread import *

import pygame.sprite

from level import YSortCamaraGroup
import pickle


class Server:
    def __init__(self):
        self.server = "192.168.0.13"
        self.port = 5555

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind()
        self.players = []
        self.find_players()

    def bind(self):
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        self.s.listen(2)
        print("Esperando Conexion, Servidor Iniciado")

    def find_players(self):
        self.players = [(64,64), (1152,1152)]

    def read_pos(self, str):
        str = str.split(",")
        return int(str[0]), int(str[1])

    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1])

    def threaded_client(self, conn, player):
        conn.send(str.encode(self.make_pos(self.players[player])))
        reply = ""
        while True:
            try:
                data = self.read_pos(conn.recv(2048).decode())
                self.players[player] = data

                if not data:
                    print("Disconnected")
                    break
                else:
                    if player == 1:
                        reply = self.players[0]
                    else:
                        reply = self.players[1]

                    print("Received: ", data)
                    print("Sending : ", reply)

                conn.sendall(str.encode(self.make_pos(reply)))
            except:
                break

        print("Lost connection")
        conn.close()


if __name__ == '__main__':
    server = Server()
    currentPlayer = 0
    while True:
        conn, addr = server.s.accept()
        print("Connected to:", addr)

        start_new_thread(server.threaded_client, (conn, currentPlayer))
        currentPlayer += 1