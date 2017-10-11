from math import sqrt

def euclidean_distance(self, preferences):
    """
    Reports the Euclidean distance of two critics, A&B by
    performing a J-dimensional Euclidean calculation of
    each of their preference vectors for the intersection
    of movies the critics have rated.
    """
    # Get the intersection of the rated titles in the data.

    # If they have no rankings in common, return 0.
    if len(preferences) == 0:
        return 0

    # Sum the squares of the differences
    sum_of_squares = sum([pow(a-b, 2) for a, b in preferences.values()])

    # Return the inverse of the distance to give a higher score to
    # folks who are more similar (e.g. less distance) add 1 to prevent
    # division by zero errors and normalize ranks in [0,1]
    return 1 / (1 + sqrt(sum_of_squares))

def pearson_correlation(self, preferences):
    """
    Returns the Pearson Correlation of two user_s, A and B by
    performing the PPMC calculation on the scatter plot of (a, b)
    ratings on the shared set of critiqued titles.
    """

    # Store the length to save traversals of the len computation.
    # If they have no rankings in common, return 0.
    length = len(preferences)
    if length == 0:
        return 0

    # Loop through the preferences of each user_ once and compute the
    # various summations that are required for our final calculation.
    sumA = sumB = sumSquareA = sumSquareB = sumProducts = 0
    for a, b in preferences.values():
        sumA += a
        sumB += b
        sumSquareA += pow(a, 2)
        sumSquareB += pow(b, 2)
        sumProducts += a*b

    # Calculate Pearson Score
    numerator   = (sumProducts*length) - (sumA*sumB)
    denominator = sqrt(((sumSquareA*length) - pow(sumA, 2)) * ((sumSquareB*length) - pow(sumB, 2)))

    # Prevent division by zero.
    if denominator == 0:
        return 0

    return abs(numerator / denominator)