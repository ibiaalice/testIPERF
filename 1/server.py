import random
import socket

def output_message (a, b, operator, r):
    message = ""
    if a == int(a): message += "%d " % (a)
    else: message += "%.2f " % (a)
    message += operator
    if b == int(b): message += "%d = " % (b)
    else: message += "%.2f = " % (b)
    if r == int(r): message += "%d" % (r)
    else: message += "%.2f" % (r)

    return message


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))

while True:
    message, address = server_socket.recvfrom(1024)
    request = message.decode('utf-8').split()
    operator = request[0].upper()
    a = float(request[1])
    b = float(request[2])

    if (operator == "ADD"):
        result = a + b
        op = "+ "
        output = output_message(a,b,op,result)
        out = output.encode('utf-8')
    elif (operator == "SUB"):
        result = a - b
        op = "- "
        output = output_message(a,b,op,result)
        out = output.encode('utf-8')
    elif (operator == "MULT"):
        result = a * b
        op = "x "
        output = output_message(a,b,op,result)
        out = output.encode('utf-8')
    elif (operator == "DIV"):
        result = a / b
        op = "/ "
        output = output_message(a,b,op,result)
        out = output.encode('utf-8')
    elif (operator == "EXP"):
        result = a ** b
        op = "^ "
        output = output_message(a,b,op,result)
        out = output.encode('utf-8')
    else:
        output = "Invalid operation"
        out = output.encode('utf-8')
    
    
    server_socket.sendto(out, address)