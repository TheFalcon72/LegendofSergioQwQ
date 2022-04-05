import socket
from _thread import *

import pygame.sprite

from level import YSortCamaraGroup
from player import Player
from settings import *
from tile import Tile
import pickle


class Server:
    def _init_(self):
        self.visible_sprite = YSortCamaraGroup
        self.obstacles_sprite = pygame.sprite.Group()
        self.server = "192.168.0.13"
        self.port = 5555

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []
        self.bind()
        self.find_players()
    def bind(self):
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        self.s.listen(2)
        print("Esperando Conexion, Servidor Iniciado")

    def find_players(self):
        self.players = ["64,64", "1152,1152"]

    def threaded_client(self, conn, player):
        conn.send(pickle.dumps(self.players[player]))
        reply = ""
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
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

                conn.sendall(pickle.dumps(reply))
            except:
                break

        print("Lost connection")
        conn.close()


if _name_ == '_main_':
    server = Server()
    currentPlayer = 0
    while True:
        conn, addr = server.s.accept()
        print("Connected to:", addr)

        start_new_thread(server.threaded_client, (conn, currentPlayer))
        currentPlayer += 1