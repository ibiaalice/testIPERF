import socket
from threading import Thread
from queue import Queue


class UDPClient():

    def __init__(self, ip, porta):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = (ip, porta)

    def request(self, responses):
        acks = Queue()

        while (True):
            self.socket.sendto(self.entrada.encode('utf-8'), self.dest)

            waiting_thread = Thread(
                target=self.espera_ack, args=(acks, ))
            waiting_thread.start()
            waiting_thread.join(timeout=0.1)

            if acks.qsize() > 0 and acks.get()[0].decode('utf-8') == 'ACK':
                print('ACK recebido')
                break

        response = self.socket.recvfrom(1024)

        if response[0].decode('utf-8') != 'ACK':
            self.socket.sendto('ACK'.encode('utf-8'), self.dest)

            print(response[0].decode('utf-8'))
            responses.put(response)

    def executar(self):
        entrada = input('Operacao: ')

        self.entrada = entrada

        while True:
            responses = Queue()

            main_thread = Thread(target=self.request, args=(responses,))
            main_thread.start()
            main_thread.join(timeout=2)
            main_thread._stop()

            if responses.qsize() > 0:
                break





    def espera_ack(self, acks):
        print('Esperando ACK')
        msg = self.socket.recvfrom(1024)
        acks.put(msg)


if __name__ == '__main__':

    UDPClient("localhost", 5000).executar()
