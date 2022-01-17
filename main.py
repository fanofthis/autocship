from src import claim_reward, read_acc_info, racing_ships, refuel_ships
from multiprocessing import Pool
from multiprocessing import freeze_support

def main():
    print('Starting run main code')
    accounts = read_acc_info()
    n_processors = 5
    run_multiprocessing(refuel_ships, accounts, n_processors)
    run_multiprocessing(racing_ships, accounts, n_processors)
    run_multiprocessing(claim_reward, accounts, n_processors)


def run_multiprocessing(func, i, n_processors):
    with Pool(processes=n_processors) as pool:
        return pool.map(func, i)


if __name__ == "__main__":
    freeze_support()
    main()