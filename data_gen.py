import random
import numpy as np
# make a function, that takes in a classification function and datset and returns a mapping from the dataset to the classification
# points may not be hashable have a unique mapping, some points may be the same but map to different classifications
def classify(classifier, dataset):
    return [(point, classifier(point)) for point in dataset]

def getVerticalBoundaryClassifier(fn, classes=(True, False)):
    return lambda point: classes[0] if point[1] > fn(point[0]) else classes[1]

def uniformRandomPointSampler(x_range, y_range, n):
    return [(random.uniform(*x_range), random.uniform(*y_range)) for _ in range(n)]

def uniformSpacedGridPointSampler(x_range, y_range, n):
    # n is the number of points ~ total
    n = int(np.sqrt(n))
    x_points = [x for x in np.linspace(*x_range, n)]
    y_points = [y for y in np.linspace(*y_range, n)]
    return [(x, y) for x in x_points for y in y_points]

def jiggleSamples(samples, jiggle_dist=0.1):
    return [(x + random.uniform(-jiggle_dist, jiggle_dist), y + random.uniform(-jiggle_dist, jiggle_dist)) for x, y in samples]


def classifyUniformSpacedGridSample(classifier, x_range, y_range, n):
    grid_sample = uniformSpacedGridPointSampler(x_range, y_range, n)
    return classify(classifier, grid_sample)

def classifyUniformRandomSample(classifier, x_range, y_range, n):
    random_sample = uniformRandomPointSampler(x_range, y_range, n)
    return classify(classifier, random_sample)

def classifyJiggledUniformRandomSample(classifier, x_range, y_range, n, jiggle_dist=0.1):
    random_sample = uniformRandomPointSampler(x_range, y_range, n)
    jiggle_sample = jiggleSamples(random_sample, jiggle_dist)
    return classify(classifier, jiggle_sample)

def splitByClass(classified_sample):
    classes = {}
    for point, classification in classified_sample:
        if classification not in classes:
            classes[classification] = []
        classes[classification].append(point)
    return classes

def randomSampleSplit(fn, x_range, y_range, n, classifier=None):
    if classifier is None:
        classifier = getVerticalBoundaryClassifier(fn)
    classified_sample = classifyUniformRandomSample(classifier, x_range, y_range, n)
    return splitByClass(classified_sample)

def gridSampleSplit(fn, x_range, y_range, n, classifier=None):
    if classifier is None:
        classifier = getVerticalBoundaryClassifier(fn)
    classified_sample = classifyUniformSpacedGridSample(classifier, x_range, y_range, n)
    return splitByClass(classified_sample)

def jiggleSampleSplit(fn, x_range, y_range, n, classifier=None, jiggle_dist=None):
    if jiggle_dist is None:
        jiggle_dist = (x_range[1] - x_range[0]) / n * 0.001
    if classifier is None:
        classifier = getVerticalBoundaryClassifier(fn)
    classified_sample = classifyJiggledUniformRandomSample(classifier, x_range, y_range, n, jiggle_dist)
    return splitByClass(classified_sample)


#TODO: Refactor this, seems like a lot of repeated code