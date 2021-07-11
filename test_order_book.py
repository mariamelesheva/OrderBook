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
    def test_create_order_negative(self, order_type, price, quantity):
        ask = self.order_book.create_order(price, quantity, order_type)
        assert ask is None
        assert len(self.order_book.asks) == 0
        assert len(self.order_book.bids) == 0


class TestGetMarketData:

    def setup(self):
        self.order_book = OrderBook()

    def test_get_market_data(self):
        self.order_book.create_order(100.5, 10, OrderType.ASK)
        self.order_book.create_order(300, 400, OrderType.BID)
        self.order_book.create_order(300, 400, OrderType.BID)
        self.order_book.create_order(60, 1, OrderType.ASK)
        self.order_book.create_order(100.4, 4, OrderType.ASK)
        self.order_book.create_order(100.5, 10, OrderType.ASK)
        self.order_book.create_order(60.6, 4, OrderType.BID)
        self.order_book.create_order(100.5, 10, OrderType.BID)
        self.order_book.create_order(100.5, 9, OrderType.ASK)

        orders_dictionary = {"asks": [{"price": 60, "quantity": 1},
                                      {"price": 100.4, "quantity": 4},
                                      {"price": 100.5, "quantity": 10},
                                      {"price": 100.5, "quantity": 10},
                                      {"price": 100.5, "quantity": 9}],
                             "bids": [{"price": 60.6, "quantity": 4},
                                      {"price": 100.5, "quantity": 10},
                                      {"price": 300, "quantity": 400},
                                      {"price": 300, "quantity": 400}]}
        assert self.order_book.get_market_data() == orders_dictionary

    def test_get_empty_market_data(self):
        assert self.order_book.get_market_data() == {"asks": [], "bids": []}


class TestRemoveOrder:

    def setup(self):
        self.order_book = OrderBook()
        self.asks = []
        self.bids = []
        self.asks.append(self.order_book.create_order(100.5, 10, OrderType.ASK))
        self.bids.append(self.order_book.create_order(300, 400, OrderType.BID))
        self.bids.append(self.order_book.create_order(300, 400, OrderType.BID))
        self.asks.append(self.order_book.create_order(60, 1, OrderType.ASK))
        self.asks.append(self.order_book.create_order(100.4, 4, OrderType.ASK))
        self.asks.append(self.order_book.create_order(100.5, 10, OrderType.ASK))
        self.bids.append(self.order_book.create_order(60.6, 4, OrderType.BID))
        self.bids.append(self.order_book.create_order(100.5, 10, OrderType.BID))
        self.asks.append(self.order_book.create_order(100.5, 9, OrderType.ASK))

        self.asks_start_len = len(self.order_book.asks)
        self.bids_start_len = len(self.order_book.bids)

    @pytest.mark.parametrize("index",
                             [0, 3, 4])
    def test_remove_ask(self, index):
        self.order_book.remove_order_by_id(self.asks[index].id)
        assert self.asks[index] not in self.order_book.asks
        self.asks.remove(self.asks[index])
        assert len(self.order_book.asks) == self.asks_start_len - 1
        assert len(self.order_book.bids) == self.bids_start_len
        for ask in self.asks:
            assert ask in self.order_book.asks
        for bid in self.bids:
            assert bid in self.order_book.bids

    def test_remove_all(self):
        for ask in self.asks:
            self.order_book.remove_order_by_id(ask.id)
        assert len(self.order_book.asks) == 0
        for bid in self.bids:
            self.order_book.remove_order_by_id(bid.id)
        assert len(self.order_book.bids) == 0

    @pytest.mark.parametrize("index",
                             [0, 3, 3])
    def test_remove_bid(self, index):
        self.order_book.remove_order_by_id(self.bids[index].id)
        assert self.bids[index] not in self.order_book.bids
        self.bids.remove(self.bids[index])
        assert len(self.order_book.asks) == self.asks_start_len
        assert len(self.order_book.bids) == self.bids_start_len - 1
        for ask in self.asks:
            assert ask in self.order_book.asks
        for bid in self.bids:
            assert bid in self.order_book.bids

    class TestGetOrder:
        def setup(self):
            self.order_book = OrderBook()

        def test_get_order(self):
            order1 = self.order_book.create_order(100.5, 10, OrderType.ASK)
            order2 = self.order_book.create_order(100.5, 10, OrderType.BID)
            order_by_id = self.order_book.get_order_by_id(order1.id)
            assert order_by_id == order1
            order_by_id2 = self.order_book.get_order_by_id(order2.id)
            assert order_by_id2 == order2

        @pytest.mark.parametrize("order_id",
                                 [2276700285232,
                                  '2276700285232'])
        def test_get_order_by_wrong_id(self, order_id):
            order_by_id = self.order_book.get_order_by_id(order_id)
            assert order_by_id is None
