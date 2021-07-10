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


class OrderBook:

    def __init__(self):
        self.asks = []
        self.bids = []

    def append(self, order: Order):
        if type(order) is Ask:
            self.asks.append(order)
        elif type(order) is Bid:
            self.bids.append(order)
        else:
            print('Неверный тип заявки')

    def get_sorted_market_data(self):
        return {"asks": list(map(lambda x: x.get_data_dictionary(), sorted(self.asks, key=lambda order: order.price))),
                "bids": list(map(lambda x: x.get_data_dictionary(), sorted(self.bids, key=lambda order: order.price)))}


if __name__ == '__main__':
    order1 = Ask(100.50, 1000)
    order2 = Bid(200, 500)
    order3 = Ask(-100, 1100)
    order4 = Ask(333, 500)
    order5 = Ask(1, 500)
    order_book = OrderBook()
    order_book.append(order1)
    order_book.append(order2)
    order_book.append(order3)
    order_book.append(order4)
    order_book.append(order5)
    a = order_book.get_sorted_market_data()
    print(a)
