INI_BYT_TIP = 0
TAM_BYT_TIP = 1 # 0: indefinido 1: heartbeat 2: msg 3: pedido/voto
INI_BYT_TXT = INI_BYT_TIP + TAM_BYT_TIP
TAM_BYT_TXT = 6 # 5 chars
INI_BYT_TRM = INI_BYT_TXT + TAM_BYT_TXT
TAM_BYT_TRM = 4 # 1 int do termo atual
INI_BYT_CMT = INI_BYT_TRM + TAM_BYT_TRM
TAM_BYT_CMT = 1 # flag de commit ou n commit 0 : False 1: True
INI_BYT_IDT = INI_BYT_CMT + TAM_BYT_CMT
TAM_BYT_IDT = 4 # 1 int, id atual da sequencia de palavras

def inic_pacote():
	return list(
		("0" * TAM_BYT_TIP) +
		("a" * TAM_BYT_TXT) +
		("0" * TAM_BYT_TRM) +
		("0" * TAM_BYT_CMT) + 
		("0" * TAM_BYT_IDT) )

def int_para_chars(valor, tam):
	return list(str(valor).zfill(tam)[:tam])
def chars_para_int(chars):
	return int(''.join(chars) or '0')
def str_para_chars(valor, tam):
	return list(valor.ljust(tam)[:tam])
def chars_para_str(chars):
	resultado = ""
	for c in chars:
		resultado += str(c)
	return str(resultado)
def pacote_para_string(pacote):
	resultado = ""
	for c in pacote:
		resultado += str(c)
	return str(resultado)

T_IN = 0
T_HB = 1
T_MS = 2
T_PV = 3
T_VT = 4

def escreve_tipo(msg, tipo):
	msg[INI_BYT_TIP : (INI_BYT_TIP + TAM_BYT_TIP)] = int_para_chars(tipo, TAM_BYT_TIP)
def le_tipo(msg):
	return chars_para_int(msg[INI_BYT_TIP : (INI_BYT_TIP + TAM_BYT_TIP)])

def escreve_texto(msg, texto):
	msg[INI_BYT_TXT : (INI_BYT_TXT + TAM_BYT_TXT)] = str_para_chars(texto, TAM_BYT_TXT)
def le_texto(msg):
	return chars_para_str(msg[INI_BYT_TXT : (INI_BYT_TXT + TAM_BYT_TXT)])

def escreve_termo(msg, termo):
	msg[INI_BYT_TRM : (INI_BYT_TRM + TAM_BYT_TRM)] = int_para_chars(termo, TAM_BYT_TRM)
def le_termo(msg):
	return chars_para_int(msg[INI_BYT_TRM : (INI_BYT_TRM + TAM_BYT_TRM)])

def escreve_commit(msg, commit):
	msg[INI_BYT_CMT : (INI_BYT_CMT + TAM_BYT_CMT)] = str_para_chars(commit, TAM_BYT_CMT)
def le_commit(msg):
	return chars_para_str(msg[INI_BYT_CMT : (INI_BYT_CMT + TAM_BYT_CMT)])

def escreve_id_atual(msg, id_at):
	msg[INI_BYT_IDT : (INI_BYT_IDT + TAM_BYT_IDT)] = int_para_chars(id_at, TAM_BYT_IDT)
def le_id_atual(msg):
	return chars_para_int(msg[INI_BYT_IDT : (INI_BYT_IDT + TAM_BYT_IDT)])

def print_pacote(msg):
	print(le_tipo(msg))
	print(f"{le_id_atual(msg)}: {le_texto(msg)} ({le_commit(msg)})")
	print(le_termo(msg))