import socket
import keyboard

def send_message(send_data, client_socket):
    print('发送:', send_data)
    client_socket.sendall(send_data.encode())
    
    # 接收响应
    receive_data = client_socket.recv(1024)
    a = int(receive_data.decode())
    print('收到:', receive_data.decode())


def on_key_event(event, client_socket):
    if event.name == 'w':
        send_message('1')
    elif event.name == 's':
        send_message('2')
    elif event.name == 'a':
        send_message('3')
    elif event.name == 'd':
        send_message('4')
    elif event.name == 'x':
        send_message('5')
    elif event.name == 'z':
        send_message('6')
    elif event.name == 'esc':
        print('退出客户端')
        client_socket.close()
        exit()

#这个函数用于连接服务器
def connecting(server_address):
    print('客户端启动')
    # 创建TCP/IP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect(server_address)
    print('已连接到', server_address)
    return client_socket


def start_client():

    # 连接服务器
    server_address = ('183.173.9.217', 65437)  # 替换为服务器的实际IP地址
    client_socket=connecting(server_address)
    
    try:
        

        # 定义按键事件处理函数
        
        #on_key_event(event)
        #传回数据stars,spaceships, momentum_weapon, scale,bias_x,bias_y

        # 监听按键事件
        keyboard.on_press(on_key_event)

        # 保持程序运行
        print('按下 w, a, s, d 键发送消息，按下 esc 键退出')
        keyboard.wait('esc')

    finally:
        # 关闭连接
        client_socket.close()

if __name__ == "__main__":
    start_client()
