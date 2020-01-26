import sys
import simplejson
import os
#gestion de l'authentification
def authentification(chaine):
	chaine = space(chaine)
	elements = chaine.split("#");
	if len(elements) < 4:
		return "syntax erroe"
	if elements[0].upper() == "SERIGNEDB" and elements[1] == "-u":
		if elements[3] == "-p":
			if len(elements) > 4:
				user = elements[2]
				password = elements[4]
				auth = identify(user,password)
				return auth
			else:
				return "syntax error"
		if elements[3] != "-p":
			return "syntax error"
	else:
		return "syntax error"
#LDD
def create(chaine,base):
	chaine = space(chaine)
	elements = chaine.split("#");
	if elements[1].upper() == "DATABASE":
		if len(elements) < 3:
			return "syntax error"
		if os.path.exists("base/"+elements[2]+".json"):
			return "database already exists"
		else:
			with open("base/"+elements[2]+".json","w") as f:
				f.write('')
			f.close()
			return "database created"
	if elements[1].upper() == "TABLE":
		if len(elements) < 3:
			return "syntax error"
		if base == "":
			return "no database selected"
		with open("base/"+base+".json","r") as f:	
			size = os.path.getsize("base/"+base+".json")
			if size == 0:
				liste = {}
			else:
				liste = simplejson.load(f)
				for dict in liste:
					if dict == elements[2]:
						return"table already exist"
		liste[elements[2]] = []
		with open("base/"+base+".json","w") as g:
			simplejson.dump(liste,g,indent = 4)
		f.close()
		g.close()
		return "table created"
	if elements[1].upper() == "USER":
		if len(elements) < 4:
			return "syntax error"
		password = elements[3]
		with open("base/users.json","r") as f :
			chaine = f.read()
			if chaine[0] != "[":
				chaine = "["+chaine+"]"
			liste = simplejson.loads(chaine)
		f.close()
		exist = False
		for dict in liste:
			if dict["id"] == elements[2]:
				if dict["password"] == password:
					exist = True
					break
		if exist == True:
			return "user already exists"
		liste.append({"id":elements[2],"password":password})
		with open("base/users.json","w") as g:
			simplejson.dump(liste,g,indent =4)
		g.close()
		return "user created"
	else:
		return "syntax error"		         
def drop(chaine,base):
	chaine = space(chaine)
	elements = chaine.split("#")
	if len(elements) < 3:
		return "syntax error"
	if elements[1].upper() == "DATABASE":
		if os.path.exists("base/"+elements[2]+".json"):
			os.remove("base/"+elements[2]+".json")
			return "database removed"
		else:
			return "database not exist"
	if elements[1].upper() == "TABLE":
		if base == "":
			return "no database selected"
		with open("base/"+base+".json","r") as f:	
			size = os.path.getsize("base/"+base+".json")
			if size == 0:
				return "database empty"
			else:
				exist = False
				liste = simplejson.load(f)
				for dict in liste:
					if dict == elements[2]:
						del liste[dict]
						exist = True
						break
			if exist == False:
				return "table not exists"
		with open("base/"+base+".json","w") as g:
			simplejson.dump(liste,g,indent = 4)
		f.close()
		g.close()
		return "table deleted"
	else:
		return "syntaxe error"
def alter(chaine,base):
	chaine = space(chaine)
	elements = chaine.split("#")
	if len(elements) < 4 or elements[3].split("=")[0].upper() != "NAME":
		return "syntax error"
	new_name = elements[3].split("=")[1]
	if elements[1].upper() == "DATABASE":
		if os.path.exists("base/"+elements[2]+".json"):
			os.rename("base/"+elements[2]+".json","base/"+new_name+".json")
			return "database altered"
	if elements[1].upper() == "TABLE":
		if base == "":
			return "no database selected"
		with open("base/"+base+".json","r") as f:	
			size = os.path.getsize("base/"+base+".json")
			if size == 0:
				return "database empty"
			else:
				exist = False
				liste = simplejson.load(f)
				for dict in liste:
					if dict == elements[2]:
						dict = new_name
						exist = True
						break
			#a redefinir
			if exist == False:
				return "table not exists"
		with open("base/"+base+".json","w") as g:
			simplejson.dump(liste,g,indent = 4)
		f.close()
		g.close()
		return "table altered"
	if elements[1].upper() != "DATABASE" and elements[1].upper() != "TABLE":
		return "syntaxe error"
#LMD
def insert(chaine,base):
	chaine = space(chaine)
	elements = chaine.split("#")
	if len(elements) < 4 or elements[1].upper() != "INTO":
		return "syntax error"
	tab = elements[4].split("(")
	#print(tab)
	tab = tab[1].split(")")
	tab = tab[0].split(",")
	attr = []
	data = []
	#print(tab)
	for ch in tab:
		t = ch.split("=")
		attr.append(t[0])
		data.append(t[1])
	d = {}
	for i in range(0,len(attr)):
		d[attr[i]] = data[i]
	if base == "":
		return "no database selected"
	with open("base/"+base+".json","r") as f:	
		size = os.path.getsize("base/"+base+".json")
		if size == 0:
			liste = {}
		else:
			liste = simplejson.load(f)
			exist = False
			for dict in liste:
				if dict == elements[2]:
					exist =True
					t = []
					if not liste[dict]:
						liste[dict].append(d)
					else:
						for cle in liste[dict][0].keys():
							t.append(cle)
						if t == attr:
							liste[dict].append(d)
						else:
							return "attributs incorects"
					#return "insertion success"
			if exist == False:
				return "table n'existe pas"
	with open("base/"+base+".json","w") as g:
		simplejson.dump(liste,g,indent = 4)
	f.close()
	g.close()
	return "insertion success"
def update(chaine,base):
	if base == "":
		return "no database selected"
	chaine = space(chaine)
	elements = chaine.split("#")
	if len(elements) == 5 and elements[2].upper() == "ADD" and elements[3].upper() == "ATTRIB":
		with open("base/"+base+".json","r") as f:
			size = os.path.getsize("base/"+base+".json")
			if size == 0:
				return "database empty"
			exist = False
			liste = simplejson.load(f)
			for dict in liste:
				if dict == elements[1]:
					exist = True
					for i in range(0,len(liste[dict])):
						liste[dict][i].update({elements[4]:""})
		with open("base/"+base+".json","w") as g:
					simplejson.dump(liste,g,indent=4)
		return "update success"
	if len(elements) < 6 or elements[2].upper() != "SET" or elements[4].upper() != "WHERE":
		return "syntax error"
	with open("base/"+base+".json","r") as f:
		size = os.path.getsize("base/"+base+".json")
		if size == 0:
			return "database empty"
		liste = simplejson.load(f)
		cle_ch = elements[3].split("=")[0]
		new_value = elements[3].split("=")[1]
		cle_ind =  elements[5].split("=")[0]
		old_value = elements[5].split("=")[1]
		exist = False
		for dict in liste:
			if dict == elements[1]:
				exist = True
				for i in range(0,len(liste[dict])):
					if liste[dict][i][cle_ind] == old_value:
						liste[dict][i][cle_ch] = new_value
		if exist == False:
			return "table doesn't exist"
	with open("base/"+base+".json","w") as g:
		simplejson.dump(liste,g,indent=4)
	return "update success"
def delete(chaine,base):
	if base == "":
		return "no database selected"
	chaine = space(chaine)
	elements = chaine.split("#")	
	if len(elements) < 5 or elements[1].upper() != "FROM" or (elements[3].upper() != "WHERE" and elements[3].upper() != "ATTRIB") :
		return "syntax error" 
	if elements[3].upper() == "ATTRIB":
		with open("base/"+base+".json","r") as f:
			size = os.path.getsize("base/"+base+".json")
			if size == 0:
				return "database empty"
			liste = simplejson.load(f)
			exist=False
			for dict in liste:
				if dict == elements[2]:
					exist = True
					vattr=[]
					for e in liste[dict]:
						for attr0,data0 in e.items():
							if attr0 in vattr:
								pass
							else:
								vattr.append(attr0)
					if elements[4] in vattr:
						for i in range(0,len(liste[dict])):
							del liste[dict][i][elements[4]]
					else:
						return "attrib unknown"
			if exist == False:
				return "table doesn't exist"
		with open("base/"+base+".json","w") as g:
			simplejson.dump(liste,g,indent=4)
		return "delete success"
	tab = elements[4].split(",")
	attr = []
	data = []
	#if 
	for e in tab:
		attr.append(e.split("=")[0])
		data.append(e.split("=")[1])
	#print(attr)
	with open("base/"+base+".json","r") as f:
		size = os.path.getsize("base/"+base+".json")
		if size == 0:
			return "database empty"
		liste = simplejson.load(f)
		for dict in liste:
			if dict == elements[2]:
				exist = True
				vattr=[]
				for e in liste[dict]:
					for attr0,data0 in e.items():
						if attr0 in vattr:
							pass
						else:
							vattr.append(attr0)
					#print(vattr)
					for x in range(0,len(attr)):
						if attr[x] in vattr:
							pass
						else:
							return "attrib uknown"
					x=0
					v = True
					while(x < len(attr) and v==True):
						if e[attr[x]] == data[x]:
							x +=1
						else:
							v=False
					if v == True:
						liste[dict].remove(e)
		if exist == False:
			return "table doesn't exist"
	with open("base/"+base+".json","w") as g:
		simplejson.dump(liste,g,indent=4)
	return "delete success"
#LED
def select(chaine,base):
	if base == "":
		return "no database selected"
	chaine = space(chaine)
	elements = chaine.split("#")
	if len(elements) < 4:
		return "syntax error"
	if elements[1] == "*":
		with open("base/"+base+".json","r") as f:
			liste = simplejson.load(f)
		exist = False
		attr_1 = []
		data_1 = []
		for dict in liste:
			if dict == elements[3]:
				exist =True
				d = liste[dict]
				for e in d:
					for attr,data in e.items():
						if attr in attr_1:
							pass
						else:
							attr_1.append(attr)
						data_1.append(data)
				attr_2 = ""
				data_2 = ""
				for e in attr_1:
					attr_2 += e+"#"
				for e in data_1:
					data_2 += e+"#"
				return attr_2+"|"+data_2 
		if exist == False:
			return "table not exists"
	else:
		attr_0= elements[1].split(",")
		with open("base/"+base+".json","r") as f:
			liste = simplejson.load(f)
		exist = False
		attr_1 = []
		data_1 = []
		for dict in liste:
			if dict == elements[3]:
				exist = True
				d = liste[dict]
				for e in d:
					for attr,data in e.items():
						if attr in attr_0:
							if attr in attr_1:
								pass
							else:
								attr_1.append(attr)
							data_1.append(data)		
				attr_2 = ""
				data_2 = ""
				for e1 in attr_1:
					attr_2 += e1+"#"
				for e2 in data_1:
					data_2 += e2+"#"
				#print(data_2)
				return attr_2+"|"+data_2 
		if exist == False:
			return "table not exists"

def space(chaine):
	chaine1=""
	j=0
	for i in range(0,len(chaine)):
		if chaine[i] == " ": 
			if chaine[i-1] == " " or chaine[i-1] == "," or chaine[i-1] == "=" or chaine[i+1] == "," or chaine[i+1] == "=" or chaine[i+1] == "(" or i==0:
				pass
			else:
				chaine1+="#" 
		else:
			if chaine[i] !="(":
				chaine1+=chaine[i]
		if chaine[i] == "(":
				chaine1 += "#("	
	return chaine1

# gestion des transaction
def start(chaine,base,tampon):
	if base == "":
		return "no database selected"
	chaine = space(chaine)
	elements = chaine.split("#")
	if len(elements) < 2 or elements[1].upper() != "TRANSACTION":
		return "syntax error"
	with open("base/"+base+".json","r") as f:
		liste = simplejson.load(f)
	with open("base/"+tampon+".json","w") as g:
		simplejson.dump(liste,g,indent=4)
	return "transaction started"
def commit(chaine,base,tampon):
	chaine = space(chaine)
	elements = chaine.split("#")
	with open("base/"+tampon+".json","r") as f:
		liste = simplejson.load(f)
		print(liste)
	with open("base/"+base+".json","w") as g:
		simplejson.dump(liste,g,indent=4)
		print("OK")
	os.remove("base/"+tampon+".json")
	return "saved"
def rollback(chaine,base,tampon):
	os.remove("base/"+tampon+".json")
	return "aborted"
# fonction pour vérifier une authentifiaction
def identify(user,password):
	with open("base/users.json","r") as f :
		chaine = f.read()
	if chaine[0] != "[":
		chaine = "["+chaine+"]"
	liste = simplejson.loads(chaine)
	auth = False
	for dict in liste:
		if dict["id"] == user:
			if dict["password"] == password:
				auth = True
				break
	if auth == True:
		return "connected"
	else:
		return "not connected"
	f.close()
def describe(chaine,base):
	if base == "":
		return "no database selected"
	chaine = space(chaine)
	elements = chaine.split("#")
	if len(elements) < 2:
		return "syntaxe error"
	with open("base/"+base+".json","r") as f:
		size = os.path.getsize("base/"+base+".json")
		if size == 0:
			return "database empty"
		liste = simplejson.load(f)
		exist = False
		attr_1 = []
		for dict in liste:
			if dict == elements[1]:
				exist =True
				d = liste[dict]
				for e in d:
					for attr,data in e.items():
						if attr in attr_1:
							pass
						else:
							attr_1.append(attr)
				attr_2 = ""
				for e in attr_1:
					attr_2 += e+"#"
				return attr_2
		if exist == False:
			return "table doesn't exist"
def show(chaine,base):
	chaine = space(chaine)
	elements = chaine.split("#")
	if len(elements) < 2:
		return "syntaxe error"
	if elements[1].upper() == "DATABASES": 
		dossier = os.listdir("./base")
		ch = ""
		for chaine in dossier:
			ch+="#"+chaine
		return ch	
	else:
		if elements[1].upper() == "TABLES":
			with open("base/"+base+".json","r") as f:
				size = os.path.getsize("base/"+base+".json")
				if size == 0:
					return "database empty"
				liste = simplejson.load(f)
				ch=""
				for dict in liste:
					ch+=dict+"#"
				return ch
		else:
			return "syntax error"
def quit():
	sys.exit(0)