def compute_metrics(packets, node_ip):
    metrics = {
        "requests_sent": 0,
        "requests_recieved": 0,
        "replies_sent": 0,
        "replies_recieved": 0,
        "total_req_bytes_sent": 0,
        "total_req_bytes_recieved": 0,
        "total_req_data_sent": 0,
        "total_req_data_recieved": 0,
        "avg_rtt": 0,
        "throughput": 0,
        "goodput": 0,
        "avg_reply_delay": 0
    }

    # Dictionaries to match request/reply pairs
    requests_sent = {}
    requests_recieved = {}

    total_rtt = 0
    rtt_count = 0

    total_reply_delay = 0
    reply_delay_count = 0

    for pkt in packets:
        src = pkt["src_ip"] 
        dst = pkt["des_ip"]
        seq = pkt["seq"]

        #Ignore packets that do not involve this node
        if src != node_ip and dst != node_ip:
            continue

        key = (src, dst, seq)

        if pkt["type"] == "request":
            if src == node_ip:
                metrics["requests_sent"] += 1
                metrics["total_req_bytes_sent"] += pkt["length"]
                metrics["total_req_data_sent"] += pkt["payload"]

                requests_sent[key] = pkt

            elif dst == node_ip:
                metrics["requests_recieved"] += 1
                metrics["total_req_bytes_recieved"] += pkt["length"]
                metrics["total_req_data_recieved"] += pkt["payload"]

                requests_recieved[key] = pkt

        elif pkt["type"] == "reply":
            reverse_key = (dst, src, seq)

            # RTT
            if dst == node_ip and reverse_key in requests_sent:
                metrics["replies_recieved"] += 1

                request_pkt = requests_sent[reverse_key]

                rtt = pkt["time"] - request_pkt["time"]

                if rtt > 0:
                    total_rtt += rtt
                    rtt_count += 1

            # Reply delay
            elif src == node_ip:
                metrics["replies_sent"] += 1

                if reverse_key in requests_recieved:
                    request_pkt = requests_recieved[reverse_key]
                    reply_delay = pkt["time"] - request_pkt["time"]

                    if reply_delay > 0:
                        total_reply_delay += reply_delay
                        reply_delay_count += 1
    
    if rtt_count > 0:
        # seconds -> milliseconds
        metrics["avg_rtt"] = (total_rtt / rtt_count) * 1000

        # bytes/sec -> KB/sec
        metrics["throughput"] = (metrics["total_req_bytes_sent"] / 1000) / total_rtt
        metrics["goodput"] = (metrics["total_req_data_sent"] / 1000) / total_rtt

    if reply_delay_count > 0:
        # seconds -> microseconds
        metrics["avg_reply_delay"] = (total_reply_delay / reply_delay_count) * 1_000_000
    
    return metrics