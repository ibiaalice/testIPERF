import socket
import time
from threading import Thread, enumerate

class Servidor(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))

    def listen(self): 
        print ("servidor rodando...")

        while True:
            mensagem, cliente = self.socket.recvfrom(1024)
            print("conexao recebida do cliente: ", cliente)
            
            Thread(target=self.criaConexao, args=(mensagem, cliente)).start()
        
    def criaConexao(self, mensagem, cliente):

        # Para testar se o reenvio do ack está funcionando
        time.sleep(2)

        self.socket.sendto('ACK'.encode('utf-8'), cliente)

        # Para testar se o reenvio geral esta funcionando
        time.sleep(4)

        print('recebendo req do ip {} na porta {}'.format(cliente[0], cliente[1]))
        elements = mensagem.decode('utf-8').split()

        try:
            resposta = calcula(elements[0], int(elements[1]), int(elements[2]))
            if resposta == None:
                resposta = "Resposta invalida"
            
            print('resultado de {} = {}'.format(elements, resposta))
        except:
            resposta = 'algo deu errado'
        
        self.socket.sendto(str(resposta).encode('utf-8'), cliente)

def calcula(op, x, y):
    ans = None
    op = op.upper() 

    if op == 'ADD':
        ans = x + y
    elif op == 'SUB':
        result = x - y
    elif op == 'MULT':
        result = x * y
    elif op == 'EXP':
        result = x ** y
    elif op == 'DIV ' and y != 0:
        result = x / y

    return ans

if __name__ == "__main__":

    UDP_IP = 'localhost'
    UDP_PORT = 13000

    Servidor(UDP_IP, UDP_PORT).listen()