import sys

def compute(a, b, c, d):
    n = (a + b + c + d)
    fz = n * (a * d - b * c) * (a * d - b * c)
    fm = (a + b) * (c + d) * (a + c) * (b + d)
    return '%0.4f' % (float(fz)/float(fm))

d_pair = {}
d_one = {}
outfile =open(sys.argv[3],'wb')
with open(sys.argv[1], 'r') as fr:
    for line in fr:
        fs = line.strip().split('\t')
        key = fs[0]
        val = int(fs[1])
        if key.startswith('1_'):
            d_pair[key] = val
        else:
            d_one[key] = val

total = int(sys.argv[2])
for key in d_pair:
    v1 = key.split('_')[1]
    v2 = key.split('_')[2]
    v11 = d_pair[key]

    v1_ = '2_%s' % v1
    v2_ = '2_%s' % v2
    v10 = d_one[v1_] - v11
    v01 = d_one[v2_] - v11
    v00 = total - v11 - v10 - v01
    if v11>5 and v10>5 and v01>5 and v00>5:
        val = compute(v11, v10, v01, v00)
        line = '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (v1, v2, val, v11, v10, v01, v00)
        outfile.write(line)

outfile.close()


