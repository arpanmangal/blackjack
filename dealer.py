'''
This module gives the dealer functions to give the expected profit for the player.
The evaluation of Ace, and the case of Blackjack for both dealer and player haven't 
been covered yet.
'''

DEALER_CUTOFF = 17
BUSTED_CUTOFF = 21

# face_card_prob = p

def find_prob(player_sum, dealer_sum, p):
    """
    This function gives the probability that eventually after 
    performing consecutive Hit moves, the dealer sum exceeds or is 
    equal to the variable 'player_sum'. The function returns a tuple of 
    probabilities: 
    Exceeding the player sum without busting, and 
    Dealer exceeds the busting limit, and
    Push case (No profit, no loss) 
    """
    
    # At each call of this function, it is judged if another hit move is required or not.
    # Accordingly, the probabilities are calculated for number, face and ace cards
    
    if dealer_sum > BUSTED_CUTOFF:
        return (0, 1, 0)
    
    if dealer_sum > player_sum and dealer_sum <= BUSTED_CUTOFF:
        return (1, 0, 0)
    elif dealer_sum == player_sum and dealer_sum >= DEALER_CUTOFF:
        # player_sum is assumed to be within bust limit.
        return (0, 0, 1)
    elif dealer_sum >= DEALER_CUTOFF:
        # Dealer sum not surpassed player sum and not busted as well
        return (0, 0, 0)

    # Make another Hit move for the dealer
    nobust_prob = 0
    bust_prob = 0
    push_prob = 0

    # Add the probabilities corresponding to various number cards in the next hit move
    for card in range(2,10):
        prob_tuple = find_prob(player_sum, dealer_sum + card, p)
        nobust_prob = nobust_prob + (1-p)/9 * prob_tuple[0]
        bust_prob = bust_prob + (1-p)/9 * prob_tuple[1]
        push_prob = push_prob + (1-p)/9 * prob_tuple[2]
    
    # Add the probability of getting a Face Card in the next hit move
    face_prob_tuple = find_prob(player_sum, dealer_sum + 10, p)
    nobust_prob = nobust_prob + p * face_prob_tuple[0]
    bust_prob = bust_prob + p * face_prob_tuple[1]
    push_prob = push_prob + p * face_prob_tuple[2]

    # Add the probability of getting an Ace Card in the next hit move
    # TODO: Currently taking Ace to be 11. How to check in player's favour?
    ace_prob_tuple = find_prob(player_sum, dealer_sum + 11, p)
    nobust_prob = nobust_prob + (1-p)/9 * ace_prob_tuple[0]
    bust_prob = bust_prob + (1-p)/9 * ace_prob_tuple[1]
    push_prob = push_prob + (1-p)/9 * ace_prob_tuple[2]

    return (nobust_prob, bust_prob, push_prob)


def reward(face_up, player_sum, p, bet):
    """ 
    This function gives the reward of the player when the
    face up card of the dealer is 'face_up', probability of face 
    card is 'p', and the player_sum of the player's cards is 'player_sum', and the
    amount placed on bet is 'bet'
    """ 
    
    if player_sum < DEALER_CUTOFF:
        return -bet
    elif player_sum > BUSTED_CUTOFF:
        return -bet
    else:
        prob_tuple = find_prob(player_sum, face_up, p)
        nobust_prob = prob_tuple[0]
        bust_prob = prob_tuple[1]
        push_prob = prob_tuple[2]
        win_prob = (1-nobust_prob-push_prob)
        reward = win_prob * bet - nobust_prob * bet
        return reward
        