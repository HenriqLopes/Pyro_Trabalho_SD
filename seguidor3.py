import Pyro5.api
import threading
import time
import random

import defs
import prot

import processo

ID = defs.P3
ARQUIVO = 'seg3.txt'
LIDER = False
SEED = 2234

def main():

	p = processo.Processo(ID, ARQUIVO, 0, LIDER, SEED)

	if (LIDER):
		p.main_lider()
	else:
		p.main_seguidor()

if __name__ == '__main__':
	main()