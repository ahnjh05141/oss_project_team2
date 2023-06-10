from tkinter import *
import os
import sys
import ctypes
import pathlib
import shutil
import gitRepository

# clone public repository
def clone_public(local, address):
    os.system(f"git clone {address} {local}")

# clone private repository
def clone_private(local, address, id):
    new_address = "https://" + id + "@" + address[8:]
    os.system(f"git clone {new_address} {local}")

# store id, token
def store(path, id, token):
    f = open(path + "/store.txt", 'w')
    f.write(id)
    f.write(token)
    f.close