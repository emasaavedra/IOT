import socket
import struct
import threading
from packet_parser import parse_packet

HOST = '0.0.0.0'  # Escucha en todas las interfaces disponibles
PORT = 8081       # Puerto en el que se escucha

# def handle_client(conn, addr):
#     with conn:
#         data = conn.recv(1024)
#         if not data or data == b'':
#             print("No se recibió ningún dato.")
#         # Si se recibe ? enviar configuracion
#         elif data == b'?':
#             print("Recibido: ", data.decode('utf-8'))
#             layer, protocol = 0, 0
#             conn.send(struct.pack('<BB', layer, protocol))  # Respuestas como 2 bytes
#         else:
#             print("Recibido: ", data.decode('utf-8'))


def socket_TCP():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print("El servidor está esperando conexiones en el puerto", PORT)

        while True:
            conn, addr = s.accept()  # Espera una conexión

            # Creacion de hilos para manejar multiples clientes
            # client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            # client_thread.start()
            with conn:
                print('Conectado por', addr)
                data = conn.recv(1024)  # Recibe hasta 1024 bytes del cliente
                if data is None or data == b'':
                    print("No se recibió ningún dato.")
                    continue
                # Si se recibe ? enviar configuracion
                elif data == b'?':
                    print("Recibido: ", data.decode('utf-8'))
                    layer, protocol = 0, 0
                    conn.send(struct.pack('<BB', layer, protocol))  #  Respuestas como 2 bytes

                data = conn.recv(1024)
                if not data or data == b'':
                    print("No se recibió ningún dato.")
                    continue
                print("Recibido: ", data)
                parsed_data = parse_packet(data)
                print("Datos recibidos y analizados")

                print(parsed_data['header'])

socket_TCP()