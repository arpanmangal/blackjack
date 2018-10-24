dealer_values = [17, 18, 19, 20, 21, 'bust', 'bj']
dealer_hand = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
table = {}

def read_dealer_table():
    """
    Read the dealer table from a file 
    for p = 4/13
    """

    file = open('stand.prob', 'r')
    for hand in dealer_hand:
        table[hand] = {}
        hand_probs = file.readline()
        prob_vals = hand_probs.split(' ')
        for val, prob_val in zip(dealer_values, prob_vals):
            table[hand][val] = float(prob_val)
        
    # print (table)


def player_reward (player_sum, dealer_card, bet, hasBlackjack=False):
    assert type(player_sum) is int
    assert type(dealer_card) is str

    if player_sum > 21:
        return -bet

    if hasBlackjack:
        profit = (1 - table[dealer_card]['bj']) * (1.5 * bet)
        return profit

    hand_probs = table[dealer_card]
    profit = 0
    for val in dealer_values:
        # correct order of conditions very important
        if val is 'bj':
            profit -= table[dealer_card][val] * bet
            continue

        if val is 'bust':
            profit += table[dealer_card][val] * bet
            continue

        if val == player_sum:
            # no profit
            profit += 0
            continue

        if val > player_sum:
            profit -= table[dealer_card][val] * bet
            continue

        if val < player_sum:
            profit += table[dealer_card][val] * bet
            continue

    return profit


if __name__ == '__main__':
    read_dealer_table()

    # for hand in dealer_hand:
    #     for val in dealer_values:
    #         print (table[hand][val], ' ', end='')
    #     print()

    for player_sum in range(5, 23):
        for dealer_card in dealer_hand:
            print (round(reward(player_sum, dealer_card, 1), 2), ' ', end='')
        print()

    for dealer_card in dealer_hand:
        print (round(reward(21, dealer_card, 1, True), 2), ' ', end='')
    print()