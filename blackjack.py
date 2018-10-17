"""
Artificial Intelligence (COL333) A4
An optimal policy for blackjack (casino card game) using MDP
"""

def dealer (player_sum, dealer_card, int p):
    """
    This function shall give the *expected* profit of the *player* when the face-up card 
    of the dealer is the `dealer_card`, the sum of player's hand is `player_sum`,
    and the player has chosen to 'stand'. `p` is the probability of the face card
    """

    ## Placeholder code
    if (dealer_card <= 11):
        # let's say dealer has high chance of winning
        return -1
    else:
        return 1



## The optimal policy -- key value pair of (states, value)
## State = (player_hand, dealer_card)
optimal_policy = {}
player_hand = ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 
                 '22', '33', '44', '55', '66', '77', '88', '99', '1010', 'AA']
dealer_card = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']

def initialise_policy():
    """
    Initialise the optimal policy
    Make all states reward 0
    Initialise the goal state rewards appropriately
    """



def calc_hand_sum(hand):
    """
    Calculate the sum of this hand
    Outputs (soft, hard) value
    """