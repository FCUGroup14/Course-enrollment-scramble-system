import secrets
#生成一個長度為64 位的隨機 session key
session_key =secrets.token_hex(32)  # 32 bytes= 64 characters in hexadecimal
print(session_key)