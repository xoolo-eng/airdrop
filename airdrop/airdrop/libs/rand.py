def rand(size_chars):
    with open("/dev/urandom", "rb") as file:
        return file.read(size_chars).hex()


if __name__ == '__main__':
    print(rand(35))
