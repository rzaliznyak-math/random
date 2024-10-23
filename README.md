# Understanding Randomess & Chance with Numpy
Russ Zaliznyak
2024-10-18

- [Introduction](#introduction)
- [Simulating Data](#simulating-data)

## Introduction

Imagine your website converts 10% of its visitors to paying customers.
Over the course of 1,000 visitors, how many converts should we expect? A
quick back of the envelope calculation shows we should expect 100
conversions: $$
1000 \, \text{visitors} * \frac{10 \, \text{conversions}}{100 \, \text{visitors}} = 100 \, \text{conversions}
$$

*But how much could that number vary each time we run this experiment?*

# Simulating Data

``` python
from numpy.random import binomial
from numpy import mean

conversion_rate = 0.10
number_of_visitors = int(1e3)


number_simulated_experiments = int(1e6)
control_simulated_results = binomial(
    number_of_visitors, conversion_rate, size=number_simulated_experiments
)


print(mean(control_simulated_results))
```

    99.99668
