crc32_poly=0x104c11db7
crc32_table=[]
for operator in range(256):
    operator<<=24
    for byte in range(8):
        if (operator&0x80000000)!=0:
            operator<<=1
            operator^=crc32_poly
        else:
            operator<<=1
    crc32_table.append(operator)
def crc32(line):
    var=0xffffffff
    for character in line:
        operator=ord(character)
        operator=int('{:08b}'.format(operator)[::-1],2)
        operator=operator^(var>>24)
        var=(crc32_table[operator])^(var<<8)&0xffffffff
    var=int('{:032b}'.format(var)[::-1],2)
    return var^0xffffffff
print(hex(crc32('123456789')))
