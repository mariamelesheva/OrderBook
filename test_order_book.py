import pytest

from order_book import OrderBook


class TestAskPrice:
    def test_create_ask_price_int_quantity_int(self):
        order_book = OrderBook()
        ask = order_book.create_ask(100, 200)
        assert ask.price == 100
        assert ask.quantity == 200
        assert ask in order_book.asks
        assert len(order_book.bids) == 0

    def test_create_ask_price_float(self):
        order_book = OrderBook()
        ask = order_book.create_ask(60.90, 30)
        assert ask.price == 60.90
        assert ask.quantity == 30
        assert ask in order_book.asks
        assert len(order_book.bids) == 0

    def test_create_ask_price_zero(self):
        order_book = OrderBook()
        ask = order_book.create_ask(0, 1200)
        assert ask is None
        assert len(order_book.asks) == 0
        assert len(order_book.bids) == 0

    def test_create_ask_price_negative(self):
        order_book = OrderBook()
        ask = order_book.create_ask(-120, 1)
        assert ask is None
        assert len(order_book.asks) == 0
        assert len(order_book.bids) == 0

    def test_create_ask_price_wrong_type(self):
        order_book = OrderBook()
        ask = order_book.create_ask('123', 666666)
        assert ask is None
        assert len(order_book.asks) == 0
        assert len(order_book.bids) == 0


class TestAskQuantity:

    def test_create_ask_quantity_float(self):
        order_book = OrderBook()
        ask = order_book.create_ask(30, 160.5)
        assert ask is None
        assert len(order_book.asks) == 0
        assert len(order_book.bids) == 0

    def test_create_ask_quantity_zero(self):
        order_book = OrderBook()
        ask = order_book.create_ask(100, 0)
        assert ask is None
        assert len(order_book.asks) == 0
        assert len(order_book.bids) == 0

    def test_create_ask_quantity_negative(self):
        order_book = OrderBook()
        ask = order_book.create_ask(5, -5)
        assert ask is None
        assert len(order_book.asks) == 0
        assert len(order_book.bids) == 0

    def test_create_ask_quantity_wrong_type(self):
        order_book = OrderBook()
        ask = order_book.create_ask(66, [1])
        assert ask is None
        assert len(order_book.asks) == 0
        assert len(order_book.bids) == 0


class TestBidPrice:
    def test_create_bid_price_int_quantity_int(self):
        order_book = OrderBook()
        bid = order_book.create_bid(100, 200)
        assert bid.price == 100
        assert bid.quantity == 200
        assert bid in order_book.bids
        assert len(order_book.asks) == 0

    def test_create_bid_price_float(self):
        order_book = OrderBook()
        bid = order_book.create_bid(60.90, 30)
        assert bid.price == 60.90
        assert bid.quantity == 30
        assert bid in order_book.bids
        assert len(order_book.asks) == 0

    def test_create_bid_price_zero(self):
        order_book = OrderBook()
        bid = order_book.create_bid(0, 1200)
        assert bid is None
        assert len(order_book.bids) == 0
        assert len(order_book.asks) == 0

    def test_create_bid_price_negative(self):
        order_book = OrderBook()
        bid = order_book.create_bid(-120, 1)
        assert bid is None
        assert len(order_book.bids) == 0
        assert len(order_book.asks) == 0

    def test_create_bid_price_wrong_type(self):
        order_book = OrderBook()
        bid = order_book.create_bid('123', 666666)
        assert bid is None
        assert len(order_book.bids) == 0
        assert len(order_book.asks) == 0


class TestBidQuantity:

    def test_create_bid_quantity_float(self):
        order_book = OrderBook()
        bid = order_book.create_bid(30, 160.5)
        assert bid is None
        assert len(order_book.bids) == 0
        assert len(order_book.asks) == 0

    def test_create_bid_quantity_zero(self):
        order_book = OrderBook()
        bid = order_book.create_bid(100, 0)
        assert bid is None
        assert len(order_book.bids) == 0
        assert len(order_book.asks) == 0

    def test_create_bid_quantity_negative(self):
        order_book = OrderBook()
        bid = order_book.create_bid(5, -5)
        assert bid is None
        assert len(order_book.bids) == 0
        assert len(order_book.asks) == 0

    def test_create_bid_quantity_wrong_type(self):
        order_book = OrderBook()
        bid = order_book.create_bid(66, [1])
        assert bid is None
        assert len(order_book.bids) == 0
        assert len(order_book.asks) == 0
