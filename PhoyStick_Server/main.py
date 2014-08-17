'''
Created on 2014. 8. 14.

@author: Jooney
'''
from javax.swing import JButton, JFrame
from SocketServer import ThreadingTCPServer, StreamRequestHandler

PORT = 1920

keynum = {'uP':1, 'dP':1, 'lP':1, 'rP':1, 'uU':1, 'dU':1, 'lU':1, 'rU':1,
          'aP':1, 'bP':1, 'cP':1, 'aU':1, 'bU':1, 'cU':1,
          'xP':1, 'yP':1, 'zP':1, 'xU':1, 'yU':1, 'zU':1,
          'stP':1, 'paP':1, 'stD':1, 'paD':1}

class RequestHandler(StreamRequestHandler):
    def handle(self):
        print 'connection from', self.client_address
        conn = self.request
        while 1:
            msg = conn.recv(20)
            if msg == "keymap":
                print "keymapping!"
                keymapFrame = JFrame('Key Mapping Configuration',
                               defaultCloseOperation = JFrame.EXIT_ON_CLOSE,
                               size = (300, 500)
                               )
                keyButton = JButton('Press any key in iPhone')
                keymapFrame.add(keyButton)
                keymapFrame.visible = True
                while 1:
                    recvKey = conn.recv(20)
                    keyButton.setLabel("%s?" % recvKey)
                    keyInput = raw_input()
                    keynum[recvKey] = keyInput
                    keyButton.setText('Press any key in iPhone')
                    if recvKey == "keymap":
                        keymapFrame.visible = False
                        break
            if msg == "quit()":
                conn.close()
                print self.client_address, 'disconnected'
                break
            print self.client_address, msg

frame = JFrame('PhoyStick Proto Server',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE,
            size = (300, 300)
        )

button = JButton('Click Me!')
frame.add(button)
frame.visible = True
try:
    server = ThreadingTCPServer(('', PORT), RequestHandler)
except:
    PORT -= 1
    server = ThreadingTCPServer(('', PORT), RequestHandler)
print 'Listening Port : ', PORT
server.serve_forever()
