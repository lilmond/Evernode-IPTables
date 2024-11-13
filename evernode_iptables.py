import subprocess
import os

def get_vmbr0_inet():
    output = subprocess.check_output(["ifconfig", "vmbr0"])

    return output.decode().splitlines()[1].strip().split(" ")[1]

def intput(text: str):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print(f"Please enter a valid int value.\n")
            continue

def main():
    ovh_ip = get_vmbr0_inet()

    print(f"Please make sure your OVH IP is correct before proceeding.\nOVH IP: {ovh_ip}\n")

    vps_ip = input("VPS IP: ").strip()
    peer_port = intput("Peer Port: ")
    user_port = intput("User Port: ")
    tcp_port = intput("General TCP Port: ")
    udp_port = intput("General UDP Port: ")

    print(f"\nPlease verify if these are the ports that you want to use for your Evernode.")
    print(f"Peer Port: {peer_port} - {peer_port + 7}")
    print(f"User Port: {user_port} - {user_port + 7}")
    print(f"General TCP Port: {tcp_port} - {tcp_port + 13}")
    print(f"General UDP Port: {udp_port} - {udp_port + 13}\n")

    while True:
        verify = input("Set IPTable rules? [Y/n]: ").lower()

        if not verify in ["y", "n"]:
            print(f"\"y\" or \"n\" expected.\n")
            continue

        break

    if not verify == "y":
        print(f"\nCanceled")
        exit()

    os.system(f"""iptables -t nat -A POSTROUTING -d {vps_ip} -p tcp --dport {peer_port}:{peer_port + 7} -j SNAT --to-source {ovh_ip}
iptables -t nat -A POSTROUTING -d {vps_ip} -p tcp --dport {user_port}:{user_port + 7} -j SNAT --to-source {ovh_ip}
iptables -t nat -A POSTROUTING -d {vps_ip} -p tcp --dport {tcp_port}:{tcp_port + 13} -j SNAT --to-source {ovh_ip}
iptables -t nat -A POSTROUTING -d {vps_ip} -p udp --dport {udp_port}:{udp_port + 13} -j SNAT --to-source {ovh_ip}

iptables -t nat -A PREROUTING -d {ovh_ip} -p tcp --dport {peer_port}:{peer_port + 7} -j DNAT --to-destination {vps_ip}
iptables -t nat -A PREROUTING -d {ovh_ip} -p tcp --dport {user_port}:{user_port + 7} -j DNAT --to-destination {vps_ip}
iptables -t nat -A PREROUTING -d {ovh_ip} -p tcp --dport {tcp_port}:{tcp_port + 13} -j DNAT --to-destination {vps_ip}
iptables -t nat -A PREROUTING -d {ovh_ip} -p udp --dport {udp_port}:{udp_port + 13} -j DNAT --to-destination {vps_ip}""")

    print(f"\nIPTable rules have been set.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
