import pytest

from order_book import OrderBook


class TestOrderBook:
    def test_create_ask_price_int(self):
        order_book = OrderBook()
        ask = order_book.create_ask(100, 200)
        assert ask.price == 100
        assert ask.quantity == 200
        assert ask in order_book.asks

    def test_create_ask_price_float(self):
        order_book = OrderBook()
        ask = order_book.create_ask(60.90, 30)
        assert ask.price == 60.90
        assert ask.quantity == 30
        assert ask in order_book.asks

    def test_create_ask_price_zero(self):
        order_book = OrderBook()
        ask = order_book.create_ask(0, 1200)
        assert ask is None
        assert len(order_book.asks) == 0

    def test_create_ask_price_negative(self):
        order_book = OrderBook()
        ask = order_book.create_ask(-120, 1)
        assert ask is None
        assert len(order_book.asks) == 0
