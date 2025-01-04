################################################################################
#   CSE Project 5 - Yu-Gi-Oh TCG Program
#   Algorithm Overview:
#       1 - Program starts
#       2 - User is asked for a file name
#       3 - The program opens the file and asks the user for an option
#       4 - The options perform different tasks depending on what is selected
#       5 - The user can choose check all the cards, which are printed out
#       6 - The user can search for specific cards depending on given factors
#       7 - The user can view cards from a given set of IDs
#       8 - If incorrect option is chosen, the user is prompted again.
#       9 - The program continues to run until told to stop
#       10- Program ends if user chooses the option
################################################################################

import csv
from itertools import count
from operator import itemgetter

MENU = "\nYu-Gi-Oh! Card Data Analysis" \
           "\n1) Check All Cards" \
           "\n2) Search Cards" \
           "\n3) View Decklist" \
           "\n4) Exit" \
           "\nEnter option: "

CATEGORIES = ["id", "name", "type", "desc", "race", "archetype", "card price"]

def open_file(prompt_str):
    '''The function repeatedly asks the user for a file name.
        If the file exists, it is opened and returned.
        If it doesn't, the user is asked again until a valid file is entered.'''
    try:
        file = open(prompt_str, 'r', encoding='utf-8')
        return file
    except IOError: # Incorrect files are rejected and the function reruns.
        print("\nFile not Found. Please try again!")
        prompt_str = input("\nEnter cards file name: ")
        return open_file(prompt_str)

def read_card_data(fp):
    ''' The data is read and converted into a csv list with tuples.
        The first row is skipped, the tuples are added to a list.
        The list is then sorted in order of price and then name.
        The list is returned.'''
    card_list = []
    csv_reader = csv.reader(fp)
    next(csv_reader)
    for line in csv_reader:
        card_tuple = (line[0], line[1][:45], line[2], line[3], line[4], line[5], float(line[6]))
        card_list.append(card_tuple)
        card_list.sort(key= itemgetter(6,1)) #sorts the list
    return card_list


def read_decklist(fp, card_data):
    ''' Creates a new list of cards from the card data by their ID.
        A YDK file with IDs is used to find the cards.
        The list is then sorted in order of price and then name.
        The list is returned.'''
    decklist = []
    for line in fp:
        line = line.strip()
        for card in card_data:
            if line == card[0]:
                decklist.append(card)
    decklist.sort(key= itemgetter(6,1))
    return decklist


def search_cards(card_data, query, category_index):
    ''' This function goes through the card data and finds cards that
        match the given query and category. The cards are added to a
        list and then sorted in order of price and then name.
        The list is returned.'''
    search_list = []
    for card in card_data:
        if query in card[category_index]:
            search_list.append(card)
    search_list.sort(key=itemgetter(6, 1))
    return search_list


def compute_stats(card_data):
    ''' The function finds the min, max and median values of the
    cards and adds the cards with those values into separate lists.
    The lists and the values are then returned.'''

    # this block finds the max value and cards and makes the list.
    max_price = max(card_data, key = itemgetter(6))[6]
    max_list = []
    for card in card_data:
        if card[6] == max_price:
            max_list.append(card)
    max_list.sort(key=itemgetter(1))

    # this block finds the min value and cards and makes the list.
    min_list = []
    min_price = min(card_data, key = itemgetter(6))[6]
    for card in card_data:
        if card[6] == min_price:
            min_list.append(card)
    max_list.sort(key=itemgetter(1))

    # this block finds the max value and cards and makes the list.
    median = card_data[len(card_data)//2][6]
    med_list = []
    for card in card_data:
        if card[6] == median:
            med_list.append(card)

    return min_list, min_price, max_list, max_price, med_list, median

def display_data(card_data):
    ''' This function takes the cards from a given card data set
        and prints them out with the specified formatting.'''
    print(f"{'Name':<50}{'Type':<30}{'Race':<20}{'Archetype':<40}{'TCGPlayer':<12}")
    total_price = 0
    for card in card_data:
        print(f"{card[1]:<50}{card[2]:<30}{card[4]:<20}{card[5]:<40}{card[6]:>12,.2f}")
        total_price += card[6]
    print(f"\n{'Totals':50}{'':30}{'':20}{'':40}{total_price:>12,.2f}")
    return


def display_stats(min_cards, min_price, max_cards, max_price, med_cards, med_price):
    ''' This function takes the cards from a given card data set and
        prints out the cards with the minimum, maximum and median values.'''
    print(f"\nThe price of the least expensive card(s) is {min_price:,.2f}")
    for card in min_cards:
        print(f"\t{card[1]}")
    print(f"\nThe price of the most expensive card(s) is {max_price:,.2f}")
    for card in max_cards:
        print(f"\t{card[1]}")
    print(f"\nThe price of the median card(s) is {med_price:,.2f}")
    for card in med_cards:
        print(f"\t{card[1]}")


def main():
    stop_bool = False
    prompt_str = input("\nEnter cards file name: ")
    fp = open_file(prompt_str)
    card_list = read_card_data(fp)
    user_input_options = ['1','2','3','4']

    while stop_bool == False:
        user_input = input(MENU)
        while user_input not in user_input_options:
            print("\nInvalid option. Please try again!")
            user_input = input(MENU)
        user_input = int(user_input)
        if user_input ==1:
            print(f"\nThere are {len(card_list)} cards in the dataset.")
            card_list.sort(key = itemgetter(6))
            display_data(card_list[:50])
            min_list, min_price, max_list, max_price, med_list, median = compute_stats(card_list)
            display_stats(min_list, min_price, max_list, max_price, med_list, median)
        elif user_input == 2:
            query = input("\nEnter query: ")
            category = input("\nEnter category to search: ").lower()
            cat_bool = True
            while cat_bool == True:
                if category in CATEGORIES:
                    cat_bool = False
                else:
                    print("\nIncorrect category was selected!")
                    category = input("\nEnter category to search: ").lower()
            searched_cards = search_cards(card_list, query, CATEGORIES.index(category))
            print("\nSearch results")
            if len(searched_cards) != 0:
                print(f"\nThere are {len(searched_cards)} cards with '{query}' in the '{category}' category.")
                min_list, min_price, max_list, max_price, med_list, median = compute_stats(searched_cards)
                display_data(searched_cards)
                display_stats(min_list, min_price, max_list, max_price, med_list, median)
            else:
                print(f"\nThere are no cards with '{query}' in the '{category}' category.")
        elif user_input == 3:
            deck_file = input("\nEnter decklist filename: ")
            print("\nSearch results")
            deckfile_open = open(deck_file, "r", encoding = 'utf-8')
            decklist = read_decklist(deckfile_open, card_list)
            deckfile_open.close()
            display_data(decklist)
            min_list, min_price, max_list, max_price, med_list, median = compute_stats(decklist)
            display_stats(min_list, min_price, max_list, max_price, med_list, median)
        elif user_input == 4:
            print("\nThanks for your support in Yu-Gi-Oh! TCG")
            stop_bool = True
    pass


if __name__ == "__main__":
    main()