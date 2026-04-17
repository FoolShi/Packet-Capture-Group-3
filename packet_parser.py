import re

def parse_packets(filtered):
        packets = []
        with open(filtered, 'r') as file:
            for line in file:
                try:
                    # Extracts the timestamp
                    time_match = re.search(r"^(\d+\.\d+)", line)
                    time = float(time_match.group(1)) if time_match else 0

                    # Extracts the source and destination IPs
                    ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+) -> (\d+\.\d+\.\d+\.\d+)", line)
                    src_ip = ip_match.group(1) if ip_match else None 
                    des_ip = ip_match.group(2) if ip_match else None

                    # Determines the packets type
                    if "request" in line:
                        type = "request"
                    else:
                            type = "reply"

                    # Extracts the sequence num
                    seq_match = re.search(r"seq=(\d+)", line)
                    seq = int(seq_match.group(1)) if seq_match else None

                    # Extracts the frame length
                    len_match = re.search(r"length (\d+)", line)
                    len = int(len_match.group(1)) if len_match else None 

                    # Typical payload size 32-bits for ping
                    payload = 32

                    packets.append({
                            "time": time,
                            "src_ip": src_ip,
                            "des_ip": des_ip,
                            "type": type,
                            "seq": seq,
                            "length": len,
                            "payload": payload
                    })
                except Exception:
                     continue
                
        return packets