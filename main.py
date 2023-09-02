import sys

from controllers import MainController


if __name__ == "__main__":
    controller = MainController(sys.argv)
    controller.run()

    sys.exit()
