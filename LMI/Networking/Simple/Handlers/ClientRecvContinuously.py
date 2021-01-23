def handle_client(client, addr, trackClients=None):
    print(f"Connection established with {addr}")
    request = None
    if trackClients:
        trackClients[addr] = client
    blanks = 0
    try:
        while request != 'quit' and client:
            request = client.recv(512).decode('utf-8')
            if request:
                print(f"{addr} ==> {request}")
                blanks = 0
            else:
                blanks += 1
            if blanks == 1000:
                print(f"{addr} has disconnected")
                break
    except Exception as e:
        print(e)
    if trackClients:
        del trackClients[addr]
