# -*- coding: utf-8 -*-

import datetime
import click

from qstrader import settings
from qstrader.compat import queue
from qstrader.price_parser import PriceParser
from qstrader.price_handler.yahoo_daily_csv_bar import YahooDailyCsvBarPriceHandler
from cyd.strategy.portfolio.monthly_liquidate_rebalance_strategy import MonthlyLiquidateRebalanceStrategy
from qstrader.strategy import Strategies
from qstrader.position_sizer.rebalance import LiquidateRebalancePositionSizer
from qstrader.risk_manager.example import ExampleRiskManager
from qstrader.portfolio_handler import PortfolioHandler
from qstrader.compliance.example import ExampleCompliance
from qstrader.execution_handler.ib_simulated import IBSimulatedExecutionHandler
from qstrader.statistics.tearsheet import TearsheetStatistics
from qstrader.trading_session import TradingSession

def run_montly_rebalance(config, testing, filename, benchmark, ticker_weights, title_str,
                         start_date, end_date, equity):
    config = settings.from_file(config, testing)
    tickers = [t for t in ticker_weights.keys()]

    events_queue = queue.Queue()
    csv_dir = config.CSV_DATA_DIR
    initial_equity = PriceParser.parse(equity)

    price_handler = YahooDailyCsvBarPriceHandler(
        csv_dir, events_queue, tickers,
        start_date=start_date, end_date=end_date
    )

    strategy = MonthlyLiquidateRebalanceStrategy(tickers, events_queue)
    strategy = Strategies(strategy)

    position_sizer = LiquidateRebalancePositionSizer(ticker_weights)

    risk_manager = ExampleRiskManager()

    portfolio_handler = PortfolioHandler(
        initial_equity, events_queue, price_handler,
        position_sizer, risk_manager
    )

    compliance = ExampleCompliance(config, "KK_Test")

    execution_handler = IBSimulatedExecutionHandler(
        events_queue, price_handler, compliance
    )

    title = [title_str]
    statistics = TearsheetStatistics(
        config, portfolio_handler, title, benchmark
    )

    backtest = TradingSession(
        config, strategy, tickers,
        equity, start_date, end_date,events_queue,
        price_handler=price_handler, portfolio_handler=portfolio_handler,
        compliance = compliance, position_sizer=position_sizer,
        execution_handler = execution_handler, risk_manager=risk_manager,
        statistics=statistics, title=title

    )
    results = backtest.start_trading(testing=testing)
    statistics.save(filename)
    return results

