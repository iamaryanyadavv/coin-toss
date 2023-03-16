# coin-toss
Simulating a coin toss using Bit Commitment and Coin Flipping Procotol.

This is a set of programs written to simulate a coin-toss.
Using bit commitment and coin flipping protocol, I was able to simulate a coin-toss
giving the guarantee of security by implementing AES(128) in OFB mode for encryption.

# Dependencies

pycryptodomex
base64
socket
json

# How to run

First clone the repository
Install all dependencies by running the commands
"pip3 install pycryptodomex"
"pip3 install base64"
in your terminal.

Then execute server.py using the command "python3 server.py"
(Our server is up and running)
Then execute client.py using the command "python3 client.py"

Now, input two options you cannot decide between, the output will give you a fair coin toss (verified by the server)
and, hence, a result as to which option you should choose.

---------------------------------------------------------------------------

Completed as part of my university course "Ashoka University CS-2362 Computer Security and Privacy" in spring semester 2023.
