"""
Unit tests for the accounts.py module
"""
import unittest
from accounts import Account, InsufficientFundsError, InvalidTransactionError

class TestAccount(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.account = Account("ACC001", 1000.0)
        
    def test_account_creation(self):
        """Test account creation with correct parameters."""
        self.assertEqual(self.account.account_id, "ACC001")
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(len(self.account.transactions), 0)
        
    def test_deposit_positive_amount(self):
        """Test depositing a positive amount."""
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 1)
        
    def test_deposit_zero_amount(self):
        """Test depositing zero amount raises InvalidTransactionError."""
        with self.assertRaises(InvalidTransactionError):
            self.account.deposit(0.0)
            
    def test_deposit_negative_amount(self):
        """Test depositing negative amount raises InvalidTransactionError."""
        with self.assertRaises(InvalidTransactionError):
            self.account.deposit(-100.0)
            
    def test_withdraw_positive_amount(self):
        """Test withdrawing a positive amount."""
        self.account.withdraw(200.0)
        self.assertEqual(self.account.balance, 800.0)
        self.assertEqual(len(self.account.transactions), 1)
        
    def test_withdraw_zero_amount(self):
        """Test withdrawing zero amount raises InvalidTransactionError."""
        with self.assertRaises(InvalidTransactionError):
            self.account.withdraw(0.0)
            
    def test_withdraw_negative_amount(self):
        """Test withdrawing negative amount raises InvalidTransactionError."""
        with self.assertRaises(InvalidTransactionError):
            self.account.withdraw(-100.0)
            
    def test_withdraw_insufficient_funds(self):
        """Test withdrawing more than available balance raises InsufficientFundsError."""
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(1500.0)
            
    def test_buy_valid_transaction(self):
        """Test buying shares with valid parameters."""
        self.account.buy("AAPL", 10, 50.0)
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(len(self.account.transactions), 1)
        
    def test_buy_zero_quantity(self):
        """Test buying zero quantity raises InvalidTransactionError."""
        with self.assertRaises(InvalidTransactionError):
            self.account.buy("AAPL", 0, 50.0)
            
    def test_buy_negative_price(self):
        """Test buying with negative price raises InvalidTransactionError."""
        with self.assertRaises(InvalidTransactionError):
            self.account.buy("AAPL", 10, -50.0)
            
    def test_buy_insufficient_funds(self):
        """Test buying shares with insufficient funds raises InsufficientFundsError."""
        with self.assertRaises(InsufficientFundsError):
            self.account.buy("AAPL", 10, 200.0)
            
    def test_sell_valid_transaction(self):
        """Test selling shares with valid parameters."""
        self.account.sell("AAPL", 10, 50.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 1)
        
    def test_sell_zero_quantity(self):
        """Test selling zero quantity raises InvalidTransactionError."""
        with self.assertRaises(InvalidTransactionError):
            self.account.sell("AAPL", 0, 50.0)
            
    def test_sell_negative_price(self):
        """Test selling with negative price raises InvalidTransactionError."""
        with self.assertRaises(InvalidTransactionError):
            self.account.sell("AAPL", 10, -50.0)
            
    def test_get_balance(self):
        """Test getting account balance."""
        self.assertEqual(self.account.get_balance(), 1000.0)
        
    def test_get_transaction_history(self):
        """Test getting transaction history."""
        self.account.deposit(500.0)
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["type"], "deposit")
        
    def test_get_account_info(self):
        """Test getting account information."""
        info = self.account.get_account_info()
        self.assertEqual(info["account_id"], "ACC001")
        self.assertEqual(info["balance"], 1000.0)
        self.assertEqual(info["transaction_count"], 0)
        
    def test_transaction_timestamp(self):
        """Test that transactions record timestamps."""
        self.account.deposit(500.0)
        transaction = self.account.transactions[0]
        self.assertIn("timestamp", transaction)
        
    def test_multiple_transactions(self):
        """Test multiple transactions are recorded correctly."""
        self.account.deposit(500.0)
        self.account.withdraw(200.0)
        self.account.buy("AAPL", 10, 50.0)
        
        self.assertEqual(len(self.account.transactions), 3)
        self.assertEqual(self.account.balance, 800.0)
        
    def test_account_id_access(self):
        """Test that account ID can be accessed correctly."""
        self.assertEqual(self.account.account_id, "ACC001")

if __name__ == '__main__':
    unittest.main()