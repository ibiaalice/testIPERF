import socket
import time
from threading import Thread
from queue import Queue
import sys

class Cliente(object):

    def __init__(self, ip, porta, verbose):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.destino = (ip, porta)
        self.verbose = verbose

    def start(self):
        """envia a solicitacao 2 segundos depois"""
        operacao = input()

        self.operacao = operacao

        while True:
            respostas = Queue()

            criaConexao = Thread(target=self.conecta, args=(respostas, ))
            criaConexao.start()
            criaConexao.join(timeout=2)

            if respostas.qsize() > 0:
                break


    def conecta(self, salvarResposta):
        
        confirmacoes = Queue()

        # If after 0.1s client doesnt receive a ack resposta (confirmacoes is empty)
        # se we assume as lost and resend the request
        while True:
            if self.verbose:
                print('enviando requisicao')

            self.socket.sendto(self.operacao.encode('utf-8'), self.destino)

            threadPrincipal = Thread(target=self.recv_ack, args=(confirmacoes,))
            threadPrincipal.start()
            threadPrincipal.join(timeout=0.1) # botao do timeout
           


            if confirmacoes.qsize() > 0 and confirmacoes.get()[0].decode('utf-8') == 'ACK':
                if self.verbose:
                    print('recebendo ack')
                break
        
        resposta = self.socket.recvfrom(1024)
 
        if resposta[0].decode('utf-8') != 'ACK':
            if self.verbose:
                print('recebendo resposta')
            print("{}\n".format(resposta[0].decode('utf-8')))
            salvarResposta.put(resposta)        

    def recv_ack(self, mensagem):
        if self.verbose:
            print('esperando o ack')
        resposta = self.socket.recvfrom(1024)
        mensagem.put(resposta)

if __name__ == '__main__':

    verbose = False

    if "--verbose" in sys.argv:
        verbose = True

    SERVER_IP = "localhost"
    SERVER_PORTA = 13000

    Cliente(SERVER_IP, SERVER_PORTA, verbose).start()