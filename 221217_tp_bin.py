from algorithms.genetic import *
from collections import namedtuple
import numpy as np

year_start = 2021
year_end = 2045
number_years = year_start-year_end

Asset = namedtuple('Asset', ['asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period' # time
                                'x_h2_0', 'x_h2_1', 'x_h2_2', # h2 suitability in %vol
                                'c_1_euro', 'c_2_euro']) # cost per quantity in €

first_example = [ #todo create
    Asset('asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period'
                                'x_h2_0', 'x_h2_1', 'x_h2_2',
                                'c_1_euro', 'c_2_euro'),
    Asset('asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period'
                                'x_h2_0', 'x_h2_1', 'x_h2_2',
                                'c_1_euro', 'c_2_euro'),
    Asset('asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period'
                                'x_h2_0', 'x_h2_1', 'x_h2_2',
                                'c_1_euro', 'c_2_euro'),
    Asset('asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period'
                                'x_h2_0', 'x_h2_1', 'x_h2_2',
                                'c_1_euro', 'c_2_euro'),
    Asset('asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period'
                                'x_h2_0', 'x_h2_1', 'x_h2_2',
                                'c_1_euro', 'c_2_euro'),
    Asset('asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period'
                                'x_h2_0', 'x_h2_1', 'x_h2_2',
                                'c_1_euro', 'c_2_euro'),
    Asset('asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period'
                                'x_h2_0', 'x_h2_1', 'x_h2_2',
                                'c_1_euro', 'c_2_euro'),
    Asset('asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period'
                                'x_h2_0', 'x_h2_1', 'x_h2_2',
                                'c_1_euro', 'c_2_euro'),
    Asset('asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period'
                                'x_h2_0', 'x_h2_1', 'x_h2_2',
                                'c_1_euro', 'c_2_euro'),
    Asset('asset_id', 'asset_name', 'level', 'quantity'
                                'y_construction', 'av_useful_life', 'depreciation_period'
                                'x_h2_0', 'x_h2_1', 'x_h2_2',
                                'c_1_euro', 'c_2_euro'),
]

#  brauchen wir erstmal nicht oder?
# def generate_things(num: int) -> [Thing]:
#    return [Thing(f"thing{i}", i, i) for i in range(1, num+1)]

def fitness(genome: Genome, assets: [Asset], limit: int) -> ([float], [float]):
    if len(genome) != len(assets)*number_years: # todo [[assets],...,[assets]]
        raise ValueError("genome and product of number of assets and years must be of same length")

    # PSEUDOCODE todo check compliance with boundary condition (climate goals / h2 readyness)

    add_cost = [] # initiate fitness measurement additional cost to minimize
    annual_exp = [] # initiate empty list for annual expenditures
    x_h2_min = [] # iniate list for minimum h2 suitability
    x_h2 = [asset.x_h2_0 for asset in assets] # todo fill list with asset.x_h2_0
    
    # loop over years
    for y in list(range(0, year_end-year_start)):
        # PSEUDOCODE todo: subset / trim genome to 'yearly_genom'


        add_cost[y] = 0
        annual_exp[y] = 0 # set annual expenditures to zero at beginning of year

        # loop over assets
        for i, asset in enumerate(assets):

            # calculate remaining life
            remaining_life = y - (asset.y_construction + asset.depreciation_period)
            if genome[i] == 1:
                annual_exp[y] += asset.quantity * asset.c_1_euro
                x_h2[i] = asset.x_h2_1
            if genome[i] == 1 and remaining_life >0:
                add_cost[y] += ((asset.quantity * asset.c_1_euro) / asset.depreciation_period) * remaining_life
            if sum(add_cost) > limit:
                # todo: check whether to fill annual_exp with NaN
                return [np.inf]*number_years, annual_exp # todo check other options for 'high number'! NaN? calculate worst case?
        x_h2_min[y] = min(x_h2)
    return add_cost, annual_exp


def from_genome(genome: Genome, things: [Thing]) -> [Thing]:
    result = []
    for i, thing in enumerate(things):
        if genome[i] == 1:
            result += [thing]
    return result


def to_string(things: [Thing]):
    return f"[{', '.join([t.name for t in things])}]"


def value(things: [Thing]):
    return sum([t.value for t in things])


def weight(things: [Thing]):
    return sum([p.weight for p in things])


def print_stats(things: [Thing]):
    print(f"Things: {to_string(things)}")
    print(f"Value {value(things)}")
    print(f"Weight: {weight(things)}")


if __name__ == '__main__':
    print('Hello Marcus')

    def generate_genome(length: int) -> Genome:
        return choices([0, 1], k=length)


    gen = .generate_genome(len(assets)*number_years)



