class Category:
    # Initialize the given variables
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.__balance = 0.0
    
    # Make a readable object description
    def __str__(self):
        ledger_items = ''
        for items in self.ledger:
            ledger_items = ledger_items + '{: <23}{: >7.2f}'.format(items['description'][:23], items['amount'])
            if items != self.ledger[-1]:
                ledger_items += '\n'
            else:
                ledger_items += '\nTotal: {}'.format(self.__balance)
        return str(self.name).center(30, '*') + '\n' + ledger_items
    
    # Make a deposit and update the balance
    def deposit(self, amount, description = ''):
        self.ledger.append({"amount": amount, "description": description})
        self.__balance += amount
    
    # Check if the funds are enough for the withdrawal and go through with it, or not.
    # Return True if funds are sufficient, false otherwise
    def withdraw(self, amount, description = ''):
        if Category.check_funds(self, amount):
            self.ledger.append({"amount": -amount, "description": description})
            self.__balance -= amount
            return True
        else:
            return False
    
    # Return balance
    def get_balance(self):
        return self.__balance
    
    # See if balance is sufficient
    def check_funds(self, amount):
        return (self._Category__balance >= amount)
    
    # Transfer money between accounts and update the ledger with description
    def transfer(self, amount, other):
        if Category.check_funds(self, amount):
            self._Category__balance -= amount
            other._Category__balance += amount
            self.ledger.append({"amount": -amount, "description": 'Transfer to {}'.format(other.name)})
            other.ledger.append({"amount": amount, "description": 'Transfer from {}'.format(self.name)})
            return True
        else:
            return False


# Here we will make a chart showing the distribution of spendings (withdrawals)
def create_spend_chart(categories):
    
    # Variables used in this function
    title = 'Percentage spent by category\n'
    amount_spent = {}
    total = 0
    string_categories = []
    diagram = ''
    divider = '    ' + '-' * (3 * len(categories) + 1) + '\n'
    vertical_categories = ''
    
    # Looping through the ledger and adding the spendings into a dictionary and total spendings as a variable (total).
    # We also fill the string_categories list to make it easier for us later
    for category in categories:
        spendings = 0
        string_categories.append(category.name)
        for item in category.ledger:
            if item['amount'] < 0:
                spendings += -item['amount']
                total -= item['amount']
        amount_spent[category] = spendings
    
    # Making the diagram itself
    for i in range(100, -1, -10):
        diagram += '{: >3}| '.format(i)
        for category in categories:
            if (round(amount_spent[category] * 1000 / (total)) / 10) >= i:
                diagram += 'o  '
            else:
                diagram += '   '
        diagram += '\n'
    
    # Looping through lines and categories to make the category names vertical
    for i in range(len(max(string_categories, key=len))):
        vertical_categories += '     '
        for category in string_categories:
            try:
                vertical_categories += '{}  '.format(category[i])
            except:
                vertical_categories += '   '
        if i != len(max(string_categories, key=len)) - 1:
            vertical_categories += '\n'
    
    
    return title + diagram + divider + vertical_categories

