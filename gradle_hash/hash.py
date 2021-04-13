from hashlib import md5
import sys


def baseN(num, b): return ((num == 0) and "0") or (
    baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def hash(u): return baseN(int(md5(u.encode('utf-8')).hexdigest(), 16), 36)


if __name__ == '__main__':
    print(hash(sys.argv[1]))
