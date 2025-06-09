import socket

def serve_policy():
    policy_request = '<policy-file-request/>\x00'
    policy_response = """<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.adobe.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
    <allow-access-from domain="*" to-ports="12345"/>
</cross-domain-policy>\x00"""

    policy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    policy_server.bind(('0.0.0.0', 843))
    policy_server.listen(5)
    print("Policy server started, waiting for connections...")

    while True:
        client_socket, addr = policy_server.accept()
        print(f"Policy request from {addr}")
        data = client_socket.recv(1024).decode('utf-8')
        if data == policy_request:
            client_socket.sendall(policy_response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    serve_policy()