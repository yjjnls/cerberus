def MD5(fileMd5):
    import hashlib
    md5_value = hashlib.md5()
    with open(fileMd5,'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5_value.update(data)
    return md5_value.hexdigest()

