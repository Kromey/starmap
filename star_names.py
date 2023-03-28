import csv
import re

MAX_RANGE = 16.999

header = []

by_hip = {}
by_hd = {}
by_hr = {}
by_gliese = {}

all_names = []
bf_names = []

iau_count = 0
with open('data/iau_star_names.txt', 'r') as fh:
    for line in fh.readlines():
        line = line.strip()
        if len(line) == 0:
            continue

        if line.startswith(('#', '$')):
            header = line[1:].split()
            continue

        data = [
            line[0:18].strip(),
            line[18:36].strip(),
            line[36:49].strip()
        ] + line[49:].split()
        row = dict(zip(header, data))
        # print(row)
        # if "Proxima" in line:
        #     print(line)
        #     print(data)
        #     print(row)
        #     exit()
        
        by_hip[row['HIP']] = row['Name/Diacritics']
        by_hd[row['HD']] = row['Name/Diacritics']

        if row['Designation'].startswith('HR '):
            by_hr[row['Designation'][3:]] = row['Name/Diacritics']
        elif row['Designation'].startswith('GJ '):
            by_gliese[row['Designation'][3:]] = row['Name/Diacritics']

        iau_count += 1

with open('data/HabHyg.csv', 'r', newline='') as fh:
    reader = csv.DictReader(fh)

    for row in reader:
        dist = float(row['Distance'].strip())
        if dist > MAX_RANGE:
            break

        hip = row['Hip']
        hd = row['HD']
        hr = row['HR']
        gliese = row['Gliese'][3:]
        try:
            name = by_hip[hip]
        except KeyError:
            try:
                name = by_hd[hd]
            except KeyError:
                try:
                    name = by_hr[hr]
                except KeyError:
                    try:
                        name = by_gliese[gliese]
                    except KeyError:
                        name = row['Proper Name']

                        if not name and row['BayerFlamsteed']:
                            name = re.sub(r'^\d+\s+', '', row['BayerFlamsteed'])
                            name = re.sub(r'\s+\d\s+', ' ', name)

                            bf_names.append(name)

        if name and name not in all_names:
            bf = " *" if name in bf_names else ""
            print(f"Found name! {name}{bf}")

            all_names.append(name)

print(f"IAU list contains {iau_count} names")
print("Found {} names, of which {} are from BayerFlamsteed".format(len(all_names), len(bf_names)))

