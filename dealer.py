'''
This module gives the dealer functions to give the expected profit for the player.
The evaluation of Ace, and ~~the case of Blackjack for both dealer and player~~ haven't 
been covered yet.
'''

DEALER_CUTOFF = 17
BUSTED_CUTOFF = 21
PLAYER_BLACKJACK = False

def find_prob(player_sum, dealer_sum, p, num_cards): 
    """
    This function gives the probability that eventually after 
    performing consecutive Hit moves, the dealer sum exceeds or is 
    equal to the variable `player_sum`. The function returns a tuple of 
    probabilities:  
    Exceeding the player sum without busting, and  
    Dealer exceeds the busting limit, and  
    Push case (No profit, no loss), and  
    Player wins with a blackjack
    """
    
    # At each call of this function, it is judged if another hit move is required or not.
    # Accordingly, the probabilities are calculated for number, face and ace cards  

    if PLAYER_BLACKJACK and num_cards != 1:
        if num_cards == 2 and dealer_sum == player_sum:
            return (0, 0, 1, 0)
        else:
            return (0, 0, 0, 1)
    
    if dealer_sum > BUSTED_CUTOFF:
        return (0, 1, 0, 0)
    
    if dealer_sum > player_sum and dealer_sum <= BUSTED_CUTOFF:
        return (1, 0, 0, 0)
    elif dealer_sum == player_sum and dealer_sum >= DEALER_CUTOFF:
        # player_sum is assumed to be within bust limit.
        return (0, 0, 1, 0)
    elif dealer_sum >= DEALER_CUTOFF:
        # Dealer sum not surpassed player sum and not busted as well
        return (0, 0, 0, 0)

    # Make another Hit move for the dealer
    nobust_prob = 0
    bust_prob = 0
    push_prob = 0
    blackjack_prob = 0

    # Add the probabilities corresponding to various number, face and ace cards in the next hit move
    for card in range(2,12):
        if card is 10:
            # Add the probability of getting a Face Card in the next hit move
            face_prob_tuple = find_prob(player_sum, dealer_sum + 10, p, num_cards+1)
            nobust_prob = nobust_prob + p * face_prob_tuple[0]
            bust_prob = bust_prob + p * face_prob_tuple[1]
            push_prob = push_prob + p * face_prob_tuple[2]
            blackjack_prob = blackjack_prob + p * face_prob_tuple[3]
        else:
            prob_tuple = find_prob(player_sum, dealer_sum + card, p, num_cards+1)
            nobust_prob = nobust_prob + (1-p)/9 * prob_tuple[0]
            bust_prob = bust_prob + (1-p)/9 * prob_tuple[1]
            push_prob = push_prob + (1-p)/9 * prob_tuple[2]
            blackjack_prob = blackjack_prob + (1-p)/9 * prob_tuple[3]
    
    return (nobust_prob, bust_prob, push_prob, blackjack_prob)


def reward(face_up, player_sum, p, bet, has_blackjack):
    """ 
    This function gives the reward of the player when the
    face up card of the dealer is `face_up`, probability of face 
    card is `p`, and the player_sum of the player's cards is `player_sum`, 
    and the amount placed on bet is `bet`
    Also, `has_blackjack` argument is true if the player has a blackjack
    """ 

    PLAYER_BLACKJACK = has_blackjack

    if player_sum < DEALER_CUTOFF:
        return -bet
    elif player_sum > BUSTED_CUTOFF:
        return -bet
    else:
        prob_tuple = find_prob(player_sum, face_up, p, 1)
        nobust_prob = prob_tuple[0]
        bust_prob = prob_tuple[1]
        push_prob = prob_tuple[2]
        blackjack_prob = prob_tuple[3]
        simple_win_prob = (1-nobust_prob-push_prob-blackjack_prob)
        reward = simple_win_prob * bet + 1.5 * blackjack_prob * bet - nobust_prob * bet
        return reward
        