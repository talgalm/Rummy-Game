import pygame
import random

deck = []
player1 = []
player2 = []
cardOnTable = ''
turn = 0
table = []


class Card:
    def __init__(self, value, shape, index):
        self.value = value
        self.shape = shape
        self.index = index


def print_list(turn, player1, player2):
    player1Sort = sorted(player1, key=lambda Card: Card.index)
    player2Sort = sorted(player2, key=lambda Card: Card.index)
    if turn == 0:
        print('\nPlayer 1 cards: ')
        for i in player1Sort:
            print(i.value, i.shape)
    else:
        print('\nPlayer 2 cards: ')
        for i in player2Sort:
            print(i.value, i.shape)
    print(" ")


def create_deck():
    new_card = Card(0, 0, 0)
    shapes = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
    for x in range(2):
        for y in shapes:
            for z in range(1, 14):
                if z == 1:
                    deck.append(Card('A', y, z))
                elif 1 < z < 11:
                    deck.append(Card(str(z), y, z))
                elif z == 11:
                    deck.append(Card('Jack', y, z))
                elif z == 12:
                    deck.append(Card('Queen', y, z))
                else:
                    deck.append(Card('King', y, z))
        deck.append(Card('JOKER', '', 0))


def show_table(table):
    if len(table) != 0:
        print('The sets on the table are:')
        for i in table:
            for j in i:
                print('(', end='')
                print(j.value, j.shape, end=')')
            print('', end='\n')


def shuffle_cards():
    for x in range(14):
        new_card = random.randint(0, len(deck) - 1)
        player1.append(deck[new_card])
        deck.remove(deck[new_card])
        new_card = random.randint(0, len(deck) - 1)
        player2.append(deck[new_card])
        deck.remove(deck[new_card])


def pick_from_deck(deck, turn, player1, player2):
    print('You Picked from the deck: ', end="")

    if turn == 0:
        new_card = random.randint(0, len(deck) - 1)
        print(deck[new_card].value, deck[new_card].shape)
        player1.append(deck[new_card])
        deck.remove(deck[new_card])
    else:
        new_card = random.randint(0, len(deck) - 1)
        print(deck[new_card].value, deck[new_card].shape)
        player2.append(deck[new_card])
        deck.remove(deck[new_card])


def pick_table_card(turn, player1, player2, cardOnTable):
    if turn == 0:
        player1.append(cardOnTable)
    else:
        player2.append(cardOnTable)


def check_set(newSet):
    def same_shape(newSet):
        defineShape = newSet[0].shape
        defineValue = newSet[0].value
        for i in newSet:
            if i == newSet[0]:
                continue
            if defineShape == i.shape or defineValue != i.value:
                return False
        return True

    def regular_order(newSet):
        sortSet = sorted(newSet, key=lambda Card: Card.index)
        or2or13 = 0
        for c in sortSet:
            if c.index == 13:
                or2or13 = 13
        for j in sortSet:
            if j.index == 13:
                if or2or13 == 13:
                    sortSet.append(Card('A', j.shape, 14))
                    for r in sortSet:
                        if r.index == 1 and r.value == 'A':
                            sortSet.remove(r)
        currentVar = ''
        currentShp = ''
        for i in sortSet:
            if i == sortSet[0]:
                currentVar = i.index
                currentShp = i.shape
                continue
            else:
                if currentVar + 1 != i.index or currentShp != i.shape:
                    return False
            currentVar = i.index
        return True

    def set_with_joker(newSet):
        findJokerIndex = 0
        countJoker = 0
        sameShapeCheck = sorted(newSet, key=lambda Card: Card.index)
        for i in newSet:
            if i.index == 0:
                findJokerIndex = countJoker
                sameShapeCheck.remove(i)
            countJoker += 1
        if same_shape(sameShapeCheck) or regular_order(sameShapeCheck):
            return True
        findJokerCheck = newSet
        first = []
        last = []
        for x in range(findJokerIndex):
            first.append(findJokerCheck[x])
        for y in range(findJokerIndex + 1, len(newSet)):
            last.append(findJokerCheck[y])
        if regular_order(first) and regular_order(last):
            if first[len(first) - 1].index + 2 == last[0].index and newSet[findJokerIndex].index == 0:
                return True

    def set_with_2_joker(newSet):
        countJoker = 0
        lstJoker = []
        location = 0
        for i in newSet:
            if i.index == 0:
                countJoker += 1
                lstJoker.append(location)
            location += 1
        if countJoker == 2:
            first = []
            second = []
            for x in range(0, lstJoker[0] + 2):
                first.append(newSet[x])
            for y in range(lstJoker[0] + 1, ):
                second.append(newSet[y])
            if set_with_joker(first) and set_with_joker(second):
                return True

    if len(newSet) < 3:
        return False
    if same_shape(newSet):
        return True
    elif regular_order(newSet):
        return True
    elif set_with_joker(newSet):
        return True
    elif set_with_2_joker(newSet):
        return True
    else:
        return False


def find_index(card):
    if card.value == 'A':
        card.index = 1
    elif card.value == 'Jack':
        card.index = 11
    elif card.value == 'Queen':
        card.index = 12
    elif card.value == 'King':
        card.index = 13
    elif card.value == 'JOKER':
        card.index = 0
    else:
        for i in range(1, 11):
            if int(card.value) == i:
                card.index = i
    return card


def remove_set(turn, newSet, player1, player2):
    for i in newSet:
        check = 0
        if turn == 0:
            for j in player1:
                if i.index == j.index and i.value == j.value and i.shape == j.shape:
                    check += 1
                    if check == 1:
                        player1.remove(j)
        else:
            for j in player2:
                if i.index == j.index and i.value == j.value and i.shape == j.shape:
                    check += 1
                    if check == 1:
                        player2.remove(j)


def remove_card(turn, player1, player2, card):
    doubleCheck = 0
    if turn == 0:
        for i in player1:
            if card.value == i.value and card.shape == i.shape:
                doubleCheck +=1
                if doubleCheck == 1:
                    player1.remove(i)
    else:
        for i in player2:
            if card.value == i.value and card.shape == i.shape:
                doubleCheck += 1
                if doubleCheck == 1:
                    player2.remove(i)


def down(turn, player1, player2):
    validSet = False
    newSet = []
    numOfVar = 0
    while not validSet:
        checkVar = False
        try:
            cardValue, cardShape = input('Enter card ' or 'JOKER').split()
        except ValueError:
            cardValue = 'JOKER'
            cardShape = ''
        card = Card(cardValue, cardShape, 0)
        card = find_index(card)
        if turn == 0:
            for i in player1:
                if i.value == cardValue and i.shape == cardShape:
                    newSet.append(card)
                    numOfVar += 1
                    checkVar = True
        else:
            for i in player2:
                if i.value == cardValue and i.shape == cardShape:
                    newSet.append(card)
                    numOfVar += 1
                    checkVar = True
        if not checkVar:
            print('Card does not exist, please type again ')
            continue
        if numOfVar < 3:
            continue
        if input('finish set ? ') == 'No':
            continue
        else:
            for x in newSet:
                if newSet.count(x) > 1:
                    newSet.remove(x)
            if check_set(newSet):
                if turn == 0 and len(newSet) == len(player1) or turn == 1 and len(newSet) == len(player2):
                    print('You can not finish turn without drop card')
                    break
                table.append(newSet)
                remove_set(turn, newSet, player1, player2)
                print('New set on the table\n')
                validSet = True
            else:
                print('Invalid set, please enter again')
                newSet = []
                numOfVar = 0
        if input('Do you want to continue with another set ? ') == 'Yes':
            down(turn, player1, player2)


def paste(turn, player1, player2, table):
    def same_value(table, card):
        for x in table:
            for y in x:
                if y.shape == card.shape or y.index != card.index:
                    return False
            x.append(card)
            temp = sorted(x, key=lambda Card: Card.index)
            table.remove(x)
            table.append(temp)
            return True

    def regular(table, card):
        for m in table:
            for n in m:
                if n.index == 13 and card.index == 1 and n.shape == card.shape:
                    card.index == 14
        for x in table:
            if (card.index + 1 == x[0].index and card.shape == x[0].shape) or (
                    x[-1].index + 1 == card.index and card.shape == x[-1].shape):
                x.append(card)
                checkJ = False
                countJ = 0
                indexJ = 0
                for j in x:
                    if j.index == 0:
                        checkJ = True
                        indexJ = countJ
                    countJ+=1
                if checkJ:
                    x[indexJ].index = (x[indexJ+1].index + x[indexJ-1].index) / 2
                temp = sorted(x, key=lambda Card: Card.index)
                table.remove(x)
                table.append(temp)
                return True
        return False

    def this_is_joker(table, card, first, last):
        if card.value == 'JOKER':
            for x in table:
                if (first.value == x[0].value and first.shape == x[0].shape) and (
                        last.value == x[-1].value and last.shape == x[-1].shape):
                    pos = input('Paste the Joker Last or First ? ')
                    x.append(card)
                    if pos == 'First':
                        temp = sorted(x, key=lambda Card: Card.index)
                    else:
                        temp = x
                    table.remove(x)
                    table.append(temp)
                    return True
            return False

    def paste_on_joker(table, card, first, last):
        def color(tempSet, card):
            for z in tempSet:
                if card.index != z.index or card.shape == z.shape:
                    return False
            return True

        def row(tempSet, card):
            if card.index + 2 == tempSet[0].index and card.shape == tempSet[0].shape:
                return 'first'
            if card.index == tempSet[-1].index + 2 and card.shape == tempSet[-1].shape:
                return 'last'
            return False

        tempSet = []
        for x in table:
            if (first.value == x[0].value and first.shape == x[0].shape) or (
                    last.value == x[-1].value and last.shape == x[-1].shape):
                for y in x:
                    if y.index != 0:
                        tempSet.append(y)
                if row(tempSet, card) == 'first':
                    temp = []
                    temp.append(card)
                    temp = temp + x
                    table.remove(x)
                    table.append(temp)
                    return True
                elif row(tempSet, card) == 'last':
                    x.append(card)
                    temp = x
                    table.remove(x)
                    table.append(temp)
                    return True
                elif color(tempSet, card):
                    x.append(card)
                    temp = sorted(x, key=lambda Card: Card.index)
                    table.remove(x)
                    table.append(temp)
                    return True
        return False

    try:
        cardValue, cardShape = input('Enter card ' or ' ').split()
    except ValueError:
        cardValue = 'JOKER'
        cardShape = ''
    card = Card(cardValue, cardShape, 0)
    card = find_index(card)
    check = 'not'
    if turn == 0:
        for i in player1:
            if i.value == cardValue and i.shape == cardShape:
                check = 'in'

    else:
        for i in player2:
            if i.value == cardValue and i.shape == cardShape:
                check = 'in'
    if check == 'not':
        print('Card not found , please try again ')
        paste(turn, player1, player2, table)
    else:
        print('Enter first and last card on the set you want to paste: ')
        try:
            firstValue, firstShape = input('Enter first card ' or ' ').split()
        except ValueError:
            firstValue = 'JOKER'
            firstShape = ''
        try:
            lastValue, lastShape = input('Enter last card ' or ' ').split()
        except ValueError:
            lastShape = ''
            lastValue = 'JOKER'
        first = Card(firstValue, firstShape, 0)
        last = Card(lastValue, lastShape, 0)
        first = find_index(first)
        last = find_index(last)
        if same_value(table, card) or regular(table, card) or this_is_joker(table, card, first, last) or paste_on_joker(
                table, card, first, last):
            print('The card was pasted successfully')
            remove_card(turn, player1, player2, card)
            if input('Do you want to paste another card ? ') == 'Yes':
                paste(turn, player1, player2, table)
        else:
            print('The card is not suitable for any set, enter another card:')
            paste(turn, player1, player2, table)


def drop_card(deck, turn, player1, player2):
    try:
        cardValue, cardShape = input('\nEnter the card you want to drop ' or '').split()
    except ValueError:
        cardValue = 'JOKER'
        cardShape = ''
    card = Card(cardValue, cardShape, 0)
    card = find_index(card)
    if turn == 0:
        for i in player1:
            if i.value == cardValue and i.shape == cardShape:
                cardOnTable = i
                player1.remove(i)
                return cardOnTable

    else:
        for i in player2:
            if i.value == cardValue and i.shape == cardShape:
                cardOnTable = i
                player2.remove(i)
                return cardOnTable
    print('Card not found, please enter again ')
    return drop_card(deck, turn, player1, player2)

def main():
    create_deck()
    shuffle_cards()
    cardOnTable = deck[random.randint(0, len(deck) - 1)]
    deck.remove(cardOnTable)
    win = False
    turn = 0


    while not win:
        print_list(turn, player1, player2)
        print('Card on table - ', cardOnTable.value, cardOnTable.shape)
        wantFromDeck = input('Do you  want the card on the table ? ')
        print(" ")
        if wantFromDeck == 'No':
            pick_from_deck(deck, turn, player1, player2)
        else:
            pick_table_card(turn, player1, player2, cardOnTable)
        wantDown = input('Do you want to go down ? ')
        if wantDown == 'Yes':
            down(turn, player1, player2)
        show_table(table)
        if len(table):
            wantPaste = input('\nDo you want to paste card ?')
            if wantPaste == 'Yes':
                paste(turn, player1, player2, table)

        cardOnTable = drop_card(deck, turn, player1, player2)
        if len(player1) == 0:
            win = True
            print('The winner is player1 !')
        if len(player2) == 0:
            win = True
            print('The winner is player2 !')
        turn = (turn + 1) % 2


main()
