def assembler_bits_en_octets(chaine_bits):
    """
    transforme une chaine en bits en octets.
    Gere le padding (ajout de bits'0') pour que la longueur soit un multiple de 8.
    retourn : tuple(bytes , padding)
    """
    remplissage = (8-len (chaine_bits)%8)%8
    chaine_bits +='0'* remplissage 
    tableau_octets = bytearray()
    for i in range(0, len (chaine_bits),8):
        octet = chaine_bits [i:i+8]
        tableau_octets.append(int(octet,2))
        return bytes(tableau_octets),remplissage






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
  
