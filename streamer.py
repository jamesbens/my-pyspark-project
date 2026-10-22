# Listen for text inpurt on port 9999

import socket
s= socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 9999))
s.listen(1)
c, _ = s.accept()
while True:
    c.send((input() + '\n').encode())