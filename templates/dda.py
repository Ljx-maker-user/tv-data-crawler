# 直接执行
from base64 import b64decode
from Crypto.Util.number import long_to_bytes, inverse

n = 2140324650240744961264423072839333563008614715144755017797754920881418023447140136643345519095804679610992851872470914587687396261921557363047454770520805119056493106687691590019759405693457452230589325976697471681738069364894699871578494975937497937
e = 65537
p = 33372027594978156556226010605355114227940760344767554666784520987023841729210037080257448673296881877565718986258036932062711
q = 64135289477071580278790190170577389084825014742943447208116859632024532344630238623598752668347708737661925585694639798853367

table1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*+,-./:;?@+-"
table2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

a = 'aK-Au+WTT+yYkIHs/noPUif+yNryFQLW;bN+/eNdbu/OvW*ctI:xTGqM-zZzaYl-Lmj?nEctJBgp@@pT-kXrKtU*sEIrtJppF-UHDhdGAIfZlwFnEYkb?qiEMU+kLApumfjjWTTw-YG='

def correct_mapping(s: str) -> str:
    result = []
    for ch in s:
        idx = table1.find(ch)
        if idx != -1:
            result.append(table2[idx])
        else:
            result.append(ch)
    return "".join(result)

b64_str = correct_mapping(a)
print(f"Base64字符串: {b64_str}")
print(f"Base64长度: {len(b64_str)}")

# Base64 解码
cipher_bytes = b64decode(b64_str)
print(f"解码后字节长度: {len(cipher_bytes)}")

c = int.from_bytes(cipher_bytes, 'big')
print(f"密文整数c的长度: {c.bit_length()} bits")

# RSA 解密
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, n)

flag_bytes = long_to_bytes(m)
print(f"解密后字节: {flag_bytes}")

# 尝试解码
try:
    flag = flag_bytes.decode('utf-8')
    print(f"Flag: {flag}")
except:
    print(f"十六进制: {flag_bytes.hex()}")