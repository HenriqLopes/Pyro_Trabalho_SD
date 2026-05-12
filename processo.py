import Pyro5.api
import threading
import time
import random

import defs
import prot

class Processo:
	def __init__ (self, id, arquivo, termo, lider, seed):
		self.id_atual = 0
		self.id = id
		self.arquivo = arquivo
		self.termo = termo
		self.lider = lider

		self.votos = 0
		self.buffer = bytearray(5)

		self.candidato = False

		random.seed(seed)
		self.timer = random.randint(150, 300) / 10
		self.tempo_hb = time.time()

		link_dns = Pyro5.api.locate_ns()
		if (self.lider == False):
			self.uri_lid = link_dns.lookup(defs.NS_LIDER)


		self.lista_URIS = []
		for i in range(defs.N_PROC):
			self.lista_URIS.append(defs.URI[i])
			

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

	def send_pacote(self, pacote, uri):

		if uri not in self.lista_URIS:
			return
		
		try:
			proxy = Pyro5.api.Proxy(uri)

			tipo = prot.le_tipo(pacote)
			# Heartbeat
			if (tipo == prot.T_HB):
				proxy.recebe_hb(pacote)

			# Mensagem
			elif (tipo == prot.T_MS):
				proxy.recebe_msg(pacote)

			# Pedido de Voto
			elif (tipo == prot.T_PV):
				proxy.recebe_pvt(pacote)
				
			# Recebe Voto
			elif (tipo == prot.T_VT):
				proxy.recebe_vt()

		except Pyro5.errors.CommunicationError:
			print(f"Processo {uri} caiu")
			# remove da lista de seguidores
			if uri in self.lista_URIS:
				self.lista_URIS.remove(uri)

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

	@Pyro5.api.expose
	def recebe_hb(self, pacote):

		term_lid = prot.le_termo(pacote)
		# if tem um novo xerife na cidade
		if (term_lid > self.termo):
			link_dns = Pyro5.api.locate_ns()
			self.uri_lid = link_dns.lookup(defs.NS_LIDER)
			self.termo = term_lid
			self.candidato = False

		self.tempo_hb = time.time()
		self.votos = 0
		return
	@Pyro5.api.expose
	def recebe_msg(self, pacote):
		#msg padrao
		prot.print_pacote(pacote)
		id_pc = prot.le_id_atual(pacote)

		if (prot.le_commit(pacote) == 0):
			if (id_pc - self.id_atual == 1):
				self.add_info(prot.le_texto(pacote))
			
			print(self.uri_lid)
			proxy = Pyro5.api.Proxy(self.uri_lid)
			proxy.confirma_msg()

		#pediu pra commitar
		elif (prot.le_commit(pacote) == 1):
			if(id_pc == self.id_atual):
				self.commit()
			elif (id_pc - self.id_atual == 1): 
				self.add_info(prot.le_texto(pacote))
				self.commit()
			#else: 
				#reporta erro				
	@Pyro5.api.expose
	def recebe_pvt(self, pacote):
		if (self.pesquisa_eleitoral(pacote)):
			self.tempo_hb = time.time() # tem um caba bom pra mim se elegendo, ent vo me aquietar um tempinho
			prot.escreve_tipo(pacote, prot.T_VT)
			self.send_pacote(pacote, self.lista_URIS[prot.le_id_atual(pacote)])
	@Pyro5.api.expose
	def recebe_vt(self):
		self.votos += 1
		if (self.votos >= (defs.N_PROC) // 2):
			self.votos = 0
			self.registra_como_lider()

	#thread de manutenção do hb
	def heart_beat(self):
		lid = self.lider
		self.candidato = False
		while (lid == self.lider):
			#time.sleep(0.1) #s

			if (self.lider):
				pacote = self.constroi_pacote_hb()
				for uri in self.lista_URIS:
					if (uri != defs.URI[self.id]):
						self.send_pacote(pacote, uri)
						
			else:
				#print(f"{(time.time() - self.tempo_hb)}ms de {self.timer}ms")
				if(self.timer < (time.time() - self.tempo_hb)) and (not(self.candidato)):
					self.candidato = True
					self.inicia_eleicao()

	#chamada quando o timer do hb da pau
	def inicia_eleicao(self):
		pacote = self.constroi_pacote_pedido_voto()
		self.votos = 1
		for uri in self.lista_URIS:
			if (uri != defs.URI[self.id]):
				thread = threading.Thread(target=self.send_pacote, args=(pacote, uri)) # 1. Create the thread
				thread.start() # 2. Start the thread	
	#chamada quando alguem pede seu voto
	def pesquisa_eleitoral(self, pacote):
		if (self.termo <= prot.le_termo(pacote)):
			return True
		#else:
			#self.inicia_eleicao()
		return False
	# chamada quando virar o novo lider
	def registra_como_lider(self):
		link_dns = Pyro5.api.locate_ns()
		link_dns.register(defs.NS_LIDER, defs.URI[self.id])  #se coloca no DNS
		self.lider = True
		self.termo += 1

		time.sleep(10)

		thread = threading.Thread(target=self.heart_beat) # 1. Create the thread
		thread.start() # 2. Start the thread

	#TODO DESFAZER ESSA FEIURA TODA AQUI, PARA DE SOCAR THREAD ATÈ O CARALHO
	#@Pyro5.api.oneway
	@Pyro5.api.expose
	def recebe_pacote(self, pacote):
		tipo = prot.le_tipo(pacote)
		# Heartbeat
		if (tipo == prot.T_HB):
			#print("recebeu HB \n")
			thread = threading.Thread(target=self.recebe_hb, args=(pacote, )) # 1. Create the thread
			thread.start() # 2. Start the thread	
		
		# Mensagem
		elif (tipo == prot.T_MS):
			print("recebeu MSG \n")
			thread = threading.Thread(target=self.recebe_msg, args=(pacote, )) # 1. Create the thread
			thread.start() # 2. Start the thread
		
		# Pedido de Voto
		elif (tipo == prot.T_PV):
			print("recebeu PVT \n")
			thread = threading.Thread(target=self.recebe_pvt, args=(pacote, )) # 1. Create the thread
			thread.start() # 2. Start the thread

		# Recebe Voto
		elif (tipo == prot.T_VT):
			print("recebeu VT \n")
			thread = threading.Thread(target=self.recebe_vt) # 1. Create the thread
			thread.start() # 2. Start the thread

		return

	#thread que vai ficar esperando os inputs do cliente
	def recebe_do_cliente(self, texto):

		pacote = self.constroi_pacote_msg(texto)
		for uri in self.lista_URIS:
			if (uri != defs.URI[self.id]):
				thread = threading.Thread(target=self.send_pacote, args=(pacote, uri)) # 1. Create the thread
				thread.start() # 2. Start the thread	

	@Pyro5.api.expose
	def confirma_msg(self, pacote):

		print("chegou aqui porra")

		#n aceita pacotes atrasados
		if (prot.le_id_atual(pacote) == self.id_atual):
			self.votos += 1
			#se der maioria manda commitar (== pra n ficar remandando commit)
			if (self.votos == (defs.N_PROC) // 2):
				prot.escreve_commit(pacote, 1)
				for uri in self.lista_URIS:
					if (uri != defs.URI[self.id]):
						thread = threading.Thread(target=self.send_pacote, args=(pacote, uri)) # 1. Create the thread
						thread.start() # 2. Start the thread	
						
	@Pyro5.api.expose
	def recebe_texto(self, texto):
		self.buffer = texto
		self.id_atual += 1

		thread = threading.Thread(target=self.recebe_do_cliente, args=(texto, )) # 1. Create the thread
		thread.start() # 2. Start the thread

		return

	#baseado na flag muda a main que ta executando
	def main_seguidor(self):
		#cria 2 threads
		
		# uma fica conferindo heatbeat e timer e intenção de voto
		thread = threading.Thread(target=self.heart_beat) # 1. Create the thread
		thread.start() # 2. Start the thread

		# a outra fica recebendo info e commit
		daemon = Pyro5.api.Daemon(host="localhost", port=defs.PORTA[self.id])             # make a Pyro daemon
		uri = daemon.register(self, defs.NOMES[self.id])

		print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
		daemon.requestLoop()

	def main_lider(self):
		#2 threads
		# uma fica mandando heartbeat e cuidando de timer
		self.registra_como_lider()

		# a outra vai ficar recebendo do cliente e encaminhando pros seguidores
		# a outra fica recebendo info e commit
		daemon = Pyro5.api.Daemon(host="localhost", port=defs.PORTA[self.id])             # make a Pyro daemon
		uri = daemon.register(self, defs.NOMES[self.id])

		print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
		daemon.requestLoop()
	