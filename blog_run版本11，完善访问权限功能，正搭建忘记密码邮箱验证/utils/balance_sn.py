import random
from datetime import datetime


def sn_balance():
    sn = datetime.strftime(datetime.now(),'%Y%m%d%H%M%f')
    return sn+str(random.randint(1000,9999))
