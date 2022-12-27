from codebase.algorithms import genetic
from codebase.algorithms.genetic import Genome

from collections import namedtuple

import pandas as pd
import numpy as np

from functools import partial
from codebase.utils.analyze import timer

year_start = 2021
year_end = 2045
number_years =year_end - year_start

Asset = namedtuple('Asset', ['asset_id', 'asset_name', 'level', 'quantity',
                                'y_construction', 'av_useful_life', 'depreciation_period', # time
                                'x_h2_0', 'x_h2_1', 'x_h2_2', # h2 suitability in %vol
                                'c_1_euro', 'c_2_euro']) # cost per quantity in €

#  brauchen wir erstmal nicht oder?
# def generate_things(num: int) -> [Thing]:
#    return [Thing(f"thing{i}", i, i) for i in range(1, num+1)]

def fitness(genome: Genome, assets: [Asset], limit: int) -> ([float], [float]):
    if len(genome) != len(assets)*number_years: # todo [[assets],...,[assets]]
        raise ValueError("genome and product of number of assets and years must be of same length")

    # PSEUDOCODE todo check compliance with boundary condition (climate goals / h2 readyness)

    add_cost = [0]*number_years # initiate fitness measurement additional cost to minimize
    annual_exp = [0]*number_years # initiate empty list for annual expenditures
    x_h2_min = [] # iniate list for minimum h2 suitability
    x_h2 = [asset.x_h2_0 for asset in assets] # todo fill list with asset.x_h2_0
    remaining_life = [(asset.y_construction + asset.depreciation_period) - year_start for asset in assets]
    years = list(range(0, year_end-year_start))
    # loop over years
    for i_year, y in enumerate(years): #Todo enumerate entfernen
        yearly_genome = genome[i_year*len(assets):(i_year+1)*len(assets)]
        add_cost[y] = 0
        annual_exp[y] = 0 # set annual expenditures to zero at beginning of year

        # loop over assets
        for i, asset in enumerate(assets):
            if yearly_genome[i] == 1 and remaining_life[i] >0:
                add_cost[y] += ((asset.quantity * asset.c_1_euro) / asset.depreciation_period) * remaining_life[i]
            if (yearly_genome[i] == 0 and remaining_life[i] == 0) or yearly_genome[i] == 1:
                annual_exp[y] += asset.quantity * asset.c_1_euro
                x_h2[i] = asset.x_h2_1
                remaining_life[i] = asset.depreciation_period
            if sum(add_cost) > limit:
                # todo: check whether to fill annual_exp with NaN
                return np.inf
                # return [np.inf]*number_years, annual_exp # todo check other options for 'high number'! NaN? calculate worst case?
            remaining_life[i] -= 1
        x_h2_min.append(min(x_h2))
    return sum(add_cost)#, annual_exp

#
# def from_genome(genome: Genome, things: [Thing]) -> [Thing]:
#     result = []
#     for i, thing in enumerate(things):
#         if genome[i] == 1:
#             result += [thing]
#     return result
#
#
# def to_string(things: [Thing]):
#     return f"[{', '.join([t.name for t in things])}]"
#
#
# def value(things: [Thing]):
#     return sum([t.value for t in things])
#
#
# def weight(things: [Thing]):
#     return sum([p.weight for p in things])
#
#
# def print_stats(things: [Thing]):
#     print(f"Things: {to_string(things)}")
#     print(f"Value {value(things)}")
#     print(f"Weight: {weight(things)}")


if __name__ == '__main__':
    print('Hello Marcus')


    assets = []
    df = pd.read_excel('data/220117_RMG2050_MKG_VNB_MPo.xlsx', sheet_name='first_example')
    for i, row in df.iterrows():
        assets.append(Asset(row['asset_id'], row['asset_name'], row['level'], row['quantity'],
                                row['y_construction'], row['av_useful_life'], row['depreciation_period'],
                                row['x_h2_0'], row['x_h2_1'], row['x_h2_2'],
                                row['c_1_euro'], row['c_2_euro'])
                      )

    print(assets)
    limit = 100e15

    print("")
    print("GENETIC ALGORITHM")
    print("----------")

    with timer():
        population, generations = genetic.run_evolution(
            populate_func=partial(genetic.generate_population, size=20, genome_length=len(assets)*number_years),
            fitness_func=partial(fitness, assets=assets, limit=limit),
            fitness_limit=10e15,
            generation_limit=1000
        )
        print(population[0])

        print(generations)
        print(fitness(population[0],assets,limit))


    # gen = genetic.generate_genome(len(assets)*number_years)
    # print(gen)



