# https://stackoverflow.com/questions/10965336/python-error-no-module-named-pylab
# sudo apt-get install python-numpy python-scipy python-matplotlib
# import libraries
import hashlib
import random
import string
import json
import binascii
import logging
import datetime
import collections
# import numpy as np
# import pandas as pd
# import pylab as pl

# https://stackoverflow.com/questions/19623267/importerror-no-module-named-crypto-cipher
# pip install pycryptodome
# following imports are required by PKI
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


# https://www.tutorialspoint.com/python_blockchain/python_blockchain_transaction_class.htm
class Client:

    def __init__(self):
        random = Crypto.Random.new().read

        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')


class Transaction:

    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()

    def sign_transaction(self):
        # private_key = self.sender._private_key
        # signer = PKCS1_v1_5.new(private_key)
        # h = SHA.new(str(self.to_dict()).encode('utf8'))
        # return binascii.hexlify(signer.sign(h)).decode('ascii')

        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        asdf1 = str(self.to_dict()).encode('utf-8')
        hash1 = SHA.new(asdf1)
        output1 = signer.sign(hash1)

        # convert to hex
        asdf2 = binascii.hexlify(output1)
        ascii_output = asdf2.decode('ascii')

        return ascii_output

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time': self.time})


class Block:
    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""


transactions = [] # 'queue'
last_transaction_index = 0
last_block_hash = "" # value of the 'last block'
TPCoins = [] # is this the 'chained block' ?


def display_transaction(transaction):

    # for transaction in transactions:
    dict = transaction.to_dict()

    print("sender: " + dict['sender'])
    print('-----')
    print("recipient: " + dict['recipient'])
    print('-----')
    print("value: " + str(dict['value']))
    print('-----')
    print("time: " + str(dict['time']))
    print('-----')


'''
    Helper Functions
'''

# printing all the 'blocks' and 'transactions' INSIDE the 'block'
def dump_blockchain(input1):

    print("Number of blocks in the chain: " + str(len(input1)))

    network_length = len(TPCoins)
    for x in range(network_length):
        block_temp = TPCoins[x]

        print("block # " + str(x))

        for transaction in block_temp.verified_transactions:
            display_transaction(transaction)

        print('--------------')
        print('=====================================')

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def sha256(message):
    asdf1 = message.encode('ascii')

    # converting 'sha256' object to 'string'
    return hashlib.sha256(asdf1).hexdigest()

def mine(message, difficulty=1):
    assert difficulty >= 1
    prefix = '1' * difficulty # prefix >> '111'

    for i in range(1000): # mod 1000
        asdf1 = hash(message)
        asdf2 = str(asdf1)
        asdf3 = str(asdf1) + str(i)
        digest = sha256(asdf3)

        if digest.startswith(prefix):
            print ("after " + str(i) + " iterations found nonce: "+ digest)
            return digest


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    Dinesh = Client()
    Ramesh = Client()
    Seema = Client()
    Vijay = Client()
    # print(Dinesh.identity)

    t1 = Transaction(
        Dinesh,
        Ramesh.identity,
        15.0
    )

    sign1 = t1.sign_transaction();
    transactions.append(t1)

    t2 = Transaction(
        Dinesh,
        Seema.identity,
        6.0
    )
    t2.sign_transaction()
    transactions.append(t2)
    t3 = Transaction(
        Ramesh,
        Vijay.identity,
        2.0
    )
    t3.sign_transaction()
    transactions.append(t3)
    t4 = Transaction(
        Seema,
        Ramesh.identity,
        4.0
    )
    t4.sign_transaction()
    transactions.append(t4)
    t5 = Transaction(
        Vijay,
        Seema.identity,
        7.0
    )
    t5.sign_transaction()
    transactions.append(t5)
    t6 = Transaction(
        Ramesh,
        Seema.identity,
        3.0
    )
    t6.sign_transaction()
    transactions.append(t6)
    t7 = Transaction(
        Seema,
        Dinesh.identity,
        8.0
    )
    t7.sign_transaction()
    transactions.append(t7)
    t8 = Transaction(
        Seema,
        Ramesh.identity,
        1.0
    )
    t8.sign_transaction()
    transactions.append(t8)
    t9 = Transaction(
        Vijay,
        Dinesh.identity,
        5.0
    )
    t9.sign_transaction()
    transactions.append(t9)
    t10 = Transaction(
        Vijay,
        Ramesh.identity,
        3.0
    )
    t10.sign_transaction()
    transactions.append(t10)

    ## print all 'transactions' in the list
    # for tran in transactions:
    #     display_transaction(tran)


    # making the 'genesis block', the FIRST block
    Dinesh = Client()

    t0 = Transaction(
        "Genesis",
        Dinesh.identity,
        500.0
    )

    block0 = Block()
    block0.previous_block_hash = None
    block0.Nonce = None
    block0.verified_transactions.append(t0)

    # now, 'hashing' the 'block' (the 'block' with 'transactions' inside)
    block0_hash = hash(block0)
    last_block_hash = block0_hash

    TPCoins.append(block0) # add 'block0' to 'TPcoin network'
    dump_blockchain(TPCoins) # print info

    # making a new 'block'
    # Miner 1 adds a block
    block = Block()

    for i in range(3): # mod 3, grab '3 transactions'
        temp_transaction1 = transactions[last_transaction_index]
        # validate transaction
        # if valid
        block.verified_transactions.append(temp_transaction1) # add 1 transaction to the 'current block'
        last_transaction_index += 1 # increment by 1


    block.previous_block_hash = last_block_hash # add the 'hash value' of the 'block before this block'
    the_nounce = mine(block, 2) # 'brute force' to find the value of the 'nounce
    block.Nonce = the_nounce # add the 'answer' to the 'current block'
    digest1 = hash(block) # make a 'hash value' for the 'current block'
    TPCoins.append(block) # add the 'current block' to the 'TPcoin network'
    last_block_hash = digest1 # give the 'hash value' for the 'current block' to another variable


    # Miner 2 adds a block
    block = Block()

    # grab 3 'transactions'
    for i in range(3): # mod 3
        temp_transaction1 = transactions[last_transaction_index]
        # validate transcation
        # if valid
        block.verified_transactions.append(temp_transaction1)
        last_transaction_index += 1 # increase the 'index' by 1

    block.previous_block_hash = last_block_hash
    the_nounce = mine(block, 2)
    block.Nonce = the_nounce
    digest1 = hash(block)
    # why not add the 'current block hash' to the 'block object'

    # adding the 'current block' to 'TPcoin network'
    TPCoins.append(block)
    last_block_hash = digest1

    print('\n')
    print('f'*30)
    print('final output')
    print('f' * 30)
    print('\n')

    dump_blockchain(TPCoins)

    print('debug wait')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
