from struct import unpack, pack
import random


# desempaquetar un 3 arreglos de bytes que vengan en formato  2000f2000f2000f
# paquete original:
pack3 = b''
for i in range(3):
    raw = []
    for j in range(10):
        random_float = random.uniform(0, 1)
        pack3 += pack('<f', random_float)
        raw.append(random_float)
    # print(raw)

# unpack 3 arrays separados
unpacked = unpack('<30f', pack3)
print(unpacked[0])