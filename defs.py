daemon = Pyro5.api.Daemon(porta)             # make a Pyro daemon
uri = daemon.register(processo, nome)   