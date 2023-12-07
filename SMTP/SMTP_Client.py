# Author: Rishab Pallepati  

# Utilizes SMTP in conjunction with TLS to send mails
# to the Gmail mail server

import ssl
import socket
import base64

msg = "Subject: Important Message\r\n\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

print(msg)

recipient = "<alice@gmail.com>"
sender = "<bob@gmail.com>"
username = "bob"
password = "app_password" # to make this work you need to use gmail app password with 2FA (if using gmail)

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.gmail.com"
port = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket.socket()
clientSocket.connect((mailserver, port))
recv = clientSocket.recv(1024).decode()
print (recv)
if recv[:3] != '220':
	print ('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Server\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print (recv1)
if recv1[:3] != '250':
	print ('250 reply not received from server.')

# Request an encrypted connection
startTlsCommand = 'STARTTLS\r\n'
clientSocket.send(startTlsCommand.encode())
tls_recv = clientSocket.recv(1024).decode()
print (tls_recv)
if tls_recv[:3] != '220':
	print ('220 reply not received from server')

# Encrypt the socket
# ssl_clientSocket = socket.ssl(clientSocket)
ssl_clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLSv1_2)

# Send the AUTH LOGIN command and print server response.
authCommand = 'AUTH LOGIN\r\n'
ssl_clientSocket.write(authCommand.encode())
auth_recv = ssl_clientSocket.read(1024).decode()
print (auth_recv)
if auth_recv[:3] != '334':
	print ('334 reply not received from server')

# Send username and print server response.
x = '\r\n'
uname = base64.b64encode(username.encode()) + x.encode()
ssl_clientSocket.write(uname)
uname_recv = ssl_clientSocket.read(1024).decode() 
print (uname_recv)
if uname_recv[:3] != '334':
	print ('334 reply not received from server')

# Send password and print server response.
pword = base64.b64encode(password.encode()) + x.encode()
ssl_clientSocket.write(pword)
pword_recv = ssl_clientSocket.read(1024).decode() 
print (pword_recv)
if pword_recv[:3] != '235':
	print ('235 reply not received from server')

# Send MAIL FROM command and print server response.
mailFromCommand = 'MAIL FROM: ' + sender + '\r\n'
ssl_clientSocket.write(mailFromCommand.encode())
recv2 = ssl_clientSocket.read(1024).decode()
print (recv2)
if recv2[:3] != '250':
	print ('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptToCommand = 'RCPT TO: ' + recipient + '\r\n'
ssl_clientSocket.write(rcptToCommand.encode())
recv3 = ssl_clientSocket.read(1024).decode()
print (recv3)
if recv3[:3] != '250':
	print ('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
ssl_clientSocket.write(dataCommand.encode())
recv4 = ssl_clientSocket.read(1024).decode()
print (recv4)
if recv4[:3] != '354':
	print ('354 reply not received from server.')

# Send message data.
ssl_clientSocket.write(msg.encode())

# Message ends with a single period.
ssl_clientSocket.write(endmsg.encode())
recv5 = ssl_clientSocket.read(1024).decode()
print (recv5)
if recv5[:3] != '250':
	print ('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
ssl_clientSocket.write(quitCommand.encode())
recv6 = ssl_clientSocket.read(1024).decode()
print (recv6)
if recv6[:3] != '221':
	print ('221 reply not received from server.')

clientSocket.close()
