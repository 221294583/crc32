import copy
import zlib

'''
test_crc8=0x31
poly_crc8=0x11d
for bit in range(8):
    if (test_crc8&0x80)!=0:
        test_crc8<<=1
        test_crc8^=poly_crc8
    else:
        test_crc8<<=1
print(hex(test_crc8))
'''
test_crc32=0xf8
poly_crc32_normal=0x104c11db7

test_crc32<<=24
for bit in range(8):
    if (test_crc32&0x80000000)!=0:
        test_crc32<<=1
        test_crc32^=poly_crc32_normal
    else:
        test_crc32<<=1

crc32_table_normal=[]
for byte in range(256):
    operator=copy.copy(byte)
    operator<<=24
    for bit in range(8):
        if (operator & 0x80000000) != 0:
            operator <<= 1
            operator ^= poly_crc32_normal
        else:
            operator <<= 1
    crc32_table_normal.append(operator)
to_print_normal=list(map(hex,crc32_table_normal))

test_crc32=0x01
poly_crc32_recip=0x104c11db7
test_crc32=int('{:08b}'.format(test_crc32)[::-1],2)
test_crc32<<=24
for bit in range(8):
    if (test_crc32&0x80000000)!=0:
        test_crc32<<=1
        test_crc32^=poly_crc32_recip
    else:
        test_crc32<<=1
test_crc32=int('{:032b}'.format(test_crc32)[::-1],2)

crc32_table_recip=[]
for byte in range(256):
    operator=copy.copy(byte)
    operator=int('{:08b}'.format(operator)[::-1],2)
    operator<<=24
    for bit in range(8):
        if (operator&0x80000000)!=0:
            operator<<=1
            operator^=poly_crc32_recip
        else:
            operator<<=1
    operator=int('{:032b}'.format(operator)[::-1],2)
    crc32_table_recip.append(operator)
to_print_recip=list(map(hex,crc32_table_recip))
'''
file=open('crctable.txt','w')
for i in range(32):
    file.write(' '.join(to_print_normal[i*8:(i+1)*8]))
    file.write('\n')
file.write('\n')
for i in range(32):
    file.write(' '.join(to_print_recip[i*8:(i+1)*8]))
    file.write('\n')
file.close
'''
def crc32_recip(line):
    var=0xffffffff
    for ch in line:
        operator=ord(ch)
        operator=(operator^var)&0xff
        var=crc32_table_recip[operator]^(var>>8)
    return var^0xffffffff

print(hex(zlib.crc32('123456789'.encode('utf-8'))))
print(hex(crc32_recip('123456789')))

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

crc32_table_polyrev=[]
poly_rev=0xedb88320
for byte in range(256):
    operator=copy.copy(byte)
    for bit in range(8):
        if (operator&0x1)!=0:
            operator>>=1
            operator^=poly_rev
        else:
            operator>>=1
    crc32_table_polyrev.append(operator)
to_print_polyrev=list(map(hex,crc32_table_polyrev))

def crc32_polyrev(line):
    var=0xffffffff
    for ch in line:
        operator=ord(ch)
        operator=(operator^var)&0xff
        print(operator)
        var=crc32_table_recip[operator]^(var>>8)
    return var^0xffffffff

print(hex(crc32_polyrev('123456789')))