import random
random.seed(0)

def makeTransaction(maxValue=3):
    # This will create valid transactions in the range of (1,maxValue)
    sign      = int(random.getrandbits(1))*2 - 1   # This will randomly choose -1 or 1
    amount    = random.randint(1,maxValue)
    alicePays = sign * amount
    bobPays   = -1 * alicePays
    # By construction, this will always return transactions that respect the conservation of tokens.
    # However, note that we have not done anything to check whether these overdraft an account
    return {u'Alice':alicePays,u'Bob':bobPays}


def updateState(txn, state):
    # Inputs: txn, state: dictionaries keyed with account names, holding numeric values for transfer amount (txn) or account balance (state)
    # Returns: Updated state, with additional users added to state if necessary
    # NOTE: This does not not validate the transaction- just updates the state!
    
    # If the transaction is valid, then update the state
    state = state.copy() # As dictionaries are mutable, let's avoid any confusion by creating a working copy of the data.
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state

def isValidTxn(txn,state):
    # Assume that the transaction is a dictionary keyed by account names

    # Check that the sum of the deposits and withdrawals is 0
    if sum(txn.values()) is not 0:
        return (False, 'transaction sum isn\'t zero')
    
    # Check that the transaction does not cause an overdraft
    for key in txn.keys():
        if key in state.keys(): 
            acctBalance = state[key]
            print(key,acctBalance)
        else:
            acctBalance = 0
        if (acctBalance + txn[key]) < 0:
            return (False, 'cause the overdraft')
    
    return True

if __name__ == "__main__":
	#txnBuffer = [makeTransaction() for i in range(30)]
	#print(txnBuffer)
	state = {u'Alice':5,u'Bob':5}
	print(isValidTxn({u'Alice': -3, u'Bob': 3},state))  # Basic transaction- this works great!
	print(isValidTxn({u'Alice': -4, u'Bob': 3},state))  # But we can't create or destroy tokens!
	print(isValidTxn({u'Alice': -6, u'Bob': 6},state))  # We also can't overdraft our account.
	print(isValidTxn({u'Alice': -4, u'Bob': 2,'Lisa':2},state)) # Creating new users is valid
	print(isValidTxn({u'Alice': -4, u'Bob': 3,'Lisa':2},state)) # But the same rules still apply!