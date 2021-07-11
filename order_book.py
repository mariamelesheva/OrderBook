import enum


class OrderType(enum.Enum):
    ASK = 0
    BID = 1


class OrderBook:
    class Order:

        def __init__(self, price: float, quantity: int, order_type: OrderType):
            self.price = price
            self.quantity = quantity
            self.order_type = order_type
            self.id = id(self)

        def get_data_dictionary(self):
            return {"price": self.price, "quantity": self.quantity}

    def __init__(self):
        self.asks = []
        self.bids = []

    def get_market_data(self):
        return {"asks": list(map(lambda x: x.get_data_dictionary(), self.asks)),
                "bids": list(map(lambda x: x.get_data_dictionary(), self.bids))}

    def __insert_order(self, orders_list: list, order: Order):
        index = 0
        orders_length = len(orders_list)
        if orders_length == 0:
            orders_list.append(order)
            return
        for i in range(orders_length):
            if orders_list[i].price > order.price:
                index = i
                break
            elif i == orders_length - 1:
                orders_list.append(order)
                return
        orders_list.insert(index, order)

    def create_order(self, price: float, quantity: int, order_type: OrderType):
        if type(price) is not float and type(price) is not int:
            print(f'wrong price type: {type(price)}')
            return
        if price <= 0:
            print(f'price must be greater than 0')
            return

        if type(quantity) is not int:
            print(f'wrong quantity type: {type(quantity)}')
            return
        if quantity <= 0:
            print(f'quantity must be greater than 0')
            return

        if type(order_type) is not OrderType:
            print(f'wrong order type')
            return

        order = OrderBook.Order(price, quantity, order_type)
        if order.order_type == OrderType.ASK:
            self.__insert_order(self.asks, order)
        else:
            self.__insert_order(self.bids, order)
        return order

    def get_order_by_id(self, order_id: int):
        if type(order_id) is not int:
            print('wrong type order id')
            return
        for order in self.asks:
            if order.id == order_id:
                return order
        for order in self.bids:
            if order.id == order_id:
                return order
        print(f'order not found by id {order_id}')
        return

    def remove_order_by_id(self, order_id: int):
        if type(order_id) is not int:
            print('wrong type order id')
            return
        for order in self.asks:
            if order.id == order_id:
                self.asks.remove(order)
                return
        for order in self.bids:
            if order.id == order_id:
                self.bids.remove(order)
                return
