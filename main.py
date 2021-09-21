tr = __import__('transformations-symmetrical')

# set text and convert it to HEX
text = 'hello'
print('textDefault: ', tr.utf8ToHex(text).upper())

# get encrypted text in HEX format
textEncrypt = tr.encrypt(text, 'mypassword')
print('textEncrypt: ', textEncrypt)

# decrypt encrypted text in HEX format
textDecrypt = tr.decrypt(textEncrypt, 'mypassword')
print('textDecrypt: ', textDecrypt)
print('\ntextDecryptUTF8: ', tr.hexToUtf8(textDecrypt))