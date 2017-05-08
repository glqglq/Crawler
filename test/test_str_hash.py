# encoding=utf-8

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        lenth = len(value)
        for i in range(lenth):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret

print SimpleHash(1 << 31,59).hash('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
