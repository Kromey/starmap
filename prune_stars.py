import csv


IN = 'stars.csv'
OUT = 'stars_pruned.csv'
RANGE = 16.999


count = 0
hab = 0


with open(IN, 'r', newline='') as infile:
    reader = csv.DictReader(infile)

    with open(OUT, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            dist = float(row['Distance'].strip())
            if dist > RANGE:
                continue

            c = (float(row['Xg']), float(row['Yg']), float(row['Zg']))
            print(dist, c, row['Spectral Class'], row['Display Name'])

            count += 1
            if row['Hab?'].strip():
                hab += 1

            writer.writerow(row)


print('Stars:', count, 'Habitable:', hab)

