'''daemon = Pyro5.api.Daemon(porta)             # make a Pyro daemon
uri = daemon.register(processo, nome)   
'''

NS_LIDER = 'lider'

N_PROC = 4

P0 = 0
P1 = 1
P2 = 2
P3 = 3
LI = 4

NOMES = {
	P0 : 'proc0',
	P1 : 'proc1',
	P2 : 'proc2',
	P3 : 'proc3',
	LI : 'lider_ini'
}

PORTA = {
	P0 : 57350,
	P1 : 57351,
	P2 : 57352,
	P3 : 57353,
	LI : 57354
}

URI = {
	P0 : 'PYRO:proc0@localhost:57350',
	P1 : 'PYRO:proc1@localhost:57351',
	P2 : 'PYRO:proc2@localhost:57352',
	P3 : 'PYRO:proc3@localhost:57353',
	LI : 'PYRO:lider_ini@localhost:57354'
}




