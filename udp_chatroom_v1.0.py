# coding=utf-8
import socket


def print_menu():
    print("请输入要执行的功能：1.发送数据 2.接收数据 3.退出")


def send_msg(udp_socket):
    send_data = input("请输入要发送的信息内容")
    send_addr = (input("请输入要发送到的IP地址"), int(input("请输入要发送到的端口")))
    udp_socket.sendto(send_data.encode("utf-8"), send_addr)


def recv_msg(udp_socket):
    recv_data, recv_addr = udp_socket.recvfrom(4096)
    print("接收到从IP:%s 端口:%s 发送来的消息：%s" % (str(recv_addr[0]), str(recv_addr[1]), recv_data.decode("utf-8")))


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", 7777))
    while True:
        print_menu()
        op = input("请选择：")
        if op == "1":
            send_msg(udp_socket)
        elif op == "2":
            recv_msg(udp_socket)
        elif op == "3":
            break
        else:
            print("输入错误，请重新输入")
            continue
    udp_socket.close()


if __name__ == '__main__':
    main()




