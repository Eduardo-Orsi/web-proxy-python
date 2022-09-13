# Simple proxy server for Class assignment
from socket import *
import sys

if len(sys.argv) <= 1:
    print ('Usage: "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address of the Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerPort = 8000
tcpSerSock = socket(AF_INET, SOCK_STREAM)


#fill start
# Prepare a server socket
serverip = sys.argv[1] #from argument
print (serverip)
tcpSerSock.bind((serverip, tcpSerPort))
tcpSerSock.listen(5)
#fill end

while True:
    # Start receiving data from the client
    print ('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('Received a connection from: ', addr)
    
    #fillstart
    message = tcpCliSock.recv(1024)
    #fillend
    print (message)
    
    # Extract the filename from the given message
    print (message.split()[1])
    message=str(message)
    filename = message.split()[1].partition("/")[2]
    filename = str(filename)
    filename=filename.replace("'",'')
    filename=filename.replace("/",'')
    filename=filename.replace("b",'')
    fileExist = "false"
    filetouse = "/" + filename
    try:

        f = open(filetouse[1:], "r")#verifica se o arquivo existe na cache, passando por paramentro o nome, com r de read
        outputdata = f.readlines()
        fileExist = "true"
        print ('File Exists!')
        # Devolve a mensangem pro proxy que que teve um hit(acerto) e devolve a resposta usando o padrao http/1.0
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())
        #envia para o cliente o pacote
        for i in range(0, len(outputdata)):#lê os arquivos linha por linha e envia
            tcpCliSock.send(outputdata[i].encode())
        print ('Read from cache')
    except IOError:#caso não esteja na cache
        print ('File Exist: ', fileExist)
        if fileExist == "false":
            #cria o sockt com o protocolo TCP IP
            print ('Creating socket on proxyserver')
            c = socket(AF_INET, SOCK_STREAM)
            #criado com sucesso
            
            hostn = filename.replace("www.", "", 1)
            print ('Host Name: ', hostn)
            try:
                #conecta no socket com na porta 80
                #Tenta preencher o inicio do socket 
                c.connect((hostn, 80))
                #Terminou de preencher o socket
                print ('Socket connected to port 80 of the host')
                # le as linhas do arquivo requerido pelo cliente
                fileobj = c.makefile('r', 0)
                fileobj.write("GET " + "http://" + filename + " HTTP/1.0\n\n")
                # le a linha de resposta do buffer
                buff = fileobj.readlines()
                final = []
                for line in buff:
                    l = line.replace('href="/','href="http://' + filename + '/')#le linha por linha do buffer e da um append da linha em uma lista final
                    l = l.replace('src="/','href="http://' + filename + '/')
                    final.append(l)
                #fill end
                
                # cria um novo arquivo na cache
                # e tambem envia uma resposta para o cliente
                # e o arquivo correspondente na cache
                tmpFile = open("./" + filename, "wb")
                for i in final:
                    tmpFile.write(i)
                    tcpCliSock.send(i)

            except Exception as inst:
                print ('Illegal request')
                print (inst)

        else:
            # HTTP response message for file not found
            #fill start
            tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n".encode())
            #fill end
            
    # Close the socket and the server sockets
    tcpCliSock.close()

#fill start 
#fill end