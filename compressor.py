def assemble_bits_to_bytes(bit_string):
    """
    transforme une chaine en bits en octets.
    Gere le padding (ajout de bits'0') pour que la longueur soit un multiple de 8.
    retourn : tuple(bytes , padding)
    """
    padding = (8-len (bit_string)%8)%8
    bit_string +='0'*padding
    byte_array = bytearray()
    for i in range(0, len (bit_string),8):
        byte = bit_string [i:i+8]
        byte_array.append(int(byte,2))
        return bytes(byte_array),padding






def compress_file(input_path ,output_path , huffman_code):
    """lit un fichier source en binaire , 
    remplace chaque code Huffman, 
    et construit une longue chaine de bits
    """
    bit_string = ""
    
    with open (input_path , 'rb') as f:
        byte = f.read (1)
        while byte :
            bit_string += huffman_code[byte]
        byte = f. read(1)
        
        return bit_string






def while_compression_file(output_path,byte_data, padding):
    """
    ecrit les données compressées dans un fichier binaire .
    le premier octet stocke le padding.
    """
    
    with open (output_path,'wb') as f:
        f.write(bytes([padding]))
        f.write(byte_data) 
  
