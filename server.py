import socket
import threading
import time
import signal


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20
ENCODING = 'UTF-8'

client_list = []

sending_lock = threading.Lock()

def send_msg(conn, sender_name, msg):
	data = bytes(sender_name + ': ' + msg, ENCODING)
	conn.send(data)

def send_to_all(msg, username, addr):
	# Global sending lock
	# We can do for each connection also
	sending_lock.acquire()
	try:
		for c_conn, c_addr, c_tr in client_list:
			if c_addr != addr:
				send_msg(c_conn, username, msg)
	except Exception as e:
		print(e)
	finally:
		sending_lock.release()

def receiver(conn, addr):
	try:
		username = None
		while True:
			data = conn.recv(1024)
			if data:
				msg = data.decode(ENCODING)
				print('recebido:', msg)
				if username == None:
					print('setting username')
					username = msg
				else:
					send_to_all(msg, username, addr)
	except:
		print('closing connection')
		conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

s.bind((TCP_IP, TCP_PORT))
s.listen(2)
print('Server running on port: ',TCP_PORT)
while True:
	try:
		conn, addr = s.accept()
		tr = threading.Thread(target = receiver, args = (conn, addr))
		client_list.append((conn, addr, tr))
		tr.start()
	except:
		# Let's just ignore it for now >8)
		pass
