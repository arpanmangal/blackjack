'''
This module gives the dealer functions to give the expected profit for the player.
The ~~evaluation of Ace~~, and ~~the case of Blackjack for both dealer and player~~ haven't 
been covered yet.
'''

DEALER_CUTOFF = 17
BUSTED_CUTOFF = 21
PLAYER_BLACKJACK = False
PROB = 0
PLAYER_SUM = 0
REWARDS = []
DEFAULT = float('inf')

for i in range(DEALER_CUTOFF, BUSTED_CUTOFF+1):
    sum_reward = []
    for card in range(2, 12):
        # 2-9 Numbers, 10 Face and 11 Ace
        sum_reward.append(DEFAULT)
    REWARDS.append(sum_reward)

def find_prob(dealer_sum, num_cards, is_soft): 
    """
    This function gives the probability that eventually after 
    performing consecutive Hit moves, the dealer sum exceeds or is 
    equal to the variable `PLAYER_SUM`. The function returns a tuple of 
    probabilities:  
    Exceeding the player sum without busting, and  
    Dealer exceeds the busting limit, and  
    Push case (No profit, no loss), and  
    Player wins with a blackjack
    """
    
    # At each call of this function, it is judged if another hit move is required or not.
    # Accordingly, the probabilities are calculated for number, face and ace cards  

    # print ("Starting for dealer_sum: {0} and player_sum: {1}.".format(dealer_sum, PLAYER_SUM)) # Debug

    if PLAYER_BLACKJACK and num_cards != 1:
        if num_cards == 2 and dealer_sum == PLAYER_SUM:
            # Both player and dealer have blackjack
            return (0, 0, 1, 0)
        else:
            # Dealer does not get a blackjack, player does
            return (0, 0, 0, 1)
    
    if dealer_sum > BUSTED_CUTOFF:
        if is_soft:
            # Dealer's hand is soft and is exceeding the limit. Take the ace as 1.
            return find_prob(dealer_sum-10, num_cards, False)
        else:
            # Dealer's hand is eithere hard or no ace present. Hence, dealer busted.
            return (0, 1, 0, 0)
    
    if dealer_sum > PLAYER_SUM and dealer_sum <= BUSTED_CUTOFF:
        return (1, 0, 0, 0)
    elif dealer_sum == PLAYER_SUM and dealer_sum >= DEALER_CUTOFF:
        # player_sum is assumed to be within bust limit.
        if PLAYER_SUM == BUSTED_CUTOFF and num_cards == 2:
            return (1, 0, 0, 0)
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
            face_prob_tuple = find_prob(dealer_sum + 10, num_cards+1, False)
            nobust_prob = nobust_prob + PROB * face_prob_tuple[0]
            bust_prob = bust_prob + PROB * face_prob_tuple[1]
            push_prob = push_prob + PROB * face_prob_tuple[2]
            blackjack_prob = blackjack_prob + PROB * face_prob_tuple[3]
        elif card is 11:
            # Add the probability of getting an ace
            prob_tuple = find_prob(dealer_sum + card, num_cards+1, True)
            nobust_prob = nobust_prob + (1-PROB)/9 * prob_tuple[0]
            bust_prob = bust_prob + (1-PROB)/9 * prob_tuple[1]
            push_prob = push_prob + (1-PROB)/9 * prob_tuple[2]
            blackjack_prob = blackjack_prob + (1-PROB)/9 * prob_tuple[3]
        else:
            # Add the probabilities corresponding to simple number cards
            prob_tuple = find_prob(dealer_sum + card, num_cards+1, False)
            nobust_prob = nobust_prob + (1-PROB)/9 * prob_tuple[0]
            bust_prob = bust_prob + (1-PROB)/9 * prob_tuple[1]
            push_prob = push_prob + (1-PROB)/9 * prob_tuple[2]
            blackjack_prob = blackjack_prob + (1-PROB)/9 * prob_tuple[3]
    
    ret_tuple = (nobust_prob, bust_prob, push_prob, blackjack_prob)
    # print ("Returning {0} for dealer_sum:{1}, player_sum:{2}".format(ret_tuple, dealer_sum, PLAYER_SUM)) # Debug
    return ret_tuple


def reward(face_up, player_sum, p, bet, has_blackjack):
    """ 
    This function gives the reward of the player when the
    face up card of the dealer is `face_up`, probability of face 
    card is `p`, and the player_sum of the player's cards is `player_sum`, 
    and the amount placed on bet is `bet`
    Also, `has_blackjack` argument is true if the player has a blackjack
    """ 

    global PLAYER_SUM
    global PROB

    PLAYER_BLACKJACK = has_blackjack
    PLAYER_SUM = player_sum
    PROB = p

    if PLAYER_SUM < DEALER_CUTOFF:
        return -bet
    elif PLAYER_SUM > BUSTED_CUTOFF:
        return -bet
    else:
        array_index = PLAYER_SUM - DEALER_CUTOFF
        if REWARDS[array_index][face_up-2] < DEFAULT:
            return REWARDS[array_index][face_up-2]

        prob_tuple = (0, 0, 0, 0)
        if face_up is 11:
            prob_tuple = find_prob(face_up, 1, True)
        else:
            prob_tuple = find_prob(face_up, 1, False)

        nobust_prob = prob_tuple[0]
        bust_prob = prob_tuple[1]
        push_prob = prob_tuple[2]
        blackjack_prob = prob_tuple[3]

        simple_win_prob = (1-nobust_prob-push_prob-blackjack_prob)
        reward = simple_win_prob * bet + 1.5 * blackjack_prob * bet - nobust_prob * bet

        REWARDS[array_index][face_up-2] = reward
        return reward
        