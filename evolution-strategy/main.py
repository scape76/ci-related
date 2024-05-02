from numpy import asarray
from es_comma import es_comma
from es_plus import es_plus
from shared import cases
import time
from shared import goldsteinPrice, mcCormick, holder

# mu: The number of parents selected each iteration.
# lambda: Size of the population.
# lambda / mu: Number of children generated from each selected parent.

# A bracket notation is used to describe the algorithm configuration,
# e.g. (mu, lambda)-ES. For example, if mu=5 and lambda=20, then it would be summarized as (5, 20)-ES. A comma
# (,) separating the mu and lambda parameters indicates that the children replace
# the parents directly each iteration of the algorithm.

# (mu, lambda)-ES: A version of evolution strategies where children replace parents.
# A plus (+) separation of the mu and lambda parameters indicates that the children
# and the parents together will define the population for the next iteration.
# (mu + lambda)-ES: A version of evolution strategies where children and parents are added to the population.

lam = 10
mu = 4
stepSize = 0.15
nIter = 1000


def format_num(x):
    return f"{x:.5f}"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for case in cases:
        print(case["separator"])
        st = time.time()
        best, score, average, speed = es_comma(lam, mu, asarray(case["bounds"]), case["function"], nIter,
                                               stepSize,
                                               case["minimum"])
        et = time.time()
        print(
            f"f[{format_num(best[0])}; {format_num(best[1])}] = {format_num(score)} ||| ВІДХИЛЕННЯ: {format_num(average)}",
            " speed ", et - st)
