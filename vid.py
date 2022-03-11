poly_crc32_normal=0x104c11db7
crc32_table_normal=[]
for byte in range(256):
    operator=byte
    operator<<=24
    for bit in range(8):
        if (operator & 0x80000000) != 0:
            operator <<= 1
            operator ^= poly_crc32_normal
        else:
            operator <<= 1
    crc32_table_normal.append(operator)
def crc32_normal(line):
    var=0xffffffff
    for ch in line:
        operator=ord(ch)
        operator=int('{:08b}'.format(operator)[::-1],2)
        operator=operator^(var>>24)
        var=(crc32_table_normal[operator])^(var<<8)&0xffffffff
    var=int('{:032b}'.format(var)[::-1],2)
    return var^0xffffffff
print(hex(crc32_normal('123456789')))
