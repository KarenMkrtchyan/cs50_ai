import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidance = []
    lables = []
    with open(filename, newline='') as csv_data:
        data = csv.reader(csv_data, delimiter=',')
        fiels = next(data) # not actually used but needs to be looped over 
        for row in data:
            evidance.append(normalize(row[:17]))
            lables.append(1 if row[17] == "TRUE" else 0)

    return (evidance, lables)

def normalize(data):
    # month
    if data[10] == "Jan": 
        data[10] = 0
    elif data[10] == "Feb":
        data[10] = 1
    elif data[10] == "Mar":
        data[10] = 2
    elif data[10] == "Apr":
        data[10] = 3
    elif data[10] == "May":
        data[10] = 4
    elif data[10] == "June":
        data[10] = 5
    elif data[10] == "Jul":
        data[10] = 6
    elif data[10] == "Aug":
        data[10] = 7
    elif data[10] == "Sep":
        data[10] = 8    
    elif data[10] == "Oct":
        data[10] = 9
    elif data[10] == "Nov":
        data[10] = 10
    elif data[10] == "Dec":
        data[10] = 11

    # weekend
    if data[16] == "TRUE":
        data[16] = 1
    elif data[16] == "FALSE":
        data[16] = 0

    # ret cust
    if data[15] == "Returning_Visitor":
        data[15] = 1
    else:
        data[15] = 0

    for i in range(len(data)):
        try:
            data[i] = int(data[i])
        except: 
            data[i] = float(data[i])
    return data


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    print(evidence[0])
    print(labels[0])
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    sensitivity_counter = 0
    specificity = 0
    specificity_counter = 0

    for i in range(len(labels)):
        if labels[i]:
            sensitivity_counter += 1
            if predictions[i]:
                sensitivity += 1

        elif not labels[i]:
            specificity_counter += 1
            if not predictions[i]:
                specificity += 1


    return (sensitivity/sensitivity_counter, specificity/specificity_counter)

if __name__ == "__main__":
    main()
