#!/usr/bin/python3
# @Мартин.

import curses
import time
import random
import socket
import threading
import json
import hashlib
import argparse

SCREEN_WIDTH = 5
SCREEN_HEIGHT = 6
DEFAULT_PORT = 10011
clients = []

def handle_client(client_socket):
    while True:
        try:
            time.sleep(1)
        except:
            client_socket.close()
            clients.remove(client_socket)
            break

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"[INFO] Server started, listening on port {port}")
    
    while True:
        client_socket, addr = server.accept()
        print(f"[INFO] New connection from: {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def send_hash_to_clients(matrix):
    hash_list_str = json.dumps(matrix)
    for client in clients:
        try:
            client.send(hash_list_str.encode('utf-8'))
        except:
            client.close()
            clients.remove(client)

def game_main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(200)
    
    plane_x, plane_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 1
    bullets = []
    enemy_x, enemy_y = random.randint(0, SCREEN_WIDTH - 1), 0
    enemy_speed_counter, enemy_speed = 0, 5
    
    while True:
        key = stdscr.getch()
        screen_matrix = [[0] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]
        
        if key == curses.KEY_LEFT and plane_x > 0: plane_x -= 1
        elif key == curses.KEY_RIGHT and plane_x < SCREEN_WIDTH - 1: plane_x += 1
        elif key == ord(' ') and plane_y > 0: bullets.append([plane_y - 1, plane_x])
        
        bullets = [[y - 1, x] for y, x in bullets if y > 0]
        stdscr.clear()
        
        if enemy_y < SCREEN_HEIGHT:
            stdscr.addch(enemy_y, enemy_x, 'X')
            screen_matrix[enemy_y][enemy_x] = 1
        
        if enemy_y < SCREEN_HEIGHT and [enemy_y, enemy_x] in bullets:
            bullets.remove([enemy_y, enemy_x])
            enemy_x, enemy_y = random.randint(0, SCREEN_WIDTH - 1), 0
            
        stdscr.addch(plane_y, plane_x, '#')
        screen_matrix[plane_y][plane_x] = 1
        
        for bullet_y, bullet_x in bullets:
            if bullet_y < SCREEN_HEIGHT:
                stdscr.addch(bullet_y, bullet_x, '|')
                screen_matrix[bullet_y][bullet_x] = 1
        
        enemy_speed_counter += 1
        if enemy_speed_counter == enemy_speed:
            enemy_y += 1
            enemy_speed_counter = 0
        
        if enemy_y >= SCREEN_HEIGHT:
            enemy_x, enemy_y = random.randint(0, SCREEN_WIDTH - 1), 0
        
        stdscr.refresh()
        send_hash_to_clients(screen_matrix)
        time.sleep(0.1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=DEFAULT_PORT, help='Server Port')
    args = parser.parse_args()
    
    server_thread = threading.Thread(target=start_server, args=(args.port,))
    server_thread.daemon = True
    server_thread.start()
    
    curses.wrapper(game_main)

if __name__ == "__main__":
    main()
