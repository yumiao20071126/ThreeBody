import socket
import keyboard

class ThreeBodyClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.client_socket = None

    def connect(self):
        print('客户端启动')
        # 创建TCP/IP套接字
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect(self.server_address)
        print('已连接到', self.server_address)

    def send_message(self, send_data):
        print('发送:', send_data)
        self.client_socket.sendall(send_data.encode())
        
        # 接收响应
        receive_data = self.client_socket.recv(1024)
        a = int(receive_data.decode())
        print('收到:', receive_data.decode())

    def on_key_event(self, event):
        if event.name == 'w':
            self.send_message('1')
        elif event.name == 's':
            self.send_message('2')
        elif event.name == 'a':
            self.send_message('3')
        elif event.name == 'd':
            self.send_message('4')
        elif event.name == 'x':
            self.send_message('5')
        elif event.name == 'z':
            self.send_message('6')
        elif event.name == 'esc':
            print('退出客户端')
            self.client_socket.close()
            exit()

    def start(self):
        self.connect()

        while True:
            # 监听按键事件

            keyboard.on_press(self.on_key_event)

            # 保持程序运行
            #print('按下 w, a, s, d 键发送消息，按下 esc 键退出')
            pass


    # finally:
    #     # 关闭连接
    #     self.client_socket.close()

if __name__ == "__main__":
    server_address = ('183.173.9.217', 65437)  # 替换为服务器的实际IP地址
    client = ThreeBodyClient(server_address)
    client.start()