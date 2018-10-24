import ast

with open('console.txt', 'r') as file:
    l = (file.readlines())
    for lists in l:
        listsl = ast.literal_eval(lists)
        list_sum = 0
        soft = 0
        for card in listsl:
            list_sum += card
            if card == 11:
                soft+=1
            if list_sum > 21 and soft > 0:
                list_sum = list_sum - 10
                soft-=1
        if list_sum < 21:
            print (listsl, end=' ')
            print (list_sum)
    