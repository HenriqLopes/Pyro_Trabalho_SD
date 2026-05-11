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
	P0 : 'Proc1',
	P1 : 'Proc2',
	P2 : 'Proc3',
	P3 : 'Proc4',
	LI : 'lider_ini'
}

PORTA = {
	P0 : '45800',
	P1 : '45801',
	P2 : '45802',
	P3 : '45803',
	LI : '45804'
}

URI = {
	P0 : 'PYRO:proc0@localhost:45800',
	P1 : 'PYRO:proc1@localhost:45801',
	P2 : 'PYRO:proc2@localhost:45802',
	P3 : 'PYRO:proc3@localhost:45803',
	LI : 'PYRO:lider_ini@localhost:45804'
}




