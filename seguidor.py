
#coisas que vai ter que saber
#N_PROCESSOS pra usar maioria e fors
# IP/AQUELE BAGUI LA DE ASSINATURA de cada um dos processos (isso vai pra um arq separado se pa)
# TIMER PROPRIO pra valida os hb

#thread de manutenção do hb
def heart_beat():
	if (LIDER):
		#manda o hb
	else:
		#espera o hb e cuida do timer

#chamada quando o timer do hb da pau
def inicia_eleicao():
	#manda pedido de voto pra todo mundo
	#fica contabilizando até dar maioria

	#quando somar maioria, muda sua flag pra lider
	#atualiza o lider no DNS
	# avisa todo mundo pra atualizarem seus termos, um novo xerife chegou na cidade

#chamada quando alguem pede seu voto
def pesquisa_eleitoral():
	#confere se o termo dele ta atualizado
		#se tiver, ai vota nele e ja era

		#se não tiver, ai se elege... ou só n vota só.

# chamada quando virar o novo lider
def se_registra_como_lider():
	#se coloca no DNS
	#avisa todo mundo pra atualizar o termo

#chamada quando o processo ta normal , cliente mandou um char
def add_info():
	#adiciona o char passado no buffer não comitado

#chamada pelo lider
def commit():
	#atualiza o buffer real copiando o não commitado

#chamada quando  o timer proprio cair, e a eleição me colocar como lider? acho que n sei na real... tem que perguntar se pa
def rollback():
	#atualiza o buffer temporario (não commitado) copiando o buffer real

#retorna True ou False se o termo de uma msg é o mesmo do processo
def confere_termo():
	#protocolo e um if.

#thread que vai ficar esperando as entradas do cliente (LA ELE)
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