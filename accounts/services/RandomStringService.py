import random, string

class RandomStringService():

    @staticmethod
    def generateRandomString(n):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
