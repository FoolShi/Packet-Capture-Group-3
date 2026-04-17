def compute_metrics(packets):
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
    requests = {}
    replys = {}

    total_rtt = 0
    rtt_count = 0
    total_reply_delay = 0
    reply_delay_count = 0

    for pkt in packets:
        key = (pkt["src_ip"], pkt["des_ip"]), pkt["seq"]
        if pkt["type"] == "request":
            metrics["replies_sent"] += 1
            metrics["total_req_bytes_sent"] += pkt["length"]
            metrics["total_req_data_sent"] += pkt["payload"]

            requests[key] = pkt
        else:
            metrics["replies_recieved"] += 1
            reverse_key = (pkt["des_ip"], pkt["src_ip"], pkt["seq"])
            if reverse_key in requests:
                request_pkt = requests[reverse_key]
                rtt = pkt["time"] - request_pkt["time"]
                total_rtt += rtt
                rtt_count += 1
    
    if rtt_count > 0:
        metrics["avg_rtt"] = total_rtt / rtt_count
        metrics["throughput"] = metrics["total_req_bytes_sent"] / total_rtt
        metrics["goodput"] = metrics["total_req_data_sent"] / total_rtt
        
    return metrics