import socket
import json
import time
from base64 import b64decode, b64encode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Random.random import getrandbits
from bitstring import BitStream, BitArray

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = '127.0.0.1'
PORT = 5545

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

# def bits2string(b):
#     return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)]*8))

clientsocket.connect((IP,PORT))

print(clientsocket.recv(1024).decode()) #1 receive
clientsocket.send('Intro ok'.encode()) #2 send

print(clientsocket.recv(1024).decode()) #3 receive
clientsocket.send('Instruction ok'.encode()) #4 send

continue_choice = 'y'
while (continue_choice=='y' or continue_choice=='Y'):

    o1 = input("1: ")
    option1 = json.dumps(o1)
    clientsocket.send(option1.encode()) #5 send
    clientsocket.recv(1024).decode() #6 receive

    o2 = input("2: ")
    option2 = json.dumps(o2)
    clientsocket.send(option2.encode()) #7 send
    clientsocket.recv(1024).decode() #8 receive

    b0=getrandbits(1)

    s = get_random_bytes(16)
    # print('s: ', s)
    # print('s length: ', len(s))
    m=b"000000000000000000000000000000000000000000000000" #length = 48 bytes or 48*8 bits = 384bits
    # print("m: ", m)
    # print('m: ', len(m))

    #receiving r from server
    clientsocket.send('send r'.encode()) #11 send
    r = b64decode(json.loads(clientsocket.recv(1024).decode())) #12 receive
    # print('r: ', r)
    # print('r length:', len(r))
    
    cipher=AES.new(s, AES.MODE_OFB)

    #sending iv
    clientsocket.send(json.dumps(b64encode(cipher.iv).decode('utf-8')).encode()) #13 send

    Gs=cipher.encrypt(m)
    # print('Gs: ', Gs)
    # print('Gs length:', len(Gs))
    
    if(b0==0):
        c=Gs
        # print('c: ', c)
        clientsocket.send(json.dumps(b64encode(c).decode('utf-8')).encode()) #14 send
        clientsocket.recv(1024).decode() #14 receive
        clientsocket.send('0'.encode()) #15 send
    elif(b0==1):
        c=byte_xor(Gs,r)
        # print('c: ', c)
        clientsocket.send(json.dumps(b64encode(c).decode('utf-8')).encode()) #14 send
        clientsocket.recv(1024).decode() #14 receive
        clientsocket.send('1'.encode()) #15 send
    
    clientsocket.recv(1024).decode() #15 receive

    #send s to server
    clientsocket.send(json.dumps(b64encode(s).decode('utf-8')).encode()) # 16 send
    clientsocket.recv(1024).decode() #16 receive

    clientsocket.send('Validate'.encode()) #17 send
    b1 = int(clientsocket.recv(1024).decode()) #17 receive
    print("Flipping...\n")
    time.sleep(2)
    if(b1==0 or b1==1):
        b = b0^b1
        if(b==0):
            print('You should choose: ', option1)
        elif(b==1):
            print('You should choose: ', option2)

    elif(b1==2):
        print('ERROR! Exiting!')
        clientsocket.close()
    

    print('\nRun it again for another toss.')
    continue_choice = 'n'
    # if continue_choice == 'n' or continue_choice == 'N':
    #     clientsocket.send('End'.encode())

