import random
from datetime import datetime


def sn_order():
    sn = datetime.strftime(datetime.now(),'%Y%m%d%H%M%f')
    list1 = [chr(i) for i in range(65,91)]
    list1 += [chr(i) for i in range(97,123)]
    for j in range(4):
        sn += random.choice(list1)
    return sn+str(random.randint(10000,99999))
