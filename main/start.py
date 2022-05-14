from main.domain import MacdDeviation


def start():
    print("start")
    stock_id='sh.600036'
    MacdDeviation.print_deviation(stock_id)
    print("end")

if __name__ == "__main__":
    start()