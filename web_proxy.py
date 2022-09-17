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

    URL = ""
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
    print("Filename: ", filename)
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
        # HTTP response message for file not found
        #fill start
        tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())
        #fill end
            
    # Close the socket and the server sockets
    tcpCliSock.close()

#fill start 
#fill end
