import Pyro5.api
import threading
import time
import random

import defs
import prot

ID = defs.P0
ARQUIVO = 'seg0.txt'
LIDER = False
SEED = 1235
#coisas que vai ter que saber
#N_PROCESSOS pra usar maioria e fors
# IP/AQUELE BAGUI LA DE ASSINATURA de cada um dos processos (isso vai pra um arq separado se pa)
# TIMER PROPRIO pra valida os hb

@Pyro5.api.expose
class processo:
	def __init__ (self, id, arquivo, termo, lider):
		self.id_atual = 0
		self.id = id
		self.arquivo = arquivo
		self.termo = termo
		self.lider = lider

		self.votos = 0
		self.buffer = bytearray(5)

		random.seed(SEED)
		self.timer = random.randint(150, 300)
		self.tempo_hb = time.time()

		self.link_dns = Pyro5.api.locate_ns()
		if (self.lider == False):
			uri_lid = self.link_dns.lookup(defs.NS_LIDER)
			self.proxy_lider = Pyro5.api.Proxy(uri_lid)

		self.lista_proxys = []
		for i in range(defs.N_PROC):
			self.lista_proxys.append(Pyro5.api.Proxy(defs.URI[i]))

	def constroi_pacote_hb(self):
		pacote = prot.inic_pacote()
		prot.escreve_tipo(pacote, prot.T_HB)
		prot.escreve_termo(pacote, self.termo)
		return pacote
	def constroi_pacote_pedido_voto(self):
		pacote = prot.inic_pacote()
		prot.escreve_tipo(pacote, prot.T_PV)
		prot.escreve_id_atual(pacote, self.id)
		prot.escreve_termo(pacote, self.termo)
		return pacote
	def constroi_pacote_msg(self, texto):
		pacote = prot.inic_pacote()
		prot.escreve_tipo(pacote, prot.T_MS)
		prot.escreve_id_atual(pacote, self.id_atual)
		prot.escreve_termo(pacote, self.termo)
		prot.escreve_texto(pacote, texto)
		return pacote

	def send_pacote(self, pacote, proxy):
		proxy.recebe_pacote(pacote)

	#chamada quando o processo ta normal , cliente mandou um char
	def add_info(self, texto):
		#adiciona o char passado no buffer não comitado
		self.buffer = texto
		self.id_atual  += 1
	#chamada pelo lider
	def commit(self):
		#atualiza o buffer real copiando o não commitado
		with open(self.arquivo, "w", encoding="utf-8") as f:
			f.write(self.buffer)
	#chamada quando  o timer proprio cair, e a eleição me colocar como lider? acho que n sei na real... tem que perguntar se pa
	def rollback(self):
		#atualiza o buffer temporario (não commitado) copiando o buffer real
		self.id_atual  -= 1

	def recebe_hb(self, pacote):
		self.tempo_hb = time.time()
		self.votos = 0
		return
	def recebe_msg(self, pacote):
		#msg padrao
		if (prot.le_commit(pacote) == 0):
			if (id_pc - self.id_atual == 1):
				self.add_info(prot.le_texto(pacote))
			
			self.proxy_lider.confirma_msg()

		#pediu pra commitar
		elif (prot.le_commit(pacote) == 1):
			id_pc = prot.le_id_atual(pacote)
			if(id_pc == self.id_atual):
				self.commit()
			elif (id_pc - self.id_atual == 1): 
				self.add_info(prot.le_texto(pacote))
				self.commit()
			#else: 
				#reporta erro
	def recebe_pvt(self, pacote):
		if (self.pesquisa_eleitoral(pacote)):
			prot.escreve_tipo(pacote, prot.T_VT)
			self.lista_proxys[prot.le_id_atual(pacote)].recebe_pacote(pacote)
	def recebe_vt(self):
		self.votos += 1
		if (self.votos > (defs.N_PROC - self.termo) // 2):
			self.votos = 0
			self.registra_como_lider()

	#thread de manutenção do hb
	def heart_beat(self):
		lid = self.lider
		while (lid == self.lider):
			#time.sleep(0.1) #s

			if (self.lider):
				pacote = self.constroi_pacote_hb()
				for s in self.lista_proxys:
					self.send_pacote(pacote, s)
			else:
				if(self.timer < (time.time() - self.tempo_hb)):
					self.inicia_eleicao()

	#chamada quando o timer do hb da pau
	def inicia_eleicao(self):
		pacote = self.constroi_pacote_pedido_voto()
		for s in self.lista_proxys:
			self.send_pacote(pacote, s)
	#chamada quando alguem pede seu voto
	def pesquisa_eleitoral(self, pacote):
		if (self.termo <= prot.le_termo(pacote)):
			return True
		else:
			self.inicia_eleicao()
			return False
	# chamada quando virar o novo lider
	def registra_como_lider(self):
		self.link_dns.register(defs.NS_LIDER, defs.URI[self.id])  #se coloca no DNS
		self.lider = True
		self.termo += 1

		thread = threading.Thread(target=self.heart_beat) # 1. Create the thread
		thread.start() # 2. Start the thread

	@Pyro5.api.expose
	def recebe_pacote(self, pacote):
		tipo = prot.le_tipo(pacote)
		# Heartbeat
		if (tipo == prot.T_HB):
			thread = threading.Thread(target=self.recebe_hb, args=(pacote)) # 1. Create the thread
			thread.start() # 2. Start the thread	
		
		# Mensagem
		elif (tipo == prot.T_MS):
			thread = threading.Thread(target=self.recebe_msg, args=(pacote)) # 1. Create the thread
			thread.start() # 2. Start the thread
		
		# Pedido de Voto
		elif (tipo == prot.T_PV):
			thread = threading.Thread(target=self.recebe_pvt, args=(pacote)) # 1. Create the thread
			thread.start() # 2. Start the thread

		# Recebe Voto
		elif (tipo == prot.T_VT):
			thread = threading.Thread(target=self.recebe_vt, args=(pacote)) # 1. Create the thread
			thread.start() # 2. Start the thread

		return

	#thread que vai ficar esperando os inputs do cliente
	def recebe_do_cliente(self, texto):

		pacote = self.constroi_pacote_msg(texto)
		for s in self.lista_proxys:
			self.send_pacote(pacote, s)

	@Pyro5.api.expose
	def confirma_msg(self, pacote):
		#n aceita pacotes atrasados
		if (prot.le_id_atual(pacote) == self.id_atual):
			self.votos += 1
			#se der maioria manda commitar (== pra n ficar remandando commit)
			if (self.votos == (defs.N_PROC - self.termo) // 2):
				prot.escreve_commit(pacote, 1)
				for s in self.lista_proxys:
					self.send_pacote(pacote, s)

	@Pyro5.api.expose
	def recebe_texto(self, texto):
		self.buffer = texto
		self.id_atual += 1

		thread = threading.Thread(target=self.recebe_do_cliente, args=(texto)) # 1. Create the thread
		thread.start() # 2. Start the thread

		return


	#baseado na flag muda a main que ta executando
	def main_seguidor(self):
		#cria 2 threads
		
		# uma fica conferindo heatbeat e timer e intenção de voto
		thread = threading.Thread(target=self.heart_beat) # 1. Create the thread
		thread.start() # 2. Start the thread

		# a outra fica recebendo info e commit
		daemon = Pyro5.api.Daemon(defs.PORTA[ID])             # make a Pyro daemon
		uri = daemon.register(processo, defs.NOMES[ID])

		print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
		daemon.requestLoop()

	def main_lider(self):
		#2 threads
		# uma fica mandando heartbeat e cuidando de timer
		self.registra_como_lider()

		# a outra vai ficar recebendo do cliente e encaminhando pros seguidores
		# a outra fica recebendo info e commit
		daemon = Pyro5.api.Daemon(defs.PORTA[ID])             # make a Pyro daemon
		uri = daemon.register(processo, defs.NOMES[ID])

		print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
		daemon.requestLoop()
		
def main():

	p = processo(ID, ARQUIVO, 0, LIDER)

	if (LIDER):
		p.main_lider()
	else:
		p.main_seguidor()

if __name__ == '__main__':
	main()