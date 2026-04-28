def filter_packets(input, output):
    # Read through raw packet data
    # ONLY captures IMCP recho requests/replys into output file 
    with open(input, 'r') as infile, open(output, 'w') as outfile:
            for line in infile:
                  if "ICMP" in line and (
                        "Echo (ping) request" in line or 
                        "Echo (ping) reply" in line
                        ):
                            outfile.write(line)
