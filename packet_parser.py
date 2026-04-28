import re

def parse_packets(filtered):
        packets = []

        with open(filtered, 'r') as file:
            for line in file:
                try:

                    match = re.search(
                    r"^\s*(\d+)\s+"                 # packet number
                    r"(\d+\.\d+)\s+"                # time
                    r"(\d+\.\d+\.\d+\.\d+)\s+"      # source IP
                    r"(\d+\.\d+\.\d+\.\d+)\s+"      # destination IP
                    r"ICMP\s+"
                    r"(\d+)\s+"                     # frame length
                    r"Echo \(ping\) (request|reply).*?"
                    r"seq=(\d+)",
                    line
                    )
                     
                    if not match:
                        continue

                    # Extracts the timestamp
                    # time_match = re.search(r"^(\d+\.\d+)", line)
                    time = float(match.group(2))

                    # Extracts the source and destination IPs
                    # ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+) -> (\d+\.\d+\.\d+\.\d+)", line)
                    src_ip = match.group(3)
                    des_ip = match.group(4)
                    length = int(match.group(5))
                    pkt_type = match.group(6)
                    seq = int(match.group(7))

                    # Determines the packets type
                    # if "request" in line:
                    #     type = "request"
                    # else:
                    #         type = "reply"

                    # Extracts the sequence num
                    # seq_match = re.search(r"seq=(\d+)", line)
                    # seq = int(seq_match.group(1)) if seq_match else None

                    # Extracts the frame length
                    # len_match = re.search(r"length (\d+)", line)
                    # len = int(len_match.group(1)) if len_match else None 

                    # Ethernet header 14 + IPv4 header 20 + ICMP header 8 = 42 bytes
                    payload = max(0, length - 42)

                    packets.append({
                            "time": time,
                            "src_ip": src_ip,
                            "des_ip": des_ip,
                            "type": pkt_type,
                            "seq": seq,
                            "length": length,
                            "payload": payload
                    })

                except Exception:
                     continue
                
        return packets