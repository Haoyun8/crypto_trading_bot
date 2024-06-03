class Simulator:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.trades = []

    def simulate_trade(self, price, amount, side):
        if side == 'buy':
            cost = price * amount
            if self.balance >= cost:
                self.balance -= cost
                self.trades.append(('buy', price, amount))
            else:
                raise ValueError("Insufficient balance for buy trade")
        elif side == 'sell':
            self.balance += price * amount
            self.trades.append(('sell', price, amount))
        return self.balance

    def get_balance(self):
        return self.balance

    def get_trades(self):
        return self.trades

# Usage example
# simulator = Simulator(1000)
# balance = simulator.simulate_trade(50000, 0.001, 'buy')
# print(balance)
