import os



with open('/home/rzli/ff/tmp.csv','w') as w:
    for i in os.listdir('/home/rzli/ff/ann/'):
        f = open('/home/rzli/ff/ann/' + i,'r')
        print(i)
        li = i.split('.')[0].split('_')
        if len(li) == 3:
            lii = li[0] + '_' + li[1] + '.' + li[2]
        else:
            lii = li[0]
        count = 1
        for j in f:
            print(j)
            if count != 1:
                j = j.strip().split('\t')
                j = ['Unknown' if m =='' else m for m in j]
                line = str(count-1) + '\t' + '\t'.join(j) + '\t' + lii + '\n'
                print(line)
                w.write(line)
                count += 1
            else:
                count += 1
w.close()

# counts = 1
# with open('/home/rzli/ff/' + file + '-1.csv') as r:
#     with open('/home/rzli/ff/' + file + '.csv','w') as w:
#         for m in r:
#             lines = str(counts) + ',' + m
#             w.write(lines)
#             counts += 1
#     w.close()
# r.close()

# os.remove('/home/rzli/ff/' + file + '-1.csv')
#


counts = 1
with open('/home/rzli/ff/tmp.csv') as r:
    with open('/home/rzli/ff/annotate.csv','w') as w:
        for m in r:
            lines = str(counts) + '\t' + m
            w.write(lines)
            counts += 1
            print(lines)
    w.close()
r.close()

os.system('rm /home/rzli/ff/tmp.csv')