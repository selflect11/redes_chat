import socket
import threading
import time
import signal


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20
ENCODING = 'UTF-8'

message_queue = []
usernames = {}

def receiver(conn, addr):
	try:
		while True:
			data = conn.recv(1024)
			if data:
				msg = data.decode(ENCODING)
				print('recebido:', msg)
				if usernames.get(addr) == None:
					usernames[addr] = msg
				else:
					message_queue.append((addr, msg))
	except:
		conn.close()

def sender(conn, addr):
	last_msg_read = len(message_queue)
	try:
		while True:
			time.sleep(5)
			count = len(message_queue)
			if count > last_msg_read:
				for m_addr, msg in message_queue[last_msg_read:]:
					if m_addr != addr:
						# Username might not be set
						data = bytes(usernames[m_addr] + ': ' + msg, ENCODING)
						print("sending: " + usernames[m_addr] + ': ' + msg)
						conn.send(data)
				last_msg_read = count
	except Exception as e:
		print(e)
		print("Closing conn...")
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
		ts = threading.Thread(target = sender, args = (conn, addr))
		tr.start()
		ts.start()
	except:
		# Let's just ignore it for now >8)
		pass
