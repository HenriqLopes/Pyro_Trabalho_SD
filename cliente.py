import Pyro5.api

import defs
	
def main():

	link_dns = Pyro5.api.locate_ns()
	uri_lid = link_dns.lookup(defs.NS_LIDER)
	proxy_lid = Pyro5.api.Proxy(uri_lid)

	buffer = 'teste'
	proxy_lid.recebe_texto(buffer)

	while (1):
		buffer = input("- ")
		proxy_lid.recebe_texto(buffer)
	
if __name__ == '__main__':
	main()