import socket

from threading import Thread
from queue import Queue


class UDPServer():

    def __init__(self, ip, porta):
        self.ip = ip
        self.porta = porta
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
        self.resposta = "Inválido"


    def wait_for_client_ack(self, acks):
        print('esperando...')
        msg = self.socket.recvfrom(1024)
        acks.put(msg)

    def request(self, opc, c):

        self.socket.sendto( 'ACK'.encode('utf-8'), c )
        array =  opc.decode('utf-8').split()

        if array[0] != 'ACK':
             
            try:
                opc = array[0]
                x = int( array[1] )
                y = int( array[2] )

                if opc == 'ADD':
                    self.resposta = str(x + y)

                elif opc == 'SUB':
                    self.resposta = str(x - y)

                elif opc == 'MULT':
                    self.resposta = str(x * y)

                elif opc == 'EXP':
                    self.resposta = str(x ** y)

                elif opc == 'DIV ' and y != 0:
                    self.resposta = str(x / y)

            except:
                self.resposta = 'inválida'

            self.socket.sendto(self.resposta.encode('utf-8'), c)
        else:
            print('ACK recebido...')


    def exec(self):
        self.socket.bind((self.ip, self.porta))
        print("Servidor UDP rodando...")

        while True:
            opc, c = self.socket.recvfrom(1024)

            print('recebendo ... {}: {}'.format(c, opc))

            Thread(target=self.request,
                   args=(opc, c, )).start()





if __name__ == "__main__":

    UDPServer('localhost', 5000).exec()
