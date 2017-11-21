# coding=utf-8
# 上面这行代码为整个文件指定了utf-8的编码格式

# 导入了socket套接字模块用于底层通信
import socket

# 导入了re正则模块用于匹配用户输入路径
import re


# 定义一个专门用于处理客户端请求的函数，传入刚刚获得的客户端套接字参数
def client_handler(client_socket):
    # 使用客户端套接字的recv方法接收客户端发送过来的数据，参数为一次接收的最大字节长度
    data = client_socket.recv(4096)
    # 判断数据是否存在
    if not data:
        # 如果不存在则证明客户端已经关闭连接，打印结果
        print("客户端已断开连接")
        # 关闭对应的客户端套接字
        client_socket.close()
        # 使用return终止函数
        return
    # 若数据存在对数据进行解码
    str_data = data.decode("utf-8")
    # 将拿到的数据按照"\r\n"切割成行
    data_list = str_data.split("\r\n")
    """请求行
       空行"""
    # 拿到第一行即请求行[0]
    request_line = data_list[0]
    # GET /path/a/b/index.html HTTP/1.1   正则匹配路径
    result = re.match(r"\w+\s+(\S+)", request_line)
    # 判断正则结果是否存在
    if not result:
        # 如果正则结果不存在，则关闭连接
        client_socket.close()
        # 结果不存在，终止函数
        return
    # 拿到正则结果的第一个分组即相对路径，保存为变量
    path_info = result.group(1)
    # 判断值是否为/根目录
    if path_info == "/":
        # 若请求目录为/根目录则自动跳转至/index.html
        path_info = "/index.html"
    # 尝试打开文件，使用异常处理
    try:
        # 以rb方式打开文件，名称为"static"和刚刚相对路径的字符串拼接
        file = open("static" + path_info, "rb")
        # 读取文件数据并保存
        file_data = file.read()
        # 关闭文件
        file.close()
    # 遇到异常时的处理
    except Exception as e:
        # 目录不存在，返回404错误页面的响应头  格式为：协议 状态码 状态说明\r\n
        response_data = "HTTP/1.1 404 Not Found\r\n"
        # 为响应数据增加\r\n空行
        response_data += "\r\n"
        # 为响应数据增加响应体数据
        response_data += "Error: 404"
        # 发送响应数据，记得要编码
        client_socket.sendall(response_data.encode("utf-8"))
    # 请求目录存在（即正常）时的操作
    else:
        # 构造200成功响应头
        response_data = "HTTP/1.1 200 OK\r\n"
        # 添加空行
        response_data += "\r\n"
        # 将刚刚文件读取到的数据保存为响应体数据变量
        response_body = file_data
        # 发送响应数据（编码后的响应行+空行+刚刚得到的响应体（以二进制打开文件并读取保存，故次数无需再编码））
        client_socket.sendall(response_data.encode("utf-8") + response_body)
    # 下一步操作（无论是否抛出异常）
    finally:
        # 关闭这个客户端套接字
        client_socket.close()


# 定义主函数
def main():
    # 创建服务器套接字，AF_INET ----> IPv4   SOCK_STREAM ----> TCP协议
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置socket套接字的地址重用
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 为socket套接字绑定IP及端口
    tcp_socket.bind(("", 8800))
    # 将服务器套接字转为被动监听套接字，缓存区为经验值128
    tcp_socket.listen(128)
    # 循环处理客户端的请求
    while True:
        # 服务器套接字使用accept方法接收到两个参数，分别为客户端套接字和客户端地址
        client_socket, client_addr = tcp_socket.accept()
        # 打印请求服务的客户端地址（IP及端口号）
        print("接收到来自%s的请求" % str(client_addr))
        # 调用函数专门处理客户端的服务请求，将刚刚获得的客户端套接字作为参数传入
        client_handler(client_socket)


# 主函数命名
if __name__ == '__main__':
    # 运行主函数
    main()



