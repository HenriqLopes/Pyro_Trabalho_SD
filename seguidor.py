import Pyro5.api
import threading
import time

import defs
import prot

#coisas que vai ter que saber
#N_PROCESSOS pra usar maioria e fors
# IP/AQUELE BAGUI LA DE ASSINATURA de cada um dos processos (isso vai pra um arq separado se pa)
# TIMER PROPRIO pra valida os hb

@Pyro5.api.expose
class processo:
	def __init__ (self, id, buffer, arquivo, termo, lider, timer, tempo_hb):
		self.buffer = buffer
		self.id_atual = 0
		self.id = id
		self.arquivo = arquivo
		self.termo = termo
		self.lider = lider
		self.timer = timer #rand()
		self.tempo_hb = tempo_hb

		self.link_dns = Pyro5.api.locate_ns()

		for i in range(defs.N_PROC):
			self.lista_proxys.append(Pyro5.api.Proxy(defs.uri[i]))

	def constroi_pacote_hb(self):
		pacote = prot.inic_pacote()
		prot.escreve_tipo(pacote, prot.T_HB)
		prot.escreve_termo(self.termo)
		return pacote
	
	def constroi_pacote_pedido_voto(self):
		pacote = prot.inic_pacote()
		prot.escreve_tipo(pacote, prot.T_PV)
		prot.escreve_id_atual(pacote, self.id)
		prot.escreve_termo(self.termo)
		return

	def send_pacote(self, pacote, proxy_destino):
		???
		return

	def recebe_hb(self,):

		return
	
	'''thread = threading.Thread(target=recebe_pacote()) # 1. Create the thread

	thread.start() # 2. Start the thread

	print("Main thread is doing other work...") # 3. Main thread continues working concurrently

	thread.join() # 4. Wait for the thread to finish
	print("Thread has finished!")
	'''
	#thread de manutenção do hb
	def heart_beat(self):
		if (self.lider):
			pacote = self.constroi_pacote_hb()
			for s in self.lista_proxys:
				self.send_pacote(pacote, s)
		else:
			if(self.timer < (time() - self.tempo_hb)):
				self.inicia_eleicao()
			#espera o hb e cuida do timer
	# }

	#chamada quando o timer do hb da pau
	def inicia_eleicao(self):
		pacote = self.constroi_pacote_pedido_voto()
		for s in self.lista_proxys:
			self.send_pacote(pacote, s)
		
		### tem que fazer isso aqui numa thread de recebimento
		#fica contabilizando até dar maioria

		#quando somar maioria, muda sua flag pra lider
		#atualiza o lider no DNS
		# avisa todo mundo pra atualizarem seus termos

	#chamada quando alguem pede seu voto
	def pesquisa_eleitoral(self, pacote):
		if (self.termo <= prot.le_termo(pacote)):
			return True
		else:
			self.inicia_eleicao()
			return False
	
	# chamada quando virar o novo lider
	def registra_como_lider(self):
		self.link_dns.register("lider", defs.uri[self.id])  #se coloca no DNS
		self.lider = True
		self.termo += 1
		self.heart_beat() #avisa todo mundo pra atualizar o termo


#ARRUMAR
	@Pyro5.api.expose
	def recebe_pacote(self, pacote):
		tipo = prot.le_tipo(pacote)
		# Heartbeat
		if (tipo == prot.T_HB):
			self.tempo_hb = time()
			self.votos = 0
		
		# Mensagem
		elif (tipo == prot.T_MS):
			if (prot.le_commit(pacote) == 0):
				if (id_pc - self.id_atual == 1):
					add_info(prot.le_texto(pacote))

			elif (prot.le_commit(pacote) == 1):
				id_pc = prot.le_id_atual(pacote)
				if(id_pc == self.id_atual):
					commit()
				elif (id_pc - self.id_atual == 1): 
					add_info(prot.le_texto(pacote))
					commit()
				#else: 
					#reporta erro
		
		# Pedido de Voto
		elif (tipo == prot.T_PV):
			if (self.pesquisa_eleitoral(pacote)):
				prot.escreve_tipo(pacote, prot.T_VT)
				self.lista_proxys[prot.le_id_atual(pacote)].recebe_pacote(pacote)

		# Recebe Voto
		elif (tipo == prot.T_VT):
			self.votos += 1
			if (self.votos > (defs.N_PROC - self.termo) // 2):
				self.registra_como_lider()


		return


daemon = Pyro5.api.Daemon()             # make a Pyro daemon
uri = daemon.register(processo, "processo1")

print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
daemon.requestLoop()   

#chamada quando o processo ta normal , cliente mandou um char
def add_info():
	#adiciona o char passado no buffer não comitado

#chamada pelo lider
def commit():
	#atualiza o buffer real copiando o não commitado

#chamada quando  o timer proprio cair, e a eleição me colocar como lider? acho que n sei na real... tem que perguntar se pa
def rollback():
	#atualiza o buffer temporario (não commitado) copiando o buffer real

#thread que vai ficar esperando os inputs do cliente
def recebe_do_cliente():
	#recebe um char de cada vez
	#manda para todos os seguidores
	#aguarda maioria confirmar
	#manda commitar

#baseado na flag muda a main que ta executando
def main_seguidor():
	#cria 2 threads
		# uma fica conferindo heatbeat e timer e intenção de voto

		# a outra fica recebendo info e commit

	#obs: no fim do dia acaba sendo uma thread pra ficar recebendo pacote e encaminhando pra cada função, ent uma thread escuta e uma faz é mais jogo se pa

def main_lider():
	#2 threads
		# uma fica mandando heartbeat e cuidando de timer

		# a outra vai ficar recebendo do cliente e encaminhando pros seguidores

def main():
	if (LIDER):
		main_lider()
	else:
		main_seguidor()

if __name__ == '__main__':
	main()