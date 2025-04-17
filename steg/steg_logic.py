from bitstring import BitArray

def embed_message(carrier_file, message_file, output_file, start_bit, l):
    with open(carrier_file, 'rb') as f:
        carrier_data = bytearray(f.read())
    with open(message_file, 'rb') as f:
        message_bits = BitArray(f.read()).bin
    bit_index = start_bit
    for bit in message_bits:
        byte_pos = bit_index // 8
        bit_pos = 7 - (bit_index % 8)
        carrier_data[byte_pos] &= ~(1 << bit_pos)
        carrier_data[byte_pos] |= (int(bit) << bit_pos)
        bit_index += l
    with open(output_file, 'wb') as f:
        f.write(carrier_data)
