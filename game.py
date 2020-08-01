import os

from server_rnr import MCRunner

if __name__ == '__main__':
    runner = MCRunner(os.path.join(os.getcwd(), 'minecraft'))
    runner.start_main_loop()
