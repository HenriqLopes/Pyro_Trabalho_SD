import Pyro5.api

import defs

#vai no DNS e pega o ip do lider
def achar_lider():
	link_dns = Pyro5.api.locate_ns()
	uri_lid = link_dns.lookup(defs.NS_LIDER)
	proxy_lid = Pyro5.api.Proxy(uri_lid)
	return proxy_lid
	
def main():
	p_lid = achar_lider()

	buffer = 'teste'
	p_lid.recebe_texto(buffer)

	while (1):
		buffer = input("- ")
		p_lid.recebe_texto(buffer)
	
if __name__ == '__main__':
	main()