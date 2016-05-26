import csv

data = []

calc_vectors2 = []

with open('model.csv', 'r') as csvfile:
    print csvfile

    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')


    for row in spamreader:
        calc_vectors = []
        vec_row = []
        count = 0

        row_split = row[0].split(',')
        gesture = row_split[-1]
        row_split = row_split[:180]

        row_split2 = map(int, row_split)

        vec = [0,0,0,0,0,0]

        while count < 174: # Last set is only used once
            ax1 = row_split2[count]
            ay1 = row_split2[count + 1]
            az1 = row_split2[count + 2]
            gx1 = row_split2[count + 3]
            gy1 = row_split2[count + 4]
            gz1 = row_split2[count + 5]

            ax2 = row_split2[count + 6]
            ay2 = row_split2[count + 7]
            az2 = row_split2[count + 8]
            gx2 = row_split2[count + 9]
            gy2 = row_split2[count + 10]
            gz2 = row_split2[count + 11]

            a = [ax2 - ax1, ay2 - ay1, az2 - az1, gx2 - gx1, gy2 - gy1, gz2 - gz1]

            #add to line total vector
            vec[0]+= a[0]
            vec[1]+= a[1]
            vec[2]+= a[2]
            vec[3]+= a[3]
            vec[4]+= a[4]
            vec[5]+= a[5]

            count = count + 6  # Increase indexing
            vec_row.append(a)


        calc_vectors.append(vec) # Adding calc vector to list
        calc_vectors.append(gesture) # Adding calc vector to list
        calc_vectors2.append(calc_vectors)

        vec_row.append(gesture)  # Adding gesture
        data.append(vec_row)  # adding row of vortex to data

print len(data)

# write model to file
b = open("model.model", 'a')
a = csv.writer(b,delimiter=";")
for d in data:
    a.writerow(d)
b.close()


# write calc vectors file
b2 = open("model.vector", 'a')
a2 = csv.writer(b2,delimiter=";")
for d2 in calc_vectors2:
    a2.writerow(d2)
b2.close()