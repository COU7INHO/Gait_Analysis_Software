seq = "ATACCGGCGCGAATGACAGA"

i = 0
count = 0

while i < len(seq):
    if seq[i] == 'G' or seq[i] == 'C':
        count += 1
    i += 1

percent = count / len(seq) * 100
print(round(percent, 2), "%")

