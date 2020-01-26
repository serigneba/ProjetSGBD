# coding: utf-8 
import os
import socket
import threading
import serignedb
from random import randint
class ClientThread(threading.Thread):
    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
    def run(self):    
        print("Connexion de %s %s" % (self.ip, self.port, ))
        r = self.clientsocket.recv(2048)
        requete = r. decode()
        auth = serignedb.authentification(requete)
        self.clientsocket.send(auth.encode())
        if auth == "connected":
            base = ""
            base_init =""
            tampon = ""
            bloq = 0
            while 1:
                r = self.clientsocket.recv(2048)
                requete = r. decode()
                requete = serignedb.space(requete)
                tab_req = requete.split("#")
                #Vérification syntaxe
                
            #LDD
                if tab_req[0].upper() == "CREATE":
                    if bloq == 1:
                        create = "indisponible" 
                    else:
                        create = serignedb.create(requete,base)
                    self.clientsocket.send(create.encode())
                if tab_req[0].upper() == "DROP":
                    if bloq == 1:
                        drop = "indisponible" 
                    else:
                        drop = serignedb.drop(requete,base) 
                    self.clientsocket.send(drop.encode())
                if tab_req[0].upper() == "ALTER":
                    if bloq == 1:
                        alter = "indisponible" 
                    else:
                        alter = serignedb.alter(requete,base )
                    self.clientsocket.send(alter.encode())
            #LMD
                if tab_req[0].upper() == "INSERT":
                    if bloq == 1:
                        base = tampon 
                        insert = serignedb.insert(requete,base)
                        self.clientsocket.send(insert.encode())
                    else:
                        insert = serignedb.insert(requete,base)
                        self.clientsocket.send(insert.encode())
                if tab_req[0].upper() == "DELETE":
                    if bloq == 1:
                        base = tampon 
                        delete = serignedb.delete(requete,base)
                        self.clientsocket.send(delete.encode()) 
                    else:
                        delete = serignedb.delete(requete,base)
                        self.clientsocket.send(delete.encode())
                if tab_req[0].upper() == "UPDATE":
                    if bloq == 1:
                        base = tampon 
                        update = serignedb.update(requete,base)
                        self.clientsocket.send(update.encode())
                    else:
                        update = serignedb.update(requete,base)
                        self.clientsocket.send(update.encode())
            #LID
                if tab_req[0].upper() == "SELECT":
                    if bloq == 1:
                        select = "indisponible" 
                    else:
                        select = serignedb.select(requete,base )
                    self.clientsocket.send(select.encode())
            #Transaction
                if tab_req[0].upper() == "START":
                    bloq = 1
                    base_init = base
                    tampon = str(randint(0,10))
                    while os.path.exists("base/"+tampon+".json"):
                        tampon = str(randint(0,10))
                    start = serignedb.start(requete,base,tampon)
                    self.clientsocket.send(start.encode()) 
                if tab_req[0].upper() == "COMMIT":
                    commit = serignedb.commit(requete,base_init,base)
                    bloq = 0
                    base = base_init
                    self.clientsocket.send(commit.encode()) 
                if tab_req[0].upper() == "ROLLBACK":
                    rollback = serignedb.rollback(requete,base,tampon) 
                    bloq = 0 
                    self.clientsocket.send(rollback.encode()) 
                #elements auxiliaires
                if tab_req[0].upper() == "USE":
                    #if os.path.exists("base/"+tab_req[1]+".json"):
                    if len(tab_req) < 2:
                        use = "erreur syntaxe" 
                    else:
                        if os.path.exists("base/"+tab_req[1]+".json"):
                            base = tab_req[1]
                            use = "database changed"
                        else:
                            use = "database not exist"
                    self.clientsocket.send(use.encode()) 
                if tab_req[0].upper() == "SHOW":
                    if bloq == 1:
                        show = "indisponible" 
                    else:
                        show = serignedb.show(requete,base )
                    self.clientsocket.send(show.encode()) 
                if tab_req[0].upper() == "DESCRIBE":
                    if bloq == 1:
                        desc = "indisponible" 
                    else:
                        desc = serignedb.describe(requete,base )
                    self.clientsocket.send(desc.encode())
                if tab_req[0].upper() == "QUIT":
                    if bloq == 1:
                        quit = "indisponible" 
                    else:
                        quit ="bye bye"
                    self.clientsocket.send(quit.encode())
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",8888))
while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()