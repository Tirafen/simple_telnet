import select
import socket

SERVER_ADDRESS = ('localhost', 8686)
MAX_CONNECTIONS = 10
INPUTS = list()
OUTPUTS = list()

f = open('records.txt', 'w')
f.write('Записи сервера:' + '\n')
f.close()


def get_non_blocking_server_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind(SERVER_ADDRESS)
    server.listen(MAX_CONNECTIONS)
    return server


def handle_readables(readables, server):
    for resource in readables:
        if resource is server:
            connection, client_address = resource.accept()
            connection.setblocking(0)
            INPUTS.append(connection)
            print("Новое подключение {address}".format(address=client_address))
        else:
            data = ""
            try:
                data = resource.recv(1024).decode("utf-8")

            except ConnectionResetError:
                pass

            if data:
                result = f"Спортсмен {data[0:4]} прошел отсечку {data[5:7]}, время {data[8:18]}, группа {data[21:23]}"
                if data[21:23] == '00':
                    print(result)
                    f = open('records.txt', 'a')
                    f.write(result + '\n')
                    f.close()
                else:
                    f = open('records.txt', 'a')
                    f.write(result + '\n')
                    f.close()
                if resource not in OUTPUTS:
                    OUTPUTS.append(resource)
            else:
                clear_resource(resource)


def clear_resource(resource):
    if resource in OUTPUTS:
        OUTPUTS.remove(resource)
    if resource in INPUTS:
        INPUTS.remove(resource)
    resource.close()

    print('Соединение закрыто')


def handle_writables(writables):
    for resource in writables:
        try:
            resource.send(bytes('Привет!', encoding='UTF-8'))
        except OSError:
            clear_resource(resource)


if __name__ == '__main__':
    server_socket = get_non_blocking_server_socket()
    INPUTS.append(server_socket)
    print("Сервер запущен, для остановки нажмите ctrl+c")

    try:
        while INPUTS:
            readables, writables, exceptional = select.select(INPUTS, OUTPUTS, INPUTS)
            handle_readables(readables, server_socket)
            handle_writables(writables)

    except KeyboardInterrupt:
        clear_resource(server_socket)
        print("Сервер остановлен")
