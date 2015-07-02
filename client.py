import socket, threading, readline, sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

nome = input('nome: ')
prefix = nome+"> "

def receiver(sock):
	lock = threading.Lock()
	data = sock.recv(4096)
	if data:
		lock.acquire()
		print('Testing...\n')
		msg = data.decode('UTF-8')
		# c34ded3865d1e24d1fb0c2d3313020f0
		buf_len = len(readline.get_line_buffer())
		sys.stdout.write('\r' + ' '*(buf_len + len(prefix)) + '\r')
		print(msg)
		sys.stdout.write(prefix + readline.get_line_buffer())
		sys.stdout.flush()
		lock.release()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(bytes(nome, 'UTF-8'))

tr = threading.Thread(target = receiver, args = (s, ))
tr.start()

while True:
	msg = input(prefix)
	s.send(bytes(msg, 'UTF-8'))
	print('Client Thread is alive:', tr.isAlive())
s.close()