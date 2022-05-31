from main.strategy import StrategyLib


def start():
    print("start")
    stock_id='sh.113622'
    StrategyLib.call_day_15min(stock_id, False)
    print("end")

if __name__ == "__main__":
    start()