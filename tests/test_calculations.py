from app.calculation import add, subtract, multiply, divide, BankAccount, InsuficientFunds
import pytest 

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100)

@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),
    (7,1,8),
    (12,4,16)
]) 
def test_add(num1, num2, expected):
    print('testing add function...')
    sum = add(num1,num2)
    assert sum == expected
    

def test_subtract():
    assert subtract(5,4) == 1


def test_multiply():
    assert multiply(5,4) == 20

def test_divide():
    assert divide(20,4) == 5

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100
        

def test_starting_balance(zero_bank_account):
    assert zero_bank_account.balance == 0 


#pytest tests/test_calculations.py -v
def test_deposit(zero_bank_account):
    bank_account = zero_bank_account
    bank_account.deposit(100)
    assert bank_account.balance == 100

def test_withdrawal(bank_account):
    bank_account = bank_account
    bank_account.withdrawal(50)
    assert bank_account.balance == 50

def test_interest(bank_account):
    bank_account = bank_account
    bank_account.collected_interest()
    assert round(bank_account.balance,6) == 110

def test_bank_transaction(zero_bank_account):
    zero_bank_account.deposit(200)
    zero_bank_account.withdrawal(100)

    assert zero_bank_account.balance == 100 

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200,100,100),
    (50,10,40),
    (5000,1000,4000)
]) 
def test_bank_transaction_1(zero_bank_account,deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdrawal(withdrew)

    assert zero_bank_account.balance == expected 

def test_insuficient_funds(bank_account):

    with pytest.raises(InsuficientFunds):
        bank_account.withdrawal(200)
