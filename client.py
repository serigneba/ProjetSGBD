# coding: utf-8
import socket
import serignedb
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
requete = input(">> ") # utilisez raw_input() pour les anciennes versions python
requete1 = serignedb.space(requete)
requete2 = requete1.split("#")
if len(requete2) == 5:
	ipserveur = "localhost"
if len(requete2) == 7:
	if requete2[5].upper() == "-IP":
		ipserveur = requete2[6]
	else:
		print("syntax error")
		serignedb.quit()
if len(requete2) != 5 and len(requete2) != 7:
	print("syntax error")
	serignedb.quit()
s.connect((ipserveur, 8888))
s.send(requete.encode())
auth = s.recv(2048)
auth = auth.decode()
if auth == "erreur syntaxe" or auth == "not connected":
	print(auth)
if auth == "connected":
	bloq = 0
	while 1:
		requete = input("serignedb> ") # utilisez raw_input() pour les anciennes versions python
		s.send(requete.encode())
		reponse = s.recv(2048)
		reponse = reponse.decode()
		requete = serignedb.space(requete)
		cle = requete.split("#")
		if cle[0].upper() == "SELECT" and bloq == 0:
			if reponse == "table not exists" or reponse == "syntax error":
				print("\n"+reponse+"\n")
			else:
				tab = reponse.split("|")
				attr = tab[0]
				data = tab[1]
				attr_1 = attr.split("#")
				data_1 = data.split("#")
				mod = 0
				for x in range(0,len(attr_1)-1):
					print("{:^15s}".format("_______________"),end='')
				print('')
				for x in range(0,len(attr_1)-1):
					print("{:^15s}".format(attr_1[x]),end='')
					if x!= len(attr_1) -2:
						print("|",end='')
				print('')
				for x in range(0,len(attr_1)-1):
					print("{:^15s}".format("_______________"),end='')
				print('')
				while(mod != len(data_1)-1):
					for x in range(mod,mod+len(attr_1)-1):
						print("{:^15s}".format(data_1[x]),end='')
						if x != mod+len(attr_1) -2:
							print("|",end='')
					mod+=len(attr_1)-1
					print('')
				for x in range(0,len(attr_1)-1):
					print("{:^15s}".format("_______________"),end='')
				print('')	
		if cle[0].upper() == "DESCRIBE" and bloq == 0:
			if reponse == "table doesn't exist"	or reponse == "syntax error":
				print("\n"+reponse+"\n")
			else:
				attr_1 = reponse.split("#")
				for x in range(0,len(attr_1)-1):
					print("{:^15s}".format("_______________"),end='')
				print('')
				for x in range(0,len(attr_1)-1):
					print("{:^15s}".format(attr_1[x]),end='')
					if x!= len(attr_1) -2:
						print("|",end='')
				print('')
				for x in range(0,len(attr_1)-1):
					print("{:^15s}".format("_______________"),end='')
				print('')
		if cle[0].upper() == "SHOW" and bloq == 0:
			if reponse == "table doesn't exist"	or reponse == "syntax error":
				print("\n"+reponse+"\n")
			else:	
				attr_1 = reponse.split("#")
				print("{:^15s}".format("________________"),end='')
				print("")
				print("{:^15s}".format("DATABASE"),end='')
				print("|")
				print("{:^15s}".format("________________"),end='')
				print('')
				for x in range(0,len(attr_1)):
					base = attr_1[x].split(".")
					print("{:^15s}|".format(base[0]))
			print('')
		if cle[0].upper() == "QUIT":
			print("\n"+reponse+"\n")
			serignedb.quit()
		if cle[0].upper() == "START":
			bloq = 1
		if cle[0].upper() == "COMMIT":
			bloq = 0
			print("\n"+reponse+"\n")
		if cle[0].upper() == "ROLLBACK":
			bloq = 0
			print("\n"+reponse+"\n")	
		if cle[0].upper()!="SHOW" and cle[0].upper()!="DESCRIBE" and cle[0].upper()!="SELECT" and cle[0].upper()!="QUIT" and cle[0].upper()!="START" and cle[0].upper()!="COMMIT" and cle[0].upper()!="ROLLBACK"  or bloq == 1:	
			print("\n"+reponse+"\n")