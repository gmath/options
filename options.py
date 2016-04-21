#! /usr/bin/python

import argparse
import re
import numpy as np
import matplotlib.pyplot as plt
import textwrap
import json

class Call:
    def __init__(self, position_type, quantity, strike_price, cost):
        self.position_type = position_type
        self.quantity      = quantity
        self.strike_price  = strike_price
        self.cost          = cost
    def get_strike_price(self):
        return self.strike_price
    def get_cost(self):
        return self.cost
    def get_payout(self, stock_price):
        if self.position_type == 'l':
            return self.quantity * max(-self.cost,  stock_price - self.strike_price - self.cost)
        elif self.position_type == 's':
            return self.quantity * min(self.cost, self.strike_price + self.cost - stock_price)
    def __repr__(self):
        position_mapper = {
            'l' : 'long',
            's' : 'short'
        }
        position=position_mapper[self.position_type]
        return "{quantity} {position} Call {strike_price} at {cost}".format(quantity=self.quantity,
                                                                            position=position,
                                                                            strike_price=self.strike_price,
                                                                            cost=self.cost)

class Put:
    def __init__(self, position_type, quantity, strike_price, cost):
        self.position_type = position_type
        self.quantity      = quantity
        self.strike_price  = strike_price
        self.cost          = cost
    def get_strike_price(self):
        return self.strike_price
    def get_cost(self):
        return self.cost
    def get_payout(self, stock_price):
        if self.position_type == 'l':
            return self.quantity * max(-self.cost, self.strike_price - stock_price - self.cost)
        elif self.position_type == 's':
            return self.quantity * min(self.cost, stock_price - self.strike_price + self.cost)
    def __repr__(self):
        position_mapper = {
            'l' : 'long',
            's' : 'short'
        }
        position = position_mapper[self.position_type]
        return "{quantity} {position} Put {strike_price} at {cost}".format(quantity=self.quantity,
                                                                            position=position,
                                                                            strike_price=self.strike_price,
                                                                            cost=self.cost)

def create_expiration_graph(options):

    strike_prices = set(option.get_strike_price() for option in options)
    costs         = set(option.get_cost() for option in options)

    min_cost = min(costs)
    max_cost = max(costs)

    min_strike_price = min(strike_prices)
    max_strike_price = max(strike_prices)

    window = 0.5
    lower_bound = (1 - window) * min(min_strike_price, min_strike_price - min_cost)
    upper_bound = (1 + window) * max(max_strike_price, max_strike_price + max_cost)
    spread = upper_bound - lower_bound

    """ look at 5 cent intervals """
    xstock_prices  = np.linspace(lower_bound, upper_bound, 20 * spread)
    option_payouts = [sum(option.get_payout(xstock_price) for option in options) for xstock_price in xstock_prices]
    
    for option in options:
        payouts = [option.get_payout(xstock_price) for xstock_price in xstock_prices]
        plt.plot(xstock_prices, payouts, '--', label=option)

    plt.title("Options Expiry")
    plt.xlabel("stock price")
    plt.ylabel("value of position")
    plt.plot(xstock_prices, option_payouts, '>', label='combined position')
    plt.legend(loc='lower right')
    plt.axhline(y=0, color='k')

    for strike_price in strike_prices:
        plt.axvline(x=strike_price, color='k')
    plt.show()

if __name__=="__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description=textwrap.dedent('''                                                                                                          
                                     Use this script to create expiry graphs for finance options.\n

                                     Suppose I want to know how the following option chains expire:
                                     
                                     (example 1)
                                     long 1 100 call at 2.70 --> l1c100@2.70
                                     python options.py --chain l1c100@2.70

                                     (example 2)
                                     short 1 95 put at  1.55 --> s1p95@1.55
                                     short 1 100 put at 3.70 --> s1p100@3.70
                                     short 1 105 put at 7.10 --> s1p105@7.10
                                     python options.py --chain s1p95@1.55 s1p100@3.70 s1p105@7.10

                                     (example 3)
                                     short 1 100 call at 2.70 --> s1c100@2.70
                                     short 1 100 put at 3.70 --> s1p100@3.70
                                     python options.py --chain s1c100@2.70 s1p100@3.70

                                     (example 4) these can be made very complex
                                     short 1 90 call at 9.35 --> s1c90@9.35
                                     long two 100 calls at 2.70 --> l2c100@2.70
                                     short four 95 puts at 1.55 --> s4p95@1.55
                                     long two 100 puts at 3.70 --> l2p100@3.70
                                     python options.py --chain s1c90@9.35 l2c100@2.70 s4p95@1.55 l2p100@3.70
                                      '''))

    parser.add_argument('--chain', metavar='N', type=str, nargs='+', help='list of option configs')

    args  = parser.parse_args()
    chain = args.chain
    
    options = []
    input_success = True
    for option in chain:
        match = re.match(r"([a-z]+)([0-9]+)([a-z]+)([0-9]+)@([0-9]+\.[0-9]+)", option, re.I)
        if match:
            position_type, quantity, option_type, strike_price, cost = match.groups()
            if option_type == 'c':
                call_option = Call(position_type, float(quantity), float(strike_price), float(cost))
                options.append(call_option)
            elif option_type == 'p':
                put_option = Put(position_type, float(quantity), float(strike_price), float(cost))
                options.append(put_option)
            else:
                print "failed to parse input"
                input_success = False
                break
        else:
            print "failed to parse input"
            input_success = False
            break

    if input_success is True:
        create_expiration_graph(options)
    
