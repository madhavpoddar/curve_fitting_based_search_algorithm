import numpy as np
import random
import timeit
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit

# to generate a gaussian distribution
def get_truncated_normal(mean=4, sd=2, low=0, upp=10):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def generate_normal_dist_arr(N: int = 10000):
    normal_dist_not_sorted = get_truncated_normal().rvs(N)
    arr = np.sort(normal_dist_not_sorted)
    return arr


# Curve-fitting function
def func(x, a, b, c, d, e, f):
    # depending on the sorted data modify this equation to fit (value,index) better
    return a * x**5 + b * x**4 + c * x**3 + d * x**2 + e * x + f


class regression_based_search:
    def __init__(self, values):
        #
        # Assuming that the values are sorted
        #
        # This is a part of PRE-PROCESSING
        # and does not contribute to the time complexity of the search algorithm

        (self.a, self.b, self.c, self.d, self.e, self.f), _ = curve_fit(
            func, values, range(len(values))
        )
        # Note: we can replace this by any curve fitting / regression model
        # or try with different hyperparameters

        self.max_index = len(values) - 1

        self.element_wise_positive_deviation = np.zeros(len(values)).astype(int)
        self.element_wise_negative_deviation = np.zeros(len(values)).astype(int)
        for actual_index, ele in enumerate(values):
            predicted_index = self.calc_model_pred(ele)
            difference = actual_index - predicted_index
            if difference > 0:
                self.element_wise_positive_deviation[predicted_index] = max(
                    self.element_wise_positive_deviation[predicted_index], difference
                )
            elif difference < 0:
                self.element_wise_negative_deviation[predicted_index] = max(
                    self.element_wise_negative_deviation[predicted_index], -difference
                )

    def calc_model_pred(self, ele):
        model_pred = func(ele, self.a, self.b, self.c, self.d, self.e, self.f)
        model_pred = max(0, min(int(model_pred), self.max_index))
        return model_pred

    def search(self, values, ele):
        #
        # Step 1: Find float value of predicted index
        #
        model_pred = self.calc_model_pred(ele)

        # Step 2a: If found at predicted index, return index
        if values[model_pred] == ele:
            return model_pred

        # Step 2b: Else define the sub-array / array-slice than may contain the element
        if values[model_pred] < ele:
            subarray_start_index = min(model_pred + 1, self.max_index)
            subarray_end_index_plus_one = min(
                model_pred + self.element_wise_positive_deviation[model_pred] + 1,
                self.max_index + 1,
            )
        else:
            subarray_start_index = max(
                model_pred - self.element_wise_negative_deviation[model_pred], 0
            )
            subarray_end_index_plus_one = model_pred

        # Step 3: search only in this sub-array
        i = (
            np.searchsorted(
                values[subarray_start_index:subarray_end_index_plus_one],
                ele,
            )
            + subarray_start_index
        )
        return i if values[i] == ele else -1


# Generate non-uniform random array
N = int(1e5)
sorted_vals = generate_normal_dist_arr(N)

# Preprocessing: Computing Curve-fitting function and deviation arrays
search_model = regression_based_search(sorted_vals)

# Performing search for these elements
elements = np.random.choice(sorted_vals, int(N * 0.3))

# Time taken for Curve Fitting based Array search
print(
    timeit.timeit(
        "[search_model.search(sorted_vals, ele) for ele in elements]",
        globals=globals(),
        number=10,
    )
)

# Time taken for np.searchsorted (uses binary search)
print(
    timeit.timeit(
        "[np.searchsorted(sorted_vals, ele) for ele in elements]",
        globals=globals(),
        number=10,
    )
)
