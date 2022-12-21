from codebase.algorithms import genetic_for_int
from codebase.algorithms.genetic_for_int import Genome

from collections import namedtuple

import pandas as pd
import numpy as np

from functools import partial
from codebase.utils.analyze import timer

year_start = 2021
year_end = 2045
number_years =year_end - year_start
max_number_exchanges = 3

Asset = namedtuple('Asset', ['asset_id', 'asset_name', 'level', 'quantity',
                                'y_construction', 'av_useful_life', 'depreciation_period', # time
                                'x_h2_0', 'x_h2_1', 'x_h2_2', # h2 suitability in %vol
                                'c_1_euro', 'c_2_euro']) # cost per quantity in €

#  brauchen wir erstmal nicht oder?
# def generate_things(num: int) -> [Thing]:
#    return [Thing(f"thing{i}", i, i) for i in range(1, num+1)]

def fitness(genome: Genome, assets: [Asset], limit: int) -> float:
    if len(genome) != len(assets)*max_number_exchanges: # todo [[assets],...,[assets]]
        raise ValueError("genome and product of number of assets and years must be of same length")

    # PSEUDOCODE todo check compliance with boundary condition (climate goals / h2 readyness)
    annual_exp_df = pd.DataFrame(0, index= np.arange(len(assets)),columns=[i for i in range(year_start,year_end+1)])
    add_cost_df = pd.DataFrame(0, index= np.arange(len(assets)),columns=[i for i in range(year_start,year_end+1)])# initiate fitness measurement additional cost to minimize
    x_h2_df = pd.DataFrame(0, index= np.arange(len(assets)),columns=[i for i in range(year_start,year_end+1)])
    asset_construction_years = [asset.y_construction for asset in assets]
    # loop over number of maximum exchanges

    for i_exchange in range(0,max_number_exchanges):
        exchange_genome = genome[i_exchange*len(assets):(i_exchange+1)*len(assets)]
        # loop over assets
        for i, asset in enumerate(assets):
            if exchange_genome[i] != 0 and exchange_genome[i] > asset_construction_years[i]:
                remaining_life_asset = (asset_construction_years[i] + asset.depreciation_period) - exchange_genome[i]
                # Here we could kick out all genomes with remaining life < 0 or maybe 2 or 3 years more
                if remaining_life_asset > 0:
                    add_cost_df.at[i, exchange_genome[i]] += ((asset.quantity * asset.c_1_euro) / asset.depreciation_period) * remaining_life_asset
                annual_exp_df.at[i, exchange_genome[i]] += asset.quantity * asset.c_1_euro
                x_h2_df.at[i, exchange_genome[i]] = asset.x_h2_1
                asset_construction_years[i] = exchange_genome [i]
    return add_cost_df.sum().sum()#, annual_exp

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
        population, generations = genetic_for_int.run_evolution(start_year= year_start, end_year=year_end,
            populate_func=partial(genetic_for_int.generate_population, size=10, genome_length=len(assets)*max_number_exchanges, year_start =2022, year_end= 2045),
            fitness_func=partial(fitness, assets=assets, limit=limit),
            fitness_limit=100e15,
            generation_limit=100
        )
        print(population[-1])
        print(generations)
        print(fitness(population[-1],assets,limit))


    # gen = genetic.generate_genome(len(assets)*number_years)
    # print(gen)



