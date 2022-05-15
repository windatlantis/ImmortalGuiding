from main.domain import MacdDeviation
from main.strategy import StrategyLib


def start():
    print("start")
    stock_id='sh.603982'
    # MacdDeviation.print_deviation(stock_id)
    StrategyLib.call_day_15min(stock_id)
    print("end")

if __name__ == "__main__":
    start()