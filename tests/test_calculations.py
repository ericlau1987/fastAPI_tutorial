from app.calculations import add, subtract, BankAccount
import pytest 

@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (3, 2, 5),
    (4, 2, 6),
    (2, 1, 3)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected

def test_subtract():
    print("testing add function")
    assert subtract(5, 2) == 3

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,5) == 55