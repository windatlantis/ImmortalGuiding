from main.domain import GoldenCross


def start():
    print("start")
    GoldenCross.print_gloden_cross()
    # GoldenCross.computeMACD()
    print("end")

if __name__ == "__main__":
    start()