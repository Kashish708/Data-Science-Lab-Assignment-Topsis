import sys
import pandas as pd
import numpy as np

def error(msg):
    print("Error:", msg)
    sys.exit(1)

def main():
    if len(sys.argv) != 5:
        error("Usage: python topsis.py <InputFile> <Weights> <Impacts> <OutputFile>")

    input_file = sys.argv[1]
    weights = sys.argv[2].split(',')
    impacts = sys.argv[3].split(',')
    output_file = sys.argv[4]

    try:

       data = pd.read_csv(
    input_file,
    delimiter=",",
    engine="python",
    encoding="latin1",
    skipinitialspace=True
)
    except Exception as e:
       error("Invalid CSV file: " + str(e))



    if data.shape[1] < 3:
        error("Input file must have at least 3 columns")

    try:
        matrix = data.iloc[:, 1:].astype(float)
    except:
        error("Columns from 2nd to last must be numeric")

    if len(weights) != matrix.shape[1]:
        error("Number of weights must match number of criteria")

    if len(impacts) != matrix.shape[1]:
        error("Number of impacts must match number of criteria")

    weights = np.array(weights, dtype=float)

    for i in impacts:
        if i not in ['+', '-']:
            error("Impacts must be '+' or '-'")

    # Step 1: Normalize
    norm = matrix / np.sqrt((matrix ** 2).sum())

    # Step 2: Weighted normalized
    weighted = norm * weights

    # Step 3: Ideal best and worst
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Step 4: Distance measures
    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    # Step 5: Topsis score
    score = dist_worst / (dist_best + dist_worst)

    data['Topsis Score'] = score
    data['Rank'] = score.rank(ascending=False)

    data.to_csv(output_file, index=False)
    print("Result saved in", output_file)

    print("DEBUG: Writing output to", output_file)
if __name__ == "__main__":
    main()