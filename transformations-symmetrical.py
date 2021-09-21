import binascii

# turn text from hex to utf8
def hexToUtf8(text):
    text = binascii.unhexlify(text).decode('utf8')
    return text

# turn text from utf8 to hex
def utf8ToHex(text):
    text = binascii.hexlify(text.encode('utf8')).decode('utf8')
    return text

# xor function
def xor(num1, num2, in_code = 2):
    len1 = len(str(num1))
    num1 = int(num1, in_code)
    num2 = int(num2, in_code)

    num = str(bin(num1 ^ num2)[2:])

    num = fillZerosBeforeNumber(num, len1)

    return num

# filling zeros before number
def fillZerosBeforeNumber(num1, length):
    num1 = str(num1)
    if len(str(num1)) != length:
        for i in range(length - len(str(num1))):
            num1 = '0' + num1
    return num1

# filling zeros after number
def fillZerosAfterNumber(num1, length):
    num1 = str(num1)
    if len(str(num1)) != length:
        for i in range(length - len(str(num1))):
            num1 = num1 + '0'
    return num1

transformation_table = [
    [11, 7, 8, 15, 1, 13, 12, 6, 0, 5, 10, 9, 4, 3, 2, 14],
    [13, 12, 0, 1, 2, 9, 8, 15, 7, 10, 11, 14, 4, 5, 3, 6],
    [7, 5, 13, 6, 10, 14, 0, 1, 9, 2, 15, 8, 3, 4, 12, 11],
    [10, 9, 0, 4, 13, 2, 7, 15, 14, 1, 6, 11, 5, 12, 8, 3],
    [13, 1, 0, 4, 14, 6, 10, 15, 8, 3, 12, 7, 9, 11, 5, 2],
    [9, 4, 14, 2, 7, 13, 1, 8, 5, 15, 0, 11, 12, 6, 10, 3],
    [15, 6, 14, 13, 8, 10, 2, 0, 9, 12, 1, 7, 5, 11, 3, 4],
    [10, 6, 4, 2, 12, 13, 5, 15, 8, 14, 3, 7, 11, 0, 9, 1]
]

# conversion in Easy Overwrite Mode
def overwriteMode(bitNumberIn):
    bitNumberInOut = ''
    for i in range(8):
        num1 = bitNumberIn[i * 4: i * 4 + 4]
        num2 = bin(transformation_table[i][int(bitNumberIn[i * 4: i * 4 + 4], 2)])[2:]
        num2 = fillZerosBeforeNumber(num2, 4)

        bitNumberInOut += xor(num1, num2, 2)
    return bitNumberInOut

def transformation(numLeft, numRight, key):
    numLeftOut = numRight
    numRightOut = xor(numRight, key, 2)
    numRightOut = overwriteMode(numRightOut)
    numRightOut = xor(numRightOut, numLeft, 2)
    return numLeftOut, numRightOut

def chainOfTransformations(numLeft, numRight, key, move = 'straight'):
    if move == 'reverse':
        start = 31
        stop = 0
        step = -1
        last = 0
    else:
        start = 0
        stop = 31
        step = 1
        last = 31
    for i in range(start, stop, step):
        numLeft, numRight = transformation(numLeft, numRight, key[i])
    numRightLast = numRight
    numLeft, numRight = transformation(numLeft, numRight, key[last])
    return numRight + numRightLast

# convertation from base to base
def convertBase(num, toBase = 10, fromBase = 10):
    # converting to a decimal number
    if isinstance(num, str):
        n = int(num, fromBase)
    else:
        n = int(num)
    # converting a decimal number to the required number system
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < toBase:
        return alphabet[n]
    else:
        return convertBase(n // toBase, toBase) + alphabet[n % toBase]

# set key with right length
def transformKey(key):
    key = binascii.hexlify(key.encode('utf8')).decode('utf8')
    count = 64 - len(key) % 64
    while len(key) < 64:
        key += key
    return key[:64]

def cutKey(key):
    key = convertBase(key, 2, 16)
    keys = []
    for i in range(3):
        for j in range(8):
            keys.append(key[j * 32 : j * 32 + 32])
    for i in range(7, -1, -1):
        keys.append(key[i * 32 : i * 32 + 32])
    return keys

# encrypt from UTF8 text to HEX text with key
def encrypt(text, key):
    key = transformKey(key)
    key = cutKey(key)
    text = convertBase(utf8ToHex(text), toBase = 2, fromBase = 16)
    if len(text) % 8 != 0:
        text = fillZerosBeforeNumber(text, (len(text) // 8)  * 8 + 8)
    textArray = []
    textEncrypt = ''
    for i in range(len(text) // 64 + 1):
        textForAppend = text[i * 64 : i * 64 + 64]
        textForAppend = fillZerosAfterNumber(textForAppend, 64)
        textArray.append(textForAppend)
    for i in range(len(textArray)):
        textEncrypt += chainOfTransformations(textArray[i][:32], textArray[i][32:], key)
    textEncrypt = convertBase(textEncrypt, toBase = 16, fromBase = 2)
    return textEncrypt

# decrypt from HEX text to HEX text with key
def decrypt(text, key):
    key = transformKey(key)
    key = cutKey(key)
    text = convertBase(text, toBase = 2, fromBase = 16)
    if len(text) % 8 != 0:
        text = fillZerosBeforeNumber(text, (len(text) // 8)  * 8 + 8)
    textArray = []
    textDecrypt = ''
    if (len(text) // 64 * 64) != len(text):
        count = len(text) // 64 + 1
    else:
        count = len(text) // 64
    for i in range(count):
        textForAppend = text[i * 64 : i * 64 + 64]
        textForAppend = fillZerosAfterNumber(textForAppend, 64)
        textArray.append(textForAppend)
    for i in range(len(textArray)):
        textDecrypt += chainOfTransformations(textArray[i][:32], textArray[i][32:], key, move = 'reverse')
    textDecrypt = convertBase(textDecrypt, toBase = 16, fromBase = 2)
    return textDecrypt
