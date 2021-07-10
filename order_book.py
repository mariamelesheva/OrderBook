class OrderBook:
    class Order:

        def __init__(self, price: float, quantity: int):
            self.price = price
            self.quantity = quantity

        def get_data_dictionary(self):
            return {"price": self.price, "quantity": self.quantity}

    class Ask(Order):
        pass

    class Bid(Order):
        pass

    asks: list[Ask]
    bids: list[Bid]

    def __init__(self):

        self.asks = []
        self.bids = []

    def get_sorted_market_data(self):
        return {"asks": list(map(lambda x: x.get_data_dictionary(), sorted(self.asks, key=lambda order: order.price))),
                "bids": list(map(lambda x: x.get_data_dictionary(), sorted(self.bids, key=lambda order: order.price)))}

    def remove(self, order):
        if type(order) is OrderBook.Ask:
            self.asks.remove(order)
        elif type(order) is OrderBook.Bid:
            self.bids.remove(order)
        else:
            print(f'wrong order type: {type(order)}')

    def create_bid(self, price: float, quantity: int):
        err = self.__perform_checks(price, quantity)
        if not err:
            bid = OrderBook.Bid(price, quantity)
            self.bids.append(bid)
            print('bid added')
            return bid

    def create_ask(self, price: float, quantity: int):
        err = self.__perform_checks(price, quantity)
        if not err:
            ask = OrderBook.Ask(price, quantity)
            self.asks.append(ask)
            print('ask added')
            return ask

    def __perform_checks(self, price, quantity):
        if type(price) is not float and type(price) is not int:
            print(f'wrong price type: {type(price)}')
            return True
        if price <= 0:
            print(f'price must be greater than 0')
            return True

        if type(quantity) is not int:
            print(f'wrong quantity type: {type(quantity)}')
            return True
        if quantity <= 0:
            print(f'quantity must be greater than 0')
            return True


if __name__ == '__main__':
    orders_book = OrderBook()
    orders_book.create_bid(price=100.60, quantity=10)
    orders_book.create_bid(price=200, quantity=10)
    orders_book.create_bid(price=50, quantity=10)
    orders_book.create_bid(price=0, quantity=10)
    orders_book.create_bid(price=-150, quantity=10)
    orders_book.create_bid(price=100.60, quantity=-10)
    orders_book.create_bid(price=200, quantity=0)
    orders_book.create_bid(price=100.60, quantity=10.5)

    orders_book.create_ask(price=50, quantity=10)
    orders_book.create_ask(price=0, quantity=10)
    orders_book.create_ask(price=-150, quantity=10)
    orders_book.create_ask(price=100.60, quantity=-10)
    orders_book.create_ask(price=200, quantity=0)
    orders_book.create_ask(price=100.60, quantity=10)

    orders_book.create_ask(price='123', quantity=10)
    orders_book.create_ask(price=600, quantity='777')

    print(orders_book.get_sorted_market_data())
