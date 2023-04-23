import random
import socket

# Define the server's address and port
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12345

# Define the number of rounds in the game
NUM_ROUNDS = 13

# Define the possible card values and suits
CARD_VALUES = [str(i) for i in range(1, 14)]
CARD_SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Create a deck of cards
DECK = [f"{value} of {suit}" for value in CARD_VALUES for suit in CARD_SUITS]

# Create a dictionary to store scores
scores = {}

# Create a list to store client sockets
client_sockets = []

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
server_socket.listen(3)  # Accept up to 3 client connections

print("Server is ready to accept connections...\n")

# Accept connections from clients
for i in range(3):
    client_socket, client_address = server_socket.accept()
    print(f"Client {i + 1} connected from {client_address}")
    client_sockets.append(client_socket)
    scores[client_socket] = 0  # Initialize score for this client to 0

print("All clients connected. Starting the game...\n")

# Play the game for the specified number of rounds
for round_num in range(1, NUM_ROUNDS + 1):
    print(f"\nROUND {round_num}\n")

    # Choose a server card
    server_card = random.choice(DECK)
    print(f"Server card: {server_card}\n")


    # Send the server card to all clients
    for client_socket in client_sockets:
        client_socket.sendall(server_card.encode())

    # Receive and process client cards
    client_cards = []

    for client_socket in client_sockets:
        client_card = client_socket.recv(1024).decode()
        print(f"Client {client_sockets.index(client_socket) + 1} card: {client_card}")
        client_cards.append(client_card)

        # Determine the winner(s) of the round
    card_values = {card: CARD_VALUES.index(card.split()[0]) for card in client_cards}
    card_values[server_card] = CARD_VALUES.index(server_card.split()[0])

    max_value = max(card_values.values())
    winners = [card for card, value in card_values.items() if value == max_value]
    if server_card in winners:
        winners.append(server_card)

    # Update scores based on the winner(s)
    if len(winners) == 1:
        winner = winners[0]
        winner_index = client_cards.index(winner)
        scores[client_sockets[winner_index]] += 5
        print(f"Client {winner_index + 1} wins this round!\n")
    elif len(winners) == 2:
        scores[client_sockets[0]] += 10
        scores[client_sockets[1]] += 10
        print("It's a tie between two clients!\n")
    else:
        for client_socket in client_sockets:
            if client_cards[client_sockets.index(client_socket)] in winners:
                scores[client_socket] += 2

# Print the final scores
for client_socket in client_sockets:
    score = scores[client_socket]
    client_socket.sendall(f"Final score: {score}".encode())
    print(f"Client {client_sockets.index(client_socket) + 1} final score: {score}")

# Close all client sockets and the server socket
for client_socket in client_sockets:
    client_socket.close()

server_socket.close()
