from main.domain import GoldenCross


def start():
    print("start")
    stock_id='sh.600036'
    GoldenCross.print_cross_useful(stock_id)
    # GoldenCross.computeMACD(stock_id)
    print("end")

if __name__ == "__main__":
    start()