import hashlib

IS_DELETE = 1
NOT_DELETE = 0

# redis
TOKEN_CONNECT = 7  # 存储用户token

# 加密算法
HS256 = "HS256"
HASHES = {
    HS256: hashlib.sha256,
}