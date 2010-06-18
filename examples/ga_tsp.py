#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

import array
import sys
import logging
import random
import yaml

sys.path.append("..")

import eap.base as base
import eap.creator as creator
import eap.toolbox as toolbox
import eap.halloffame as halloffame
import eap.algorithms as algorithms

logging.basicConfig(level=logging.DEBUG)
random.seed(1618)

# gr*.yml contains the distance map in list of list style in YAML/JSON format
# Optimal solutions are : gr17 = 2085, gr24 = 1272, gr120 = 6942
tsp = yaml.load(open("gr17.yml", "r"))
distance_map = tsp["DistanceMatrix"]
IND_SIZE = tsp["TourSize"]

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, fitness=creator.FitnessMin)

tools = toolbox.Toolbox()

# Attribute generator
tools.register("indices", random.sample, xrange(IND_SIZE), IND_SIZE)

# Structure initializers
tools.register("individual", creator.Individual, "i", content_init=tools.indices)
tools.register("population", list, content_init=tools.individual, size_init=300)

def evalTSP(individual):
    distance = distance_map[individual[-1]][individual[0]]
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        distance += distance_map[gene1][gene2]
    return distance,

tools.register("mate", toolbox.cxPartialyMatched)
tools.register("mutate", toolbox.mutShuffleIndexes, indpb=0.05)
tools.register("select", toolbox.selTournament, tournsize=3)
tools.register("evaluate", evalTSP)

if __name__ == "__main__":

    pop = tools.population()
    hof = halloffame.HallOfFame(1)
    
    algorithms.eaSimple(tools, pop, 0.7, 0.2, 40, hof)
    
    logging.info("Best individual is %s, %s", hof[0], hof[0].fitness.values)
