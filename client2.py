import random
import socket

# Define the server's address and port
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12345

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
print("Connected to server...\n")

# Play the game for 13 rounds
CARD_VALUES = [str(i) for i in range(1, 14)]
suit = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
deck = [f"{value} of {s}" for value in CARD_VALUES for s in suit]
for round_num in range(1, 14):
    print(f"\nROUND {round_num}\n")
    server_card = client_socket.recv(1024).decode()
    print(f"Server card: ({server_card})\n")

    # Enter card for Client 2
    client_card = random.choice(deck)
    print(client_card)
    # deck.remove(client_card)
    client_socket.sendall(str(client_card).encode())

# Close the connection
# client_socket.close()
