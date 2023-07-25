import  datetime

from qstrader import settings
from montly_rebalance_run import run_montly_rebalance

if __name__ == '__main__':
    ticker_weight= {
        "SPY": 0.6,
        "AGG": 0.4
    }

    run_montly_rebalance(
        settings.DEFAULT_CONFIG_FILENAME,
        False, "", "SPY",
        ticker_weight, "US Equities/Bonds 60/40 Mix ETF Strategy",
        datetime.datetime(2003, 9, 29), datetime.datetime(2016, 10, 12),
        500000.00
    )