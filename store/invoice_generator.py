import string
import random
import hashlib


def generateinvoice():
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
    minlength = 10
    maxlength = 25
    length = random.randint(minlength, maxlength)
    med = ''.join(random.choice(charset) for _ in range(length)).encode('utf-8')
    return hashlib.md5(med).hexdigest()
