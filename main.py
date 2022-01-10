from src import claim_reward, read_acc_info, refuel_ship, racing_ships

def main():
    print('Starting run main code')
    accounts = read_acc_info()
    refuel_ship(accounts)
    racing_ships(accounts)
    claim_reward(accounts)


if __name__ == "__main__":
    main()