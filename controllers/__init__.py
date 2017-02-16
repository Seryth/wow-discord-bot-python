from controllers import clientController
from controllers import commandController
from controllers import infoController
from const import TOKENS


def runClient():
    try:
        clientController.client.run(TOKENS.DEV_MBL)
    except:
        print("--------------\nno valid token\n--------------")