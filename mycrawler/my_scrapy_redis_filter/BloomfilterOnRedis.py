# encoding=utf-8

from mycrawler.settings import BOT_NAME
from mycrawler.util.distributed_lock import dist_lock

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


class BloomFilter(object):
    def __init__(self, server, key, blockNum,k):
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [543, 460, 171, 876, 796, 607, 650, 81, 837, 545, 591, 946, 846, 521, 913, 636, 878, 735, 414, 372,
             344, 324, 223, 180, 327, 891, 798, 933, 493, 293, 836, 10, 6, 544, 924, 849, 438, 41, 862, 648, 338,
             465, 562, 693, 979, 52, 763, 103, 387, 374, 349, 94, 384, 680, 574, 480, 307, 580, 71, 535, 300, 53,
             481, 519, 644, 219, 686, 236, 424, 326, 244, 212, 909, 202, 951, 56, 812, 901, 926, 250, 507, 739, 371,
             63, 584, 154, 7, 284, 617, 332, 472, 140, 605, 262, 355, 526, 647, 923, 199, 518]
        self.server = server
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds[:k]:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        ret = True

        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        with dist_lock(BOT_NAME, self.server):
            for f in self.hashfunc:
                loc = f.hash(str_input)
                ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        with dist_lock(BOT_NAME, self.server):
            for f in self.hashfunc:
                loc = f.hash(str_input)
                self.server.setbit(name, loc, 1)
