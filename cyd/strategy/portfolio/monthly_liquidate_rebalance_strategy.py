# -*- coding: utf-8 -*-

import calendar
import datetime

from qstrader import settings
from qstrader.strategy.base import AbstractStrategy
from qstrader.position_sizer.rebalance import LiquidateRebalancePositionSizer
from qstrader.event import SignalEvent, EventType
from qstrader.compat import queue
from qstrader.trading_session import TradingSession

class MonthlyLiquidateRebalanceStrategy(AbstractStrategy):
    """
    每个月月末重新配置
    """
    def __init__(self, tickers, events_queue):
        self.tickers = tickers
        self.events_queue = events_queue
        self.tickers_invested = self._create_invested_list()

    def _end_of_month(self, cur_time):
        cur_day = cur_time.day
        end_day = calendar.monthrange(cur_time.year, cur_time.month)[1]
        return cur_day == end_day

    def _create_invested_list(self):
        tickers_invested = {ticker: False for ticker in self.tickers}
        return tickers_invested

    def calculate_signals(self, event):
        if(event.type in [EventType.BAR, EventType.TICK] and self._end_of_month(event.time)):
            ticker = event.ticker
            if ticker in self.tickers_invested:
                if self.tickers_invested[ticker]:
                    liquidate_signal = SignalEvent(ticker, "EXIT")
                    self.events_queue.put(liquidate_signal)
                long_signal = SignalEvent(ticker, "BOT")
                self.events_queue.put(long_signal)
                self.tickers_invested[ticker] = True

def run(config, testing, tickers, filename):
    title = ['Monthly Liquidate/Rebalance on 60%/40% SPY/AGG Portfolio']
    initial_equity = 500000.0
    start_date = datetime.datetime(2006, 11, 1)
    end_date = datetime.datetime(2016, 10, 12)

    events_queue = queue.Queue()

    strategy = MonthlyLiquidateRebalanceStrategy(tickers[1:], events_queue)

    ticker_weights = {
        "AAPL": 0.6,
        "AGG": 0.4
    }
    position_sizer = LiquidateRebalancePositionSizer(ticker_weights)

    backtest = TradingSession(
        config, strategy, tickers,
        initial_equity, start_date, end_date,
        events_queue, position_sizer=position_sizer,
        title=title, benchmark=tickers[0],
    )
    results = backtest.start_trading(testing=testing)
    return results

if __name__ == '__main__':
    testing = False
    config = settings.from_file(settings.DEFAULT_CONFIG_FILENAME, testing)

    tickers = ["SPY", "AAPL", "AGG"]
    filename = None
    run(config, testing, tickers, filename)
