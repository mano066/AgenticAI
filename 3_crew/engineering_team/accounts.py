"""
Accounting system for managing transactions and account balances
"""
import datetime
from typing import Dict, List, Optional

class InsufficientFundsError(Exception):
    """Custom exception raised when an account has insufficient funds for a transaction."""
    pass

class InvalidTransactionError(Exception):
    """Custom exception raised when a transaction is invalid."""
    pass

class Account:
    def __init__(self, account_id: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self.balance = initial_balance
        self.transactions: List[Dict] = []
        
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidTransactionError("Deposit amount must be positive")
        self.balance += amount
        self._record_transaction("deposit", amount)
        
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidTransactionError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for withdrawal")
        self.balance -= amount
        self._record_transaction("withdraw", amount)
        
    def buy(self, symbol: str, quantity: int, price: float) -> None:
        if quantity <= 0:
            raise InvalidTransactionError("Quantity must be positive")
        if price <= 0:
            raise InvalidTransactionError("Price must be positive")
        
        total_cost = quantity * price
        if total_cost > self.balance:
            raise InsufficientFundsError("Insufficient funds for purchase")
        
        self.balance -= total_cost
        self._record_transaction("buy", total_cost, symbol=symbol, quantity=quantity, price=price)
        
    def sell(self, symbol: str, quantity: int, price: float) -> None:
        if quantity <= 0:
            raise InvalidTransactionError("Quantity must be positive")
        if price <= 0:
            raise InvalidTransactionError("Price must be positive")
        
        total_value = quantity * price
        self.balance += total_value
        self._record_transaction("sell", total_value, symbol=symbol, quantity=quantity, price=price)
        
    def _record_transaction(self, transaction_type: str, amount: float, **kwargs) -> None:
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.datetime.now(),
            "account_id": self.account_id
        }
        
        # Add any additional details
        for key, value in kwargs.items():
            transaction[key] = value
            
        self.transactions.append(transaction)
        
    def get_balance(self) -> float:
        return self.balance
        
    def get_transaction_history(self) -> List[Dict]:
        return self.transactions.copy()
        
    def get_account_info(self) -> Dict:
        return {
            "account_id": self.account_id,
            "balance": self.balance,
            "transaction_count": len(self.transactions)
        }

# Function to print transaction history
def print_transaction_history(account: Account) -> None:
    print(f"Transaction history for account {account.account_id}:")
    for transaction in account.transactions:
        print(f"  {transaction['type'].capitalize()}: ${transaction['amount']:.2f}", end="")
        if 'symbol' in transaction:
            print(f" ({transaction['symbol']}, {transaction['quantity']} shares @ ${transaction['price']:.2f})")
        else:
            print()
    print()

# Function to print account summary
def print_account_summary(account: Account) -> None:
    print(f"Account ID: {account.account_id}")
    print(f"Balance: ${account.balance:.2f}")
    print(f"Number of transactions: {len(account.transactions)}")
    print()
