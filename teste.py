import Pyro5.api

@Pyro5.api.expose
class processo:
	def __init__ (self, id, arquivo, termo, lider):
		self.id_atual = 0
		self.id = id
		self.arquivo = arquivo
		self.termo = termo
		self.lider = lider

daemon = Pyro5.api.Daemon()             # make a Pyro daemon
uri = daemon.register(processo)

print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
daemon.requestLoop()