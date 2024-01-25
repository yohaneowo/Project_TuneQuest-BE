from passlib.hash import pbkdf2_sha256

hash = pbkdf2_sha256.hash("toomanysecrets")

print(pbkdf2_sha256.verify("toomanysecrets", hash))

print(pbkdf2_sha256.verify("test", hash))