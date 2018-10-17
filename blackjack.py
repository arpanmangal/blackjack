"""
Artificial Intelligence (COL333) A4
An optimal policy for blackjack (casino card game) using MDP
"""

import sys

## Policy is key value pair of (states, value)
## State = (player_hand, dealer_card)
player_hand = ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
                 '22', '33', '44', '55', '66', '77', '88', '99', '1010', 'AA']
dealer_card = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
face_card_prob = 4 / 13

def initialise_values():
    """
    Initialise and return initial policy values
    Make all states reward 0
    """

    values = {}
    for hand in player_hand:
        for card in dealer_card:
            values[(hand, card)] = 0

    return values


def value_iteration (current_values):
    """
    Performs one step of value iteration
    Computes next level of policy from current_values
    """
    return current_values # placeholder

def get_policy(values):
    """
    Get the corresponding policy, pi
    for the given values, V
    """
    
    policy = {}
    # placeholder
    for hand in player_hand:
        for card in dealer_card:
            policy[(hand, card)] = 'H'

    return policy


def print_policy (policy):
    """
    Output the policy to the required output stream
    """
    f = open("Policy.txt", "w")
    for hand in player_hand:
        if hand is 'A10':
            continue
        f.write (hand + '\t')
        for card in dealer_card:
            action = policy[(hand, card)]
            f.write(action)
            if card is 'A' and hand is not 'AA':
                f.write('\n')
            elif card is not 'A':
                f.write(' ')


def dealer (player_sum, dealer_card):
    """
    This function shall give the *expected* profit of the *player* when the face-up card 
    of the dealer is the `dealer_card`, the sum of player's hand is `player_sum`,
    and the player has chosen to 'stand'. `p`=face_card_prob is the probability of the face card
    """

    ## Placeholder code
    if (dealer_card <= 11):
        # let's say dealer has high chance of winning
        return -1
    else:
        return 1


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
    
    face_card_prob = sys.argv[1]

    optimal_values = initialise_values()
    for i in range(100):
        optimal_values = value_iteration(optimal_values)

    optimal_policy = get_policy(optimal_values)
    print_policy(optimal_policy)