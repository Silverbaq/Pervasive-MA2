import csv

data = []

with open('model.model', 'r') as csvfile:
    print csvfile

    spamreader = csv.reader(csvfile)

    for row in spamreader:
        print row