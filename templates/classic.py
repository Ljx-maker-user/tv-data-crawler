import codecs

# 原字符串（注意：¥ 和 § 不是标准 ASCII，这里我用它们的 Unicode 码点）
# 但古典密码一般用 ASCII，我先假设它们是某些符号的显示问题，用 '&' 和 '$' 代替常见情况。
# 如果不行，再尝试忽略或不同替换。

ciphers = [
    ("[aq Y 3 ¥ § A>-<<OAV 8:", "original"),
    ("[aq Y 3 & $ A>-<<OAV 8:", "replace_¥§_with_&$"),
    ("[aq Y 3 / + A>-<<OAV 8:", "replace_¥§_with_/+"),
]

for s, desc in ciphers:
    print(f"\n=== 测试: {desc} ===")
    print(f"原文: {s}")

    # 1. ROT47
    def rot47(text):
        res = []
        for c in text:
            o = ord(c)
            if 33 <= o <= 126:
                res.append(chr(33 + ((o - 33) - 47) % 94))
            else:
                res.append(c)
        return ''.join(res)
    r47 = rot47(s)
    print(f"ROT47: {r47}")
    if 'flag' in r47.lower():
        print(f"   --> 发现 flag 字样!")

    # 2. ROT13
    r13 = codecs.encode(s, 'rot_13')
    print(f"ROT13: {r13}")

    # 3. Atbash (只处理字母)
    def atbash(text):
        res = []
        for c in text:
            if 'a' <= c <= 'z':
                res.append(chr(ord('z') - (ord(c) - ord('a'))))
            elif 'A' <= c <= 'Z':
                res.append(chr(ord('Z') - (ord(c) - ord('A'))))
            else:
                res.append(c)
        return ''.join(res)
    ab = atbash(s)
    print(f"Atbash: {ab}")

    # 4. 凯撒 1-25
    for shift in range(1, 26):
        dec = []
        for c in s:
            if 'a' <= c <= 'z':
                dec.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            elif 'A' <= c <= 'Z':
                dec.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            else:
                dec.append(c)
        res = ''.join(dec)
        if 'flag' in res.lower():
            print(f"凯撒 shift {shift}: {res}   --> 发现 flag 字样!")