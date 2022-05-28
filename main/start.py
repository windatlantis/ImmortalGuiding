from main.strategy import StrategyLib


def start():
    print("start")
    stock_id='sh.601015'
    StrategyLib.call_day_15min(stock_id)
    print("end")

if __name__ == "__main__":
    start()