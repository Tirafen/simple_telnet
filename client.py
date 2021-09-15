import telnetlib
tn_ip = "localhost"
tn_port = "8686"


def telnet():
    try:
        tn = telnetlib.Telnet(tn_ip, tn_port, 15)

    except:
        print("Unable to connect to Telnet server: " + tn_ip)
        return

    finally:
        tn.set_debuglevel(100)
        while True:
            print("Введите данные в формате BBBB NN HH:MM:SS.zhq GG")
            tn.write(input().encode("utf-8"))

telnet()