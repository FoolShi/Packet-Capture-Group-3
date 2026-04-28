from filter_packets import filter_packets
from packet_parser import parse_packets
from compute_metrics import compute_metrics

def main():
    nodes = {
        "Node1": "192.168.100.1", 
        "Node2": "192.168.100.2",
        "Node3": "192.168.200.1",
        "Node4": "192.168.200.2"
        }

    for node, node_ip in nodes.items():
            input_file = f"{node}.txt"
            output_file = f"{node}_filtered.txt"

            # Phase 1: filtering
            filter_packets(input_file, output_file)

            # Phase 2: parsing 
            packets = parse_packets(output_file)

            # Phase 3: compute metrics
            metrics = compute_metrics(packets, node_ip)

            print(f"Metrics for {node}:")
            for key, value in metrics.items():
                print(f"{key}: {value}")
            print()

if __name__ == "__main__":
    main()