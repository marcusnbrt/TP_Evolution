from codebase.algorithms import genetic_for_int
from codebase.algorithms.genetic_for_int import Genome
import cProfile
from pstats import SortKey

from collections import namedtuple

import pandas as pd
import numpy as np

from functools import partial
from codebase.utils.analyze import timer

year_start = 2021
year_end = 2045
number_years =year_end - year_start
max_number_exchanges = 1

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
    annual_exp_df = np.zeros(len(assets)*max_number_exchanges)
    add_cost_df = np.zeros(len(assets)*max_number_exchanges)# initiate fitness measurement additional cost to minimize
    x_h2_df = np.zeros(len(assets)*max_number_exchanges)
    asset_construction_years = [asset.y_construction for asset in assets]
    # loop over number of maximum exchanges

    for i_exchange in range(0,max_number_exchanges):
        exchange_genome = genome[i_exchange*len(assets):(i_exchange+1)*len(assets)]
        # loop over assets
        for i, asset in enumerate(assets):
            if exchange_genome[i] != 2021 and exchange_genome[i] > asset_construction_years[i]:
                remaining_life_asset = (asset_construction_years[i] + asset.depreciation_period) - exchange_genome[i]
                # Here we could kick out all genomes with remaining life < 0 or maybe 2 or 3 years more
                if remaining_life_asset > 0:
                    add_cost_df[i+(i_exchange*len(assets))] += ((asset.quantity * asset.c_1_euro) / asset.depreciation_period) * remaining_life_asset
                annual_exp_df[i+(i_exchange*len(assets))] += asset.quantity * asset.c_1_euro
                x_h2_df[i+(i_exchange*len(assets))] = asset.x_h2_1
                asset_construction_years[i] = exchange_genome[i]
    return add_cost_df.sum()#, annual_exp


def run_evolution():
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

    population, generations = genetic_for_int.run_evolution(start_year=year_start, end_year=year_end,
                                                            populate_func=partial(genetic_for_int.generate_population,
                                                                                  size=10, genome_length=len(
                                                                    assets) * max_number_exchanges, year_start=2022,
                                                                                  year_end=2045),
                                                            fitness_func=partial(fitness, assets=assets, limit=limit),
                                                            fitness_limit=100e15,
                                                            mutation_probability = 0.4,
                                                            generation_limit=100000
                                                            )
    print(population[0])
    print(generations)
    print(fitness(population[0], assets, limit))
    print(fitness(population[-1], assets, limit))

if __name__ == '__main__':

    # cProfile.run('run_evolution()',sort=SortKey.CUMULATIVE)
    run_evolution()


