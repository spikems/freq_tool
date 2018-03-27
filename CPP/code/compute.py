import sys

#n(ad-bc)^2/(a+b)(c+d)(a+c)(b+d)
def compute(a, b, c, d):
    n = (a + b + c + d)
    fz = n * (a * d - b * c) * (a * d - b * c)
    fm = (a + b) * (c + d) * (a + c) * (b + d)
    return '%0.4f' % (float(fz)/float(fm))

d_pair = {}
d_one = {}
with open('part-00000', 'r') as fr:
    for line in fr:
        fs = line.strip().split('\t')
        key = fs[0]
        val = int(fs[1])
        if key.startswith('1_'):
            d_pair[key] = val
        else:
            d_one[key] = val

d_pair = []
for key in d_pair:
    v1 = key.split('_')[1]
    v2 = key.split('_')[2]
    v11 = d_pair[key]    #共同出现的次数

    v1_ = '2_%s' % v1
    v2_ = '2_%s' % v2
    v10 = d_one[v1_] - v11  #单独出现一个a的次数
    v01 = d_one[v2_] - v11  #单独出现b的次数
    v00 = 10000000 - v11 - v10 - v01  #没有出现a也没有出现b的次数
    val = compute(v11, v10, v01, v00)
    print '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (v1, v2, val, v11, v10, v01, v00)
   



