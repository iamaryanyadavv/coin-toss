import socket
import json
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Random.random import getrandbits
from functools import reduce

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = '127.0.0.1'
PORT = 5545

serversocket.bind((IP,PORT))
serversocket.listen()

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

print('The server is up! Listening at: \n', PORT, IP)

def handle_new_client(clientsocket, address):
    global option1, option2, iv, introRes, instructionRes, rRes

    print('New connection made! Client address\n', address)

    intro = "Can't choose between two options?\nYou've come to the right place!\nI'll help you decide by simulating a coin toss\n"
    clientsocket.send(intro.encode()) #1 send
    introRes = clientsocket.recv(1024).decode() #2 receive

    if introRes!='Intro ok': #response check
        print('Something went wrong! Disconnecting\n')
        clientsocket.close()
    

    instruction = "Enter the two options you cannot decide between (Could be a movie, restaurant, anything)\n"
    clientsocket.send(instruction.encode()) #3 send
    instructionRes = clientsocket.recv(1024).decode() #4 receive

    if (instructionRes!='Instruction ok'): #response check
        print("Something went wrong! Disconnecting\n")
        clientsocket.close()

    #receiving option1
    option1 = clientsocket.recv(1024).decode() #5 receive
    option1 = json.loads(option1)
    print("Option1: ", option1)
    clientsocket.send('Option 1 Received'.encode()) #6 send

    #receiving option2
    option2 = clientsocket.recv(1024).decode() #7 receive
    option2 = json.loads(option2)
    print("Option2: ", option2)
    clientsocket.send('Option 2 Received'.encode()) #8 send

    #sending r to client
    r = get_random_bytes(48)
    # print('r: ', r)
    rRes = clientsocket.recv(1024).decode() #11 receive
    if(rRes=='send r'): #response check
        clientsocket.send(json.dumps(b64encode(r).decode('utf-8')).encode()) #12 send
    
    iv=b64decode(json.loads(clientsocket.recv(1024).decode())) #13 receive
    # print('iv: ', iv)

    c=b64decode(json.loads(clientsocket.recv(1024).decode())) #14 receive
    # print('c: ', c)
    clientsocket.send('c Received'.encode()) #14 send

    b0 = int(clientsocket.recv(1024).decode()) #15 receive
    clientsocket.send('b0 Received'.encode()) #15 send
    # print('b0 :', b0)

    s = b64decode(json.loads(clientsocket.recv(1024).decode())) #16 receive
    clientsocket.send('s Received'.encode()) #16 send
    # print('s: ',s)

    m=b"000000000000000000000000000000000000000000000000" #length = 48 bytes or 48*8 bits = 384bits
    cipher = AES.new(s, AES.MODE_OFB, iv=iv)
    Gs = cipher.encrypt(m)
    if(b0==0):
        c1 = Gs
    elif(b0==1):
        c1 = byte_xor(Gs,r)

    b1=getrandbits(1)
    clientsocket.recv(1024).decode() #17 receive
    if(c==c1):
        if(b1==0):
            clientsocket.send('0'.encode()) #17 send
        elif(b1==1):
            clientsocket.send('1'.encode()) #17 send
    elif(c!=c1):
        print('ABORT! Invalid commitment string!')
        clientsocket.send('2'.encode()) #17 send
        clientsocket.close()
    


    # if clientsocket.recv(1024).decode()=='End':
    #     print('User wants program to end!\n')
    #     clientsocket.close()
    clientsocket.close()
    return 0


while True:
    (clientsocket, address) = serversocket.accept()
    handle_new_client(clientsocket,address)
    clientsocket.close()