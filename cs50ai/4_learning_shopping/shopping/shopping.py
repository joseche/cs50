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
    X_train, X_test, y_train, y_test = train_test_split(evidence, labels, test_size=TEST_SIZE)

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
    months = dict(Jan=0, Feb=1, Mar=2, Apr=3, May=4, Jun=5, June=5, Jul=6, Aug=7, Sep=8, Oct=9, Nov=10, Dec=11)

    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        evidence = []
        labels = []

        for row in reader:
            evidence.append(
                [
                    int(row[0]),  # administrative
                    float(row[1]),  # adm duration
                    int(row[2]),  # info
                    float(row[3]),  # info dur
                    int(row[4]),  # prod related
                    float(row[5]),  # prod related dur
                    float(row[6]),  # bounce rate
                    float(row[7]),  # exist rate
                    float(row[8]),  # page values
                    float(row[9]),  # special
                    months[row[10]],  # month
                    int(row[11]),  # OS
                    int(row[12]),  # browser
                    int(row[13]),  # region
                    int(row[14]),  # traff type
                    0 if row[15] == "New_Visitor" else 1,  # visitor type
                    0 if row[16] == "FALSE" else 1,  # weekend
                ]
            )
            labels.append(1 if row[17] == "TRUE" else 0)
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)


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
    true_positive_rate = 0  # actual positive accurately identified
    true_negative_rate = 0  # actual negative accurately identified
    positive_count = 0
    negative_count = 0
    for prediction, label in zip(predictions, labels):
        if prediction == label:
            if label == 1:
                true_positive_rate += 1
            else:
                true_negative_rate += 1
        if label == 1:
            positive_count += 1
        else:
            negative_count += 1
    return (true_positive_rate / positive_count, true_negative_rate / negative_count)


if __name__ == "__main__":
    main()
