import random
import string


class GeneratorShortUrl:
    def getShortUrl(length=10):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
