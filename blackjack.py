"""
Artificial Intelligence (COL333) A4
An optimal policy for blackjack (casino card game) using MDP
"""

import sys
from dealer import reward

## Policy is key value pair of (states, value)
## State = (player_hand, dealer_card, double_allowed)
player_hand = ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
                 '22', '33', '44', '55', '66', '77', '88', '99', '1010', 'AA']
dealer_card = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
double_allowed = [True, False]

face_card_prob = 4.0 / 13
num_card_prob = 9.0 / 13

def initialise_values():
    """
    Initialise and return initial policy values
    Make all states reward -5
    """

    values = {}
    for dbl in double_allowed:
        for hand in player_hand:
            for card in dealer_card:
                values[(hand, card, dbl)] = -5

    return values


def value_iteration (current_values):
    """
    Performs one step of value iteration
    Computes next level of policy from current_values
    """
    new_values = {}
    for dbl in double_allowed:
        for hand in player_hand:
            for card in dealer_card:
                if hand is 'AA':
                    reward = R_split('A', card, 1, current_values, dbl)[0]
                elif hand[0] is 'A':
                    # one of the cards is an ace
                    reward = R_soft(int(hand[1:]), card, 1, current_values, dbl)[0]
                elif len(hand) == 2 and hand[0] == hand[1]:
                    # both same
                    reward = R_soft(int(hand[0]), card, 1, current_values, dbl)[0]
                elif hand == '1010':
                    reward = R_soft(10, card, 1, current_values, dbl)[0]
                else:
                    # hard total
                    reward = R_hard(int(hand), card, 1, current_values, dbl)[0]
                new_values[(hand, card, dbl)] = reward

    return new_values # placeholder


def R_hard(y, dealer_card, bet, current_values, isDoubleAllowed=False):
    """
    Calculates the optimal long term reward (or value) when the player
    has a hard hand of sum y
    """
    if y > 21:
        # bust
        return -bet, 'S'
    elif y == 21:
        # stand
        return dealer(21, dealer_card, bet), 'S'
    
    # Now three choices - stand, hit, double

    # stand
    stand = dealer(y, dealer_card, bet)

    # hit
    hit = 0
    if y+10 > 21:
        hit += face_card_prob * (-bet)
    else:
        hit += face_card_prob * current_values[(str(y+10), dealer_card, False)] * bet
        
    for x in range(2,10): # pick another card x
        if y+x > 21:
            hit += num_card_prob * (-bet)
        else:
            hit += num_card_prob * current_values [(str(y + x), dealer_card, False)] * bet
    # x is an Ace
    if y <= 10: # Ay
        hit += num_card_prob * current_values [( ('A' + str(y)), dealer_card, False)] * bet
    else: # y + 1
        hit += num_card_prob * current_values [(str(y+1), dealer_card, False)] * bet

    if (not isDoubleAllowed):
        if stand>=hit:
            return (stand, 'S')
        else:
            return (hit, 'H')

    # double
    double = 0
    if y+10 > 21:
        double += face_card_prob * (-2*bet)
    else:
        double += face_card_prob * dealer(y+10, dealer_card, 2*bet)

    for x in range(2, 10): # pick another card x
        if y+x > 21:
            double += num_card_prob * (-2*bet)
        else:
            double += num_card_prob * dealer(y+x, dealer_card, 2*bet)
    # x is an Ace
    if y <= 10:
        double += num_card_prob * dealer(y+11, dealer_card, 2*bet)
    else:
        double += num_card_prob * dealer(y+1, dealer_card, 2*bet)

    if stand >= hit:
        if double >= stand:
            return (double, 'D')
        else:
            return (stand, 'S')
    else:
        if double >= hit:
            return (double, 'D')
        else:
            return (hit, 'H')


def R_soft(y, dealer_card, bet, current_values, isDoubleAllowed=False):
    """
    Calculates the optimal long term reward (or value) when the player
    has a soft hand of the form Ay
    """
    if y == 10:
        #A10
        if isDoubleAllowed:
            return dealer(21, dealer_card, bet, True), 'S'
        else:
            return dealer(21, dealer_card, bet), 'S'
    
    # Three choices - stand, hit, double
    
    # stand
    stand = dealer(11+y, dealer_card, bet)

    # hit
    hit = 0
    hit += face_card_prob * current_values[(str(1+y+10), dealer_card, False)] * bet

    for x in range(2, 10): # pick another card x
        if 11+y+x > 21:
            hit += num_card_prob * current_values[( str(1+y+x), dealer_card, False)] * bet
        else:
            hit += num_card_prob * current_values[( ('A' + str(y+x)), dealer_card, False)] * bet
    # x is an ace
        if 11+y+1 > 21:
            hit += num_card_prob * current_values[( str(1+y+1), dealer_card, False)] * bet
        else:
            hit += num_card_prob * current_values[( ('A' + str(y+1)), dealer_card, False)] * bet
    
    if (not isDoubleAllowed):
        if stand >= hit:
            return (stand, 'S')
        else:
            return (hit, 'H')
    
    # double
    double = 0
    double += face_card_prob * dealer((1+y+10), dealer_card, 2*bet)

    for x in range(2, 10): #pick another card x
        if 11+y+x > 21:
            double += num_card_prob * dealer(1+y+x, dealer_card, 2*bet)
        else:
            double += num_card_prob * dealer(11+y+x, dealer_card, 2*bet)
    # x is an ace
        if 11+y+1 > 21:
            double += num_card_prob * dealer(1+y+1, dealer_card, 2*bet)
        else:
            double += num_card_prob * dealer(11+y+1, dealer_card, 2*bet)

    if stand >= hit:
        if double >= stand:
            return (double, 'D')
        else:
            return (stand, 'S')
    else:
        if double >= hit:
            return double, 'D'
        else:
            return hit, 'H'


def R_split(y, dealer_card, bet, current_values, isDoubleAllowed=False):
    """
    Calculates the optimal long term reward (or value) when the player
    has a hand of the form yy
    """
    
    return 0, 'H' ## placeholder


def get_policy(values):
    """
    Get the corresponding policy, pi
    for the given values, V
    """
    
    policy = {}

    for hand in player_hand:
        # if hand is 'A10' or hand is '20' or hand is '21':
            # continue
        for card in dealer_card:
            if hand is 'AA':
                action = R_split('A', card, 1, values, True)[1]
            elif hand[0] is 'A':
                # one of the cards is an ace
                action = R_soft(int(hand[1:]), card, 1, values, True)[1]
            elif len(hand) == 2 and hand[0] == hand[1]:
                # both same
                action = R_soft(int(hand[0]), card, 1, values, True)[1]
            elif hand == '1010':
                action = R_soft(10, card, 1, values, True)[1]
            else:
                # hard total
                action = R_hard(int(hand), card, 1, values, True)[1]
            policy[(hand, card)] = action

    return policy


def print_policy (policy):
    """
    Output the policy to the required output stream
    """
    f = open("Policy.txt", "w")
    for hand in player_hand:
        # if hand is 'A10' or hand is '20' or hand is '21':
            # continue
        f.write (hand + '\t')
        for card in dealer_card:
            action = policy[(hand, card)]
            f.write(action)
            if card is 'A' and hand is not 'AA':
                f.write('\n')
            elif card is not 'A':
                f.write(' ')


def dealer (player_sum, dealer_card, bet, hasBlackjack=False):
    """
    This function shall give the *expected* profit of the *player* when the face-up card 
    of the dealer is the `dealer_card`, the sum of player's hand is `player_sum`,
    and the player has chosen to 'stand'. `p`=face_card_prob is the probability of the face card
    `hasBlackJack` refers to the situation when the standing player has a blackjack, and if the dealer fails to 
    produce a blackjack player will get a profit of 1.5
    Take care to deal with cases where player_sum > 21, in which case return -1 i.e. player bust
    """

    if player_sum > 21:
        return -bet

    if dealer_card == 'A':
        dealer_sum = 11
    else:
        dealer_sum = int(dealer_card)
    return reward(dealer_sum, player_sum, face_card_prob, bet, hasBlackjack)


def calc_hand_sum(hand):
    """
    Calculate the sum of this hand
    Outputs (soft, hard) value
    """

    if hand[0] == 'A':
        if hand[1] == 'A': ## AA
            ## CONFIRM -> THREE VALUES POSSIBLE
            return (12, 2)
        elif len(hand) == 3: ## A10
            return (21, 11)
        else: ## Ax
            h = int(hand[1]) + 1
            return (h+10, h)

    elif hand == '1010': ## 1010
        return (20, 20)
    elif hand[0] == hand[1]: ## xx
        v = 2 * int(hand[0])
        return (v, v)
    else: ## x
        v = int(hand)
        return (v, v)


if __name__ == '__main__':
    """
    Main function
    """
    
    face_card_prob = float(sys.argv[1])
    num_card_prob = (1 - face_card_prob) / 9.0

    optimal_values = initialise_values()
    for i in range(5):
        optimal_values = value_iteration(optimal_values)
        print (i, 'th iteration complete')

    optimal_policy = get_policy(optimal_values)
    print_policy(optimal_policy)