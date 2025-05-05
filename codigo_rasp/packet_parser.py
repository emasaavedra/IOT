
import struct # Libreria muy util para codificar y decodificar datos


"""

--- Packing en C ---



char * pack(int packet_id, float value_float, char * text) {
    char * packet = malloc(12 + strlen(text));
    memcpy(packet, &packet_id, 4);
    memcpy(packet + 4, &value_float, 4);
    memcpy(packet + 8, &largo_text, 4);
    memcpy(packet + 12, text, largo_text);
    return packet;
}

//Luego mandan el paquete por el socket


--- Unpacking en C ---


void unpack(char * packet) {
    int packet_id;
    float value_float;
    int largo_text;
    char * text;

    memcpy(&packet_id, packet, 4);
    memcpy(&value_float, packet + 4, 4);
    memcpy(&largo_text, packet + 8, 4);

    text = malloc(largo_text + 1); // +1 for the null-terminator
    if (text == NULL) {
        // Handle memory allocation failure
        return;
    }
    
    memcpy(text, packet + 12, largo_text);
    text[largo_text] = '\0'; // Null-terminate the string

    printf("Packet ID: %d\n", packet_id);
    printf("Float Value: %f\n", value_float);
    printf("Text: %s\n", text);

    free(text); 
}


"""


def pack(packet_id: int, value_float: float, text: str) -> bytes:
    largo_text = len(text)
    """
     '<' significa que se codifica en little-endian
     'i' significa que el primer dato es un entero de 4 bytes
     'f' significa que el segundo dato es un float de 4 bytes
     'i' significa que el tercer dato es un entero de 4 bytes
     '{}s'.format(largo_text) (ej: 10s para un string de largo 10) significa que el string tiene largo variable,

            Documentacion de struct: https://docs.python.org/3/library/struct.html

    """
    return struct.pack('<ifi{}s'.format(largo_text), packet_id, value_float, largo_text, text.encode('utf-8'))


def unpack(packet: bytes) -> list:
    packet_id,value_float,largo_text = struct.unpack('<ifi', packet[:12])
    text = struct.unpack('<{}s'.format(largo_text), packet[12:])[0].decode('utf-8')
    return [packet_id, value_float, text]

# Protocol pack-format map
pformat = [
    '<B',
    '<BI',
    '<BIBIBf',
    '<BIBIBffffffff',
    '<2000f2000f2000f2000f2000f2000f',
]

# Protocol data-key map
pkey = [
    ['bat_level'],
    ['bat_level', 'timestamp'],
    ['bat_level', 'timestamp', 'temp', 'press', 'hum', 'co'],
    ['bat_level', 'timestamp', 'temp', 'press', 'hum', 'co', 'rms', 'amp_x', 'frec_x', 'amp_y', 'frec_y', 'amp_z', 'frec_z'],
    ['acc_x', 'acc_y', 'acc_z', 'rgyr_x', 'rgyr_y', 'rgyr_z']
]

# pack sizes
psizes = [
    [1],
    [1, 4],
    [1, 4, 1, 4, 1, 4],
    [1, 4, 1, 4, 1, 4, 4, 4, 4, 4, 4, 4, 4],
]

# unpack for protocol 0 to 3
def unpack03(body: bytes, protocol: int) -> dict:
    raw_data = struct.unpack(pformat[protocol], body)
    sizes = psizes[protocol]
    data = {}
    for i, key in enumerate(pkey[protocol]):
        if sizes[i] == 1:
            data[key] = raw_data[i]
        else:
            start = sum(sizes[:i])
            end = start + sizes[i]
            data[key] = raw_data[start:end]
    return data

# unpack for protocol 4
def unpack4(body: bytes) -> dict:
    data = struct.unpack(pformat[2], body[:15])
    # append vectors as bytes
    vector_size = 2000 * 4
    for i, key in enumerate(pkey[4]):
        start = 15 + i * vector_size
        end = start + vector_size
        data[key] = body[start:end]
    return data

# header and body parsing
def parse_packet(packet: bytes) -> list:
    # header data
    header = packet[:12]
    unpacked_header = struct.unpack('<2B6BBBH', header)

    # header data
    header_data = {
        'id': bytes(unpacked_header[0:2]).decode('ascii'),
        'mac': ':'.join(f'{b:02x}' for b in unpacked_header[2:8]),
        'tl': unpacked_header[8],
        'protocol': unpacked_header[9],
        'length': unpacked_header[10:][0],
    }

    # body data
    body = packet[12:]
    p = int(header_data['protocol'])
    body_raw_data = None
    if p in (0, 1, 2, 3, 4):
        return { 
            'header': header_data,
            # 'body': unpack03(body, p) if p in (0, 1, 2, 3) else unpack4(body)
        }
    else:
        raise ValueError("Invalid protocol number")
        
    


if __name__ == "__main__":
    mensage = pack(1, 3.20, "Hola mundo")
    print(mensage)
    print(unpack(mensage))



