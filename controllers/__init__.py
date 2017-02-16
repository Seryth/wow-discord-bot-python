from controllers import clientController
from controllers import commandController
from const import TOKENS

def runClient():
    clientController.client.run(TOKENS.DEV_COL)