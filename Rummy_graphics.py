import pygame
import random
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import time
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Card:
    def __init__(self, value, shape, index, point, click, picture):
        self.value = value
        self.shape = shape
        self.index = index
        self.point = point
        self.click = click
        self.picture = picture


def chooseOpponent(screen, background_image2, display2, display3, display4, back):
    screen.blit(background_image2, [0, 0])
    nop = pygame.image.load("pics/nop.png").convert()
    screen.blit(nop, [600, 250])
    two = pygame.image.load(display2).convert()
    screen.blit(two, [600, 300])
    three = pygame.image.load(display3).convert()
    screen.blit(three, [650, 300])
    four = pygame.image.load(display4).convert()
    screen.blit(four, [700, 300])
    for i in range(14):
        screen.blit(back, [500 + i * 25, 550])
    if display2 == "pics/twob.png" or display3 == "pics/threeb.png" or display4 == "pics/fourb.png":
        displayPlay = pygame.image.load("pics/play.png").convert()
        screen.blit(displayPlay, [600, 375])
    if display2 == "pics/twob.png":
        for i in range(14):
            screen.blit(back, [500 + i * 25, 25])
    if display3 == "pics/threeb.png":
        for i in range(14):
            screen.blit(back, [500 + i * 25, 25])
        back2 = pygame.transform.rotate(back, 90)
        for i in range(14):
            screen.blit(back2, [50, 150 + i * 25])
    if display4 == "pics/fourb.png":
        for i in range(14):
            screen.blit(back, [500 + i * 25, 25])
        back2 = pygame.transform.rotate(back, 90)
        for i in range(14):
            screen.blit(back2, [50, 150 + i * 25])
        for i in range(14):
            screen.blit(back2, [1200, 150 + i * 25])


def create_deck(deck):
    new_card = Card(0, 0, 0, Point(0, 0), False, '')
    shapes = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
    for x in range(2):
        for y in shapes:
            for z in range(1, 14):
                if z == 1:
                    deck.append(Card('A', y, z, Point(0, 0), False, ''))
                elif 1 < z < 11:
                    deck.append(Card(str(z), y, z, Point(0, 0), False, ''))
                elif z == 11:
                    deck.append(Card('Jack', y, z, Point(0, 0), False, ''))
                elif z == 12:
                    deck.append(Card('Queen', y, z, Point(0, 0), False, ''))
                else:
                    deck.append(Card('King', y, z, Point(0, 0), False, ''))
        deck.append(Card('JOKER', '', 0, Point(0, 0), False, ''))
    for y in deck:
        if y.index == 0:
            y.picture = 'pics/' + 'JOKER.png'
        else:
            y.picture = 'pics/' + y.value + ' ' + y.shape + '.png'


def shuffle_cards(deck, player1, player2, player3, player4, nop):
    for x in range(14):
        new_card = random.randint(0, len(deck) - 1)
        player1.append(deck[new_card])
        deck.remove(deck[new_card])
        new_card = random.randint(0, len(deck) - 1)
        player2.append(deck[new_card])
        deck.remove(deck[new_card])
        if nop > 2:
            new_card = random.randint(0, len(deck) - 1)
            player3.append(deck[new_card])
            deck.remove(deck[new_card])
        if nop > 3:
            new_card = random.randint(0, len(deck) - 1)
            player4.append(deck[new_card])
            deck.remove(deck[new_card])


def pick_from_deck(deck, player):
    new_card = random.randint(0, len(deck) - 1)
    player.append(deck[new_card])
    deck.remove(deck[new_card])


def pick_table_card(player, cardOnTable):
    player.append(cardOnTable)


def check_set(newSet):
    def same_color(newSet):
        numClubs = 0
        numHearts = 0
        numDiamonds = 0
        numSpades = 0
        if len(newSet) <1:
            return False
        numVar = newSet[0].value
        for i in newSet:
            if i.value != numVar:
                return False
            if i.shape == 'Clubs':
                numClubs += 1
            if i.shape == 'Diamonds':
                numDiamonds += 1
            if i.shape == 'Hearts':
                numHearts += 1
            if i.shape == 'Spades':
                numSpades += 1
        if numClubs > 1 or numDiamonds > 1 or numHearts > 1 or numSpades > 1:
            return False
        return True

    def order(newSet):
        indexes = []
        shape = newSet[0].shape
        for i in newSet:
            indexes.append(i.index)
            if i.shape != shape:
                return False
        for i in range(0, len(newSet) - 1):
            if indexes[i] + 1 != indexes[i + 1]:
                return False
        return True

    def king_a_order(newSet):
        kingCheck = False
        aCheck = False
        twoCheck = False
        for f in newSet:
            if f.index == 13:
                kingCheck = True
            if f.value == 'A':
                aCheck = True
            if f.index == 2:
                twoCheck = True
        saved = 0
        if aCheck and kingCheck:
            for n in newSet:
                if n.value == 'A':
                    saved = n.index
                    n.index = 14
            newSet = sorted(newSet, key=lambda Card: Card.index)
            if order(newSet):
                return True
            else:
                for n in newSet:
                    if n.value == 'A':
                        n.index = saved
                return False
        else:
            return False

    def with_joker(newSet):
        countJ = 0
        for i in newSet:
            if i.value == 'JOKER':
                countJ += 1
        if countJ == 0:
            return False
        woj = []
        for w in newSet:
            if w.value != 'JOKER':
                woj.append(w)
        if same_color(woj):
            newSet[0].index = newSet[-1].index
            return True
        elif order(woj):
            newSet[0].index = newSet[1].index - 1
            return True
        elif king_a_order(woj):
            newSet[0] = newSet[1].index - 1
            return True
        else:
            first = newSet[1]
            for i in range(2, len(newSet)):
                if first.index + 1 != newSet[i].index:
                    change = Card('JOKER', newSet[i].shape, first.index + 1, Point(0, 0), True, 'JOKER.PNG')
                    woj.append(change)
                    woj = sorted(woj, key=lambda Card: Card.index)
                    if order(woj):
                        newSet[0].index = first.index + 1
                        newSet[0].shape = first.shape
                        return True
                    else:
                        return False
                else:
                    first = newSet[i]

    newSet = sorted(newSet, key=lambda Card: Card.index)
    if same_color(newSet):
        return True
    if order(newSet):
        return True
    if king_a_order(newSet):
        return True
    if with_joker(newSet):
        return True


def remove_set(player):
    countForVar = 0
    temp = []
    for j in player:
        if j.click:
            temp.append(j)
    for z in temp:
        for g in player:
            if z.value == g.value and z.shape == g.shape and z.click and countForVar == 0:
                player.remove(g)
                countForVar = 1
        countForVar = 0


def remove_card(player, card):
    doubleCheck = 0
    for i in player:
        if i.click and i.shape == card.shape and i.index == card.index:
            player.remove(i)
            break


def down(table, player):
    validSet = False
    newSet = []
    for i in player:
        if i.click:
            newSet.append(i)
    if len(newSet) > 2:
        if check_set(newSet):
            if len(newSet) == len(player):
                return False
            table.append(newSet)
            remove_set(player)
            return True
        else:
            clean_click(player)
            return False


def remove_com(player, ns):
    count = 0
    for i in ns:
        for j in player:
            if i.index == j.index and i.shape == j.shape and count == 0:
                player.remove(i)
                count += 1
        count = 0
    return player


def paste(player, table):
    pos = pygame.mouse.get_pos()
    areaFX = 0
    areaLX = 0
    areaLY = 0
    areaRY = 0
    temp = []
    count = 0
    for i in player:
        if i.click:
            for j in table:
                for z in j:
                    temp.append(z)
                j = sorted(j, key=lambda Card: Card.index)
                areaFX = j[0].point.x
                areaLX = j[-1].point.x + 25
                areaFY = j[0].point.y
                areaLY = j[0].point.y + 93
                if areaFX < pos[0] < areaLX and areaFY < pos[1] < areaLY:
                    temp.append(i)
                    if check_set(temp):
                        return count
                temp = []
                count += 1
    return 100


def show_player1(screen, player1):
    # back = pygame.transform.rotate(back, angle)
    player = sorted(player1, key=lambda Card: Card.index)
    player_position = pygame.mouse.get_pos()
    cardsX = 500
    cardsY = 550
    add = 0
    for i in player:
        cardDisplay = pygame.image.load(i.picture).convert()
        if not i.click:
            screen.blit(cardDisplay, [cardsX, cardsY])
            i.point.x = cardsX
            i.point.y = cardsY
        else:
            screen.blit(cardDisplay, [player_position[0] + add, player_position[1]])
            i.point.x = player_position[0]
            i.point.y = player_position[1]
            add += 10
        cardsX = cardsX + 25


def show_cards_on_table(screen, cardOnTable, takeTableCard):
    if not takeTableCard:
        cardDisplay = pygame.image.load(cardOnTable.picture).convert()
        screen.blit(cardDisplay, [222, 289])
    else:
        empty = pygame.image.load('pics/empty.png').convert()
        screen.blit(empty, [222, 289])


def click_card(player, pos):
    count = 0
    for i in player:
        if i.point.x < pos[0] < i.point.x + 25 and i.point.y < pos[1] < i.point.y + 93:
            i.click = True


def click_card_table(table, pos):
    for j in table:
        for i in j:
            if i.point.x < pos[0] < i.point.x + 25 and i.point.y < pos[1] < i.point.y + 93:
                i.click = True


def find_card(player):
    for i in player:
        if i.click:
            return i


def update_table(screen, table):
    posX = 325
    posY = 150
    countSets = 0
    player_position = pygame.mouse.get_pos()
    check2 = False
    check13 = False
    for j in table:
        j = sorted(j, key=lambda Card: Card.index)
        for i in j:
            if i.index == 2:
                check2 = True
            if i.index == 13:
                check13 = True
            if i.value == 'A' and check2:
                i.index = 1
            if i.value == 'A' and check13:
                i.index = 14
        if countSets == 4:
            posX = 325
            posY = 250
        if countSets == 8:
            posX = 325
            posY = 350
        if countSets == 12:
            posX = 325
            posY = 450
        for i in j:
            cardDisplay = pygame.image.load(i.picture).convert()
            if not i.click:
                screen.blit(cardDisplay, [posX, posY])
                i.point.x = posX
                i.point.y = posY
            else:
                screen.blit(cardDisplay, [player_position[0], player_position[1]])
                i.point.x = player_position[0]
                i.point.y = player_position[1]
            posX = posX + 25
        posX = posX + 75
        countSets += 1
        check2 = False
        check13 = False


def clean_click(player):
    for c in player:
        c.click = False


def change_between_sets(table):
    for j in table:
        rep = []
        temp = []
        jokerOn = False
        for i in j:
            if i.click:
                rep.append(i)
                for l in j:
                    if l.value == 'JOKER':
                        jokerOn = True
            else:
                temp.append(i)
        if len(rep) != 0:
            if not check_set(temp):
                return False
            else:
                posP = paste(rep, table)
                if posP != 100 and not jokerOn:
                    for i in rep:
                        if i.click:
                            table[posP].append(i)
                            j.remove(i)
                            return True
                else:
                    return False


def change_sets_and_player(table, player):
    cardsFromPlayer = []
    cardsFromTable = []
    leftover = []
    newSet = []
    for p in player:
        if p.click:
            cardsFromPlayer.append(p)
    for t1 in table:
        for t2 in t1:
            if t2.click:
                cardsFromTable.append(t2)
            else:
                leftover.append(t2)
        if len(t1) > 7:
            if check_set(leftover) and check_set(cardsFromTable):
                for c in cardsFromTable:
                    for s in t1:
                        if c.index == s.index and c.shape == s.shape:
                            t1.remove(s)
                return cardsFromTable
        elif len(cardsFromTable) != 0:
            if check_set(leftover):
                for t3 in cardsFromTable:
                    newSet.append(t3)
                    for t4 in t1:
                        if t3.index == t4.index and t3.shape == t4.shape:
                            t1.remove(t4)
        cardsFromTable = []
        leftover = []
    for c in cardsFromPlayer:
        newSet.append(c)
    if check_set(newSet):
        for p in player:
            if p.click:
                player.remove(p)
        # table.append(newSet)
        return newSet
    else:
        temp = []
        for n in newSet:
            for t1 in table:
                for t2 in t1:
                    temp.append(t2)
                temp.append(n)
                if check_set(temp):
                    t1.append(n)
                    newSet.remove(n)
                temp = []
            temp = []
        return temp


def count_clicks(table, player):
    p = 0
    t = 0
    for i in player:
        if i.click:
            p += 1
    if len(table) != 0:
        for a in table:
            for b in a:
                if b.click:
                    t += 1
    return t, p


def click_empty(table, pos):
    for a in table:
        for b in a:
            if b.point.x < pos[0] < b.point.x + 25 and b.point.y < pos[1] < b.point.y + 93:
                return True
    return False


def down_com(player, s, table):
    for i in s:
        if check_set(i):
            table.append(i)
            remove_com(player, i)
    return player


def paste_com(p, table):
    count = 0
    temp = []
    if p.value != 'JOKER':
        for i in table:
            for j in i:
                temp.append(j)
            temp.append(p)
            if check_set(temp):
                return count
            temp = []
            count += 1
        return 100
    else:
        return 100


def duplicate_cards(player, table):
    count1 = 0
    count2 = 0
    for p in player:
        if p.click:
            for t1 in table:
                for t2 in t1:
                    if p.index == t2.index and p.shape == t2.shape and t2.click == True:
                        t2.click = False
                        return count1, count2
                    count2 += 1
                count1 += 1
    return 100, 100


def necessary(player, cod, pairs, unnecessary):
    temp = []
    temp = []
    for p in pairs:
        for l in p:
            temp.append(l)
        temp.append(cod)
        if check_set(temp):
            return True
    theShape = cod.shape
    theValue = cod.index
    first = False
    last = False
    for i in player:
        if i.shape == theShape:
            if i.index == theValue + 1:
                last = True
            if i.index + 1 == theValue:
                first = True
    if first and last:
        return True
    for u in unnecessary:
        if u.index == cod.index:
            if u.shape != cod.shape:
                return True
        if u.shape == cod.shape:
            if u.index + 1 == cod.index or u.index == cod.index + 1:
                return True
            if (u.index == 13 and cod.index == 1) or (u.index == 1 and cod.index == 13):
                return True
    return False


def find_card_to_drop(player, unnecessary, pairs, cardOnTable):
    check = True
    countJ = 0
    if len(unnecessary) != 0 and check:
        while len(unnecessary) != 0:
            if len(unnecessary) == 1 and unnecessary[0].value == 'JOKER':
                break
            for j in unnecessary:
                if j.value == 'JOKER':
                    countJ += 1
            if countJ > 100:
                break
            if countJ == len(unnecessary):
                check = False
            cod = unnecessary[random.randint(0, len(unnecessary) - 1)]
            if cod.value != 'JOKER':
                if cardOnTable.index == cod.index and cardOnTable.shape == cod.shape:
                    if len(unnecessary) == 1:
                        if cod.value == 'A':
                            cod.index = 1
                        return cod
                else:
                    if cod.value == 'A':
                        cod.index = 1
                    return cod
    count = 0
    compare = 20
    cod = player[0]
    for i in player:
        for p1 in pairs:
            for p2 in p1:
                if p2.index == i.index and p2.shape == i.shape:
                    count += 1
        if count < compare:
            compare = count
            cod = i
        count = 0
    return cod


def find_pairs(player):
    player = sorted(player, key=lambda Card: Card.index)
    one = False
    two = False
    three = False
    p = []
    newPair = []
    unnecessary = []
    for i in range(len(player) - 2):
        for j in range(i + 1, len(player) - 1):
            if player[i].index == player[j].index and player[i].shape != player[j].shape:
                p = [player[i], player[j]]
                newPair.append(p)
                one = True
            if player[i].shape == player[j].shape and player[i].index + 1 == player[j].index:
                p = [player[i], player[j]]
                newPair.append(p)
                one = True
            if player[i].shape == player[j].shape and player[i].index == 1 and player[j].index == 13:
                p = [player[i], player[j]]
                newPair.append(p)
                one = True
        if not one:
            for p in newPair:
                if p[0].index == player[i].index and p[0].shape == player[i].shape:
                    two = True
                if p[1].index == player[i].index and p[1].shape == player[i].shape:
                    two = True
            if not two:
                unnecessary.append(player[i])
        one = False
        two = False
    check = False
    for p in player:
        for s1 in newPair:
            for s2 in s1:
                if p.index == s2.index and p.shape == s2.shape:
                    nothing = 0
                    check = True
        if not check:
            unnecessary.append(p)
        check = False
    return newPair, unnecessary


def find_sets(player):
    dup = []
    for d in player:
        dup.append(d)
    seria = []
    temp = []
    sameShape = []
    pos = 0
    check = False
    shapes = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
    for s in shapes:
        for q in player:
            if s == q.shape:
                sameShape.append(q)
        if len(sameShape) != 0:
            sameShape = sorted(sameShape, key=lambda Card: Card.index)
            pos = sameShape[0]
            temp.append(pos)
            for k in range(1, len(sameShape)):
                if pos.index == sameShape[k].index:
                    continue
                if pos.index + 1 == sameShape[k].index:
                    temp.append(sameShape[k])
                    pos = sameShape[k]
                else:
                    if len(temp) > 2:
                        seria.append(temp)
                        check = True
                    pos = sameShape[k]
                    temp = [pos]
            if len(temp) > 2:
                seria.append(temp)
        sameShape = []
        temp = []
    for s1 in seria:
        for s2 in s1:
            for d in dup:
                if d.index == s2.index and d.shape == s2.shape:
                    dup.remove(d)
    for n in range(1, 14):
        sameValue = []
        count = 0
        temp = []
        for p in dup:
            if p.index == n:
                count += 1
                sameValue.append(p)
        c, d, h, s = 0, 0, 0, 0
        for o in sameValue:
            if o.shape == 'Clubs':
                c += 1
                if c == 1:
                    temp.append(o)
            if o.shape == 'Diamonds':
                d += 1
                if d == 1:
                    temp.append(o)
            if o.shape == 'Hearts':
                h += 1
                if h == 1:
                    temp.append(o)
            if o.shape == 'Spades':
                s += 1
                if s == 1:
                    temp.append(o)
        if len(temp) > 2:
            seria.append(temp)
    return seria


def jokerIn(player, sets, pairs):
    temp = []
    for p in player:
        if p.value == 'JOKER':
            if len(pairs) != 0:
                for i in pairs:
                    for j in i:
                        temp.append(j)
                    temp.append(p)
                    if check_set(temp):
                        sets.append(temp)
                        return sets
    return sets


def pair_and_table_set_com(player, table, pairs):
    newPair = []
    rest = []
    card = 0
    pos = 0

    for p1 in pairs:
        for p2 in p1:
            newPair.append(p2)
        for t in table:
            if len(t) > 3:
                pos = 0
                for t2 in range(len(t)):
                    if t2 == pos:
                        card = t[pos]
                    else:
                        rest.append(t[pos])
                newPair.append(card)
                if check_set(newPair) and check_set(rest) and len(player) != 2:
                    t.remove(t[pos])
                    table.append(newPair)
                    for p in player:
                        if p.index == p1[0].index and p.shape == p1[0].shape:
                            player.remove(p)
                        if p.index == p1[1].index and p.shape == p1[1].shape:
                            player.remove(p)
                    pairs.remove(p1)
                    return True
                else:
                    newPair.remove(card)
                    rest = []
                    card = 0
                    pos += 1
            newPair = []
            pos = 0
    return False


def computer_turn(deck, player, cardOnTable, table):
    player = sorted(player, key=lambda Card: Card.index)
    sets = []
    unnecessary = []
    pairs = []
    pairs, unnecessary = find_pairs(player)
    if necessary(player, cardOnTable, pairs, unnecessary) or cardOnTable.value == 'JOKER':
        pick_table_card(player, cardOnTable)
    else:
        pick_from_deck(deck, player)
    pairs, unnecessary = find_pairs(player)
    player = sorted(player, key=lambda Card: Card.index)
    sets = find_sets(player)
    if len(pairs) < 3:
        sets = jokerIn(player, sets, pairs)
    countNumSets = 0
    for i in sets:
        for j in i:
            countNumSets += 1
    if countNumSets != len(player):
        player = down_com(player, sets, table)
    for p in player:
        pasteCard = paste_com(p, table)
        if pasteCard != 100 and len(player) != 0:
            table[pasteCard].append(p)
            player.remove(p)
    if pair_and_table_set_com(player, table, pairs):
        print('true')
    pairs, unnecessary = find_pairs(player)
    # ùìà éåøéã ëàùø ðùàø 1
    dc = find_card_to_drop(player, unnecessary, pairs, cardOnTable)
    return player, dc


def main():
    numberOfPlayers = 1
    deck = []
    player1 = []
    player2 = []
    player3 = []
    player4 = []
    cardOnTable = ''
    turn = 0
    table = []
    create_deck(deck)
    cardOnTable = deck[random.randint(0, len(deck) - 1)]
    deck.remove(cardOnTable)
    pygame.init()
    screen = pygame.display.set_mode([1375, 725])
    pygame.display.set_caption('RUMMY - GAME')
    pygame.display.flip()
    clock = pygame.time.Clock()
    background_image = pygame.image.load("pics/pback.jpg").convert()
    background_image2 = pygame.image.load("pics/pback.jpg").convert()
    back = pygame.image.load('pics/back.jpg').convert()
    win = False
    turn = 0
    pickCard = False
    takeTableCard = False
    doubleClick = False
    pickNumberOfPlayers = False
    display2 = "pics/two.png"
    display3 = "pics/three.png"
    display4 = "pics/four.png"
    while not win:
        pickCard = False
        takeTableCard = False
        doubleClick = False
        while turn == 0:
            player_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    win = True
                    turn = 10
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    press = pygame.mouse.get_pressed()
                    if press[2] == 1:
                        clean_click(player1)
                        for a in table:
                            clean_click(a)
                    if 222 < player_position[0] < 297 and 190 < player_position[1] < 283 and press[0] == 1: #ùéðåé
                        if not pickCard:
                            pick_from_deck(deck, player1)
                            pickCard = True
                    elif 222 < player_position[0] < 297 and 289 < player_position[1] < 289 + 93 and press[0] == 1: #ùéðåé
                        toDrop = 0
                        for i in player1:
                            if i.click:
                                toDrop = 1
                        if not pickCard:
                            pick_table_card(player1, cardOnTable)
                            pickCard = True
                            takeTableCard = True
                            doubleClick = True
                        elif not doubleClick or toDrop == 1:
                            doubleClick = True
                            takeTableCard = False
                            cardOnTable = find_card(player1)
                            player1.remove(cardOnTable)
                            turn = 1
                            clean_click(player1)
                    elif 300 < player_position[0] < 1100 and 130 < player_position[1] < 500 and press[0] == 1:
                        if pickCard:
                            click_card_table(table, player_position)
                            tc, pc = count_clicks(table, player1)
                            if len(table) != 0 and pc == 1:
                                if pc == len(player1):
                                    Tk().wm_withdraw()  # to hide the main window
                                    messagebox.showerror('Error', 'You must drop card in end of turn')
                                    clean_click(player1)
                                else:
                                    posP = paste(player1, table)
                                    if posP != 100:
                                        for i in player1:
                                            if i.click:
                                                table[posP].append(i)
                                                player1.remove(i)
                                                for a in table:
                                                    clean_click(a)
                            if pc != 0 and tc == 0:
                                if down(table, player1):
                                    clean_click(player1)
                                    for a in table:
                                        clean_click(a)
                                    update_table(screen, table)
                            if pc == 0 and tc != 0:
                                if change_between_sets(table):
                                    for a in table:
                                        clean_click(a)
                                    update_table(screen, table)

                            # ùéðåé îëàï åäìàä
                            if (pc != 0 and tc != 0 and pc + tc > 2) or tc == 3:
                                if not click_empty(table, player_position):
                                    moves = change_sets_and_player(table, player1)
                                    if len(moves) != 0:
                                        table.append(moves)
                                    for a in table:
                                        clean_click(a)
                                    update_table(screen, table)
                        elif not pickNumberOfPlayers:
                            if 600 < player_position[0] < 700 and 300 < player_position[1] < 350:
                                display2 = "pics/twob.png"
                                display3 = "pics/three.png"
                                display4 = "pics/four.png"
                                numberOfPlayers = 2
                            if 650 < player_position[0] < 750 and 300 < player_position[1] < 350:
                                display2 = "pics/two.png"
                                display3 = "pics/threeb.png"
                                display4 = "pics/four.png"
                                numberOfPlayers = 3
                            if 700 < player_position[0] < 800 and 300 < player_position[1] < 350:
                                display2 = "pics/two.png"
                                display3 = "pics/three.png"
                                display4 = "pics/fourb.png"
                                numberOfPlayers = 4
                            if 600 < player_position[0] < 800 and 375 < player_position[1] < 400:
                                pickNumberOfPlayers = True
                                shuffle_cards(deck, player1, player2, player3, player4, numberOfPlayers)
                    elif 400 < player_position[0] < 900 and 550 < player_position[1] < 650 and press[0] == 1:
                        if pickCard:
                            click_card(player1, player_position)
            if not pickNumberOfPlayers:
                chooseOpponent(screen, background_image2, display2, display3, display4, back)
            else:
                screen.blit(background_image, [0, 0])
                screen.blit(back, [222, 190])
                update_table(screen, table)
                for i in range(len(player2)):
                    screen.blit(back, [500 + i * 25, 25])
                if numberOfPlayers > 2:
                    back2 = pygame.transform.rotate(back, 90)
                    for i in range(len(player3)):
                        screen.blit(back2, [50, 150 + i * 25])
                if numberOfPlayers > 3:
                    back2 = pygame.transform.rotate(back, 90)
                    for i in range(len(player4)):
                        screen.blit(back2, [1200, 150 + i * 25])
                show_cards_on_table(screen, cardOnTable, takeTableCard)
                show_player1(screen, player1)
            pygame.display.flip()
            clock.tick(60)
            if len(player1) == 0 and pickNumberOfPlayers:
                Tk().wm_withdraw()  # to hide the main window
                messagebox.showinfo('Game Over', 'Player 1 Wins !')
                win = True
                turn = 10
        cardOnTable.click = False
        pickCard = False
        takeTableCard = False
        doubleClick = False
        pygame.display.flip()
        # player 2
        while turn == 1:
            player_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    win = True
                    turn = 10
            screen.blit(background_image, [0, 0])
            screen.blit(back, [222, 190])
            update_table(screen, table)
            for i in range(len(player2)):
                screen.blit(back, [500 + i * 25, 25])
            if numberOfPlayers > 2:
                back2 = pygame.transform.rotate(back, 90)
                for i in range(len(player3)):
                    screen.blit(back2, [50, 150 + i * 25])
            if numberOfPlayers > 3:
                back2 = pygame.transform.rotate(back, 90)
                for i in range(len(player3)):
                    screen.blit(back2, [1200, 150 + i * 25])
            show_cards_on_table(screen, cardOnTable, takeTableCard)
            show_player1(screen, player1)
            op = pygame.image.load('pics/op.png').convert()
            screen.blit(op, [600, 280])
            pygame.display.flip()
            time.sleep(3)
            player2, cardOnTable = computer_turn(deck, player2, cardOnTable, table)
            player2.remove(cardOnTable)
            show_cards_on_table(screen, cardOnTable, takeTableCard)
            if numberOfPlayers == 2:
                turn = 0
            if numberOfPlayers > 2:
                turn = 2
            clean_click(player2)
            if len(player2) == 0:
                Tk().wm_withdraw()  # to hide the main window
                messagebox.showinfo('Game Over', 'Player 2 Wins !')
                win = True
                turn = 10
        cardOnTable.click = False
        # player 3
        while turn == 2:
            player_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    win = True
                    turn = 10
            screen.blit(background_image, [0, 0])
            screen.blit(back, [222, 190])
            update_table(screen, table)
            for i in range(len(player2)):
                screen.blit(back, [500 + i * 25, 25])
            if numberOfPlayers > 2:
                back2 = pygame.transform.rotate(back, 90)
                for i in range(len(player3)):
                    screen.blit(back2, [50, 150 + i * 25])
            if numberOfPlayers > 3:
                back2 = pygame.transform.rotate(back, 90)
                for i in range(len(player3)):
                    screen.blit(back2, [1200, 150 + i * 25])
            show_cards_on_table(screen, cardOnTable, takeTableCard)
            show_player1(screen, player1)
            op2 = pygame.image.load('pics/op2.png').convert()
            screen.blit(op2, [600, 280])
            pygame.display.flip()
            time.sleep(3)
            player3, cardOnTable = computer_turn(deck, player3, cardOnTable, table)
            player3.remove(cardOnTable)
            show_cards_on_table(screen, cardOnTable, takeTableCard)
            if numberOfPlayers == 3:
                turn = 0
            if numberOfPlayers == 4:
                turn = 3
            clean_click(player2)
            if len(player3) == 0:
                Tk().wm_withdraw()  # to hide the main window
                messagebox.showinfo('Game Over', 'Player 3 Wins !')
                win = True
                turn = 10
        cardOnTable.click = False
        # player 4
        while turn == 3:
            player_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    win = True
                    turn = 10
            screen.blit(background_image, [0, 0])
            screen.blit(back, [222, 190])
            update_table(screen, table)
            for i in range(len(player2)):
                screen.blit(back, [500 + i * 25, 25])
            back2 = pygame.transform.rotate(back, 90)
            for i in range(len(player3)):
                screen.blit(back2, [50, 150 + i * 25])
            for i in range(len(player4)):
                screen.blit(back2, [1200, 150 + i * 25])
            show_cards_on_table(screen, cardOnTable, takeTableCard)
            show_player1(screen, player1)
            op3 = pygame.image.load('pics/op3.png').convert()
            screen.blit(op3, [600, 280])
            pygame.display.flip()
            time.sleep(3)
            player4, cardOnTable = computer_turn(deck, player4, cardOnTable, table)
            player4.remove(cardOnTable)
            show_cards_on_table(screen, cardOnTable, takeTableCard)
            turn = 0
            clean_click(player4)
            if len(player4) == 0:
                Tk().wm_withdraw()  # to hide the main window
                messagebox.showinfo('Game Over', 'Player 4 Wins !')
                win = True
                turn = 10
        cardOnTable.click = False
        pygame.display.flip()
    pygame.quit()


main()
