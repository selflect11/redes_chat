import socket, threading, readline, sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

nome = input('nome: ')
prefix = nome+"> "

def readline_print(msg):
	buf_len = len(readline.get_line_buffer())
	sys.stdout.write('\r' + ' '*(buf_len + len(prefix)) + '\r')
	print(msg)
	sys.stdout.write(prefix + readline.get_line_buffer())
	sys.stdout.flush()

def receiver(sock):
	while True:
		try:
		    data = sock.recv(1024)
		    if data:
			    msg = data.decode('UTF-8')
			    # c34ded3865d1e24d1fb0c2d3313020f0
			    readline_print(msg)
		except Exception as e:
		    print(e)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s.connect((TCP_IP, TCP_PORT))
# Send name
s.send(bytes(nome, 'UTF-8'))

tr = threading.Thread(target = receiver, args = (s, ))
tr.start()

try:
	while True:
		msg = input(prefix)
		s.send(bytes(msg, 'UTF-8'))
except Exception as e:
	print(e)
finally:
	s.close()
