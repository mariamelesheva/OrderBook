import pytest

from order_book import OrderBook, OrderType


class TestCreateOrder:

    def setup(self):
        self.order_book = OrderBook()

    def create_order_and_check_created(self, price, quantity, order_type):
        order = self.order_book.create_order(price, quantity, order_type)
        assert order.price == price
        assert order.quantity == quantity
        assert order.order_type == order_type
        return order

    @pytest.mark.parametrize("order_type, price, quantity",
                             [(OrderType.ASK, 100, 200),
                              (OrderType.ASK, 60.90, 30)])
    def test_create_ask_positive(self, order_type, price, quantity):
        order = self.create_order_and_check_created(price, quantity, order_type)
        assert order in self.order_book.asks
        assert len(self.order_book.bids) == 0

    @pytest.mark.parametrize("order_type, price, quantity",
                             [(OrderType.BID, 100, 200),
                              (OrderType.BID, 60.90, 30)])
    def test_create_bid_positive(self, order_type, price, quantity):
        order = self.create_order_and_check_created(price, quantity, order_type)
        assert order in self.order_book.bids
        assert len(self.order_book.asks) == 0

    @pytest.mark.parametrize("order_type, price, quantity",
                             [(OrderType.ASK, 0, 1200),
                              (OrderType.ASK, -120, 1),
                              (OrderType.ASK, '123', 666666),
                              (OrderType.ASK, 30, 160.5),
                              (OrderType.ASK, 100, 0),
                              (OrderType.ASK, 5, -5),
                              (OrderType.ASK, 66, [1]),

                              (OrderType.BID, 0, 1200),
                              (OrderType.BID, -120, 1),
                              (OrderType.BID, '123', 666666),
                              (OrderType.BID, 30, 160.5),
                              (OrderType.BID, 100, 0),
                              (OrderType.BID, 5, -5),
                              (OrderType.BID, 66, [1])
                              ])
    def test_negative(self, order_type, price, quantity):
        ask = self.order_book.create_order(price, quantity, order_type)
        assert ask is None
        assert len(self.order_book.asks) == 0
        assert len(self.order_book.bids) == 0


class TestGetMarketData:
    def test_get_market_data(self):
        order_book = OrderBook()
        order_book.create_order(100.5, 10, OrderType.ASK)
        order_book.create_order(300, 400, OrderType.BID)
        order_book.create_order(300, 400, OrderType.BID)
        order_book.create_order(60, 1, OrderType.ASK)
        order_book.create_order(100.4, 4, OrderType.ASK)
        order_book.create_order(100.5, 10, OrderType.ASK)
        order_book.create_order(60.6, 4, OrderType.BID)
        order_book.create_order(100.5, 10, OrderType.BID)
        order_book.create_order(100.5, 9, OrderType.ASK)

        orders_dictionary = {"asks": [{"price": 60, "quantity": 1},
                                      {"price": 100.4, "quantity": 4},
                                      {"price": 100.5, "quantity": 10},
                                      {"price": 100.5, "quantity": 10},
                                      {"price": 100.5, "quantity": 9}],
                             "bids": [{"price": 60.6, "quantity": 4},
                                      {"price": 100.5, "quantity": 10},
                                      {"price": 300, "quantity": 400},
                                      {"price": 300, "quantity": 400}]}
        assert order_book.get_market_data() == orders_dictionary
