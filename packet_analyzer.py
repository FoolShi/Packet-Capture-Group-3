from filter_packets import filter_packets
from packet_parser import parse_packets
from compute_metrics import compute_metrics

def main():
    nodes = ["Node1", "Node2", "Node3", "Node4"]

    for node in nodes:
            input = f"{node}.txt"
            output = f"{node}_filtered.txt"

            # Phase 1: filtering
            filter_packets(input, output)

            # Phase 2: parsing 
            packets = parse_packets(output)

            # Phase 3: compute metrics
            metrics = compute_metrics(packets)

            print(f"Metrics for {node}:")
            for key, value in metrics.items():
                print(f"{key}: {value}")
            print("\n")

if __name__ == "__main__":
    main()