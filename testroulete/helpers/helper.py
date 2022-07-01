import random

round_id = 1
print('Нажмите Ctrl+C для завершения работы')
while True:
    print("Раунд {}".format(round_id))
    roulette = [i for i in range(1, 11, 1)]
    steps = len(roulette)
    while steps > 0:
        input('Нажмите Enter')
        while True:
            rand_num = random.randint(0, len(roulette)-1)
            if roulette[rand_num] != 0:
                print(roulette[rand_num])
                roulette[rand_num] = 0
                steps -= 1
                break
    else:
        input('Нажмите Enter')
        print('Jack Pot!')
    round_id += 1