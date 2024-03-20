import os

path_1 = '/home/rzli/ff/lysin/'
path_2 = '/home/rzli/ff/peptide/'

# def cal(fasta,out,type):
#     f = open(fasta)
#     with open(out,'w') as w:
#         for i in f:
#             if i.startswith('>'):
#                 li = i.strip()[1:].split('-')
#                 if len(li) == 3:
#                     length = li[2].split('length:')[1]
#                     line = li[0] + '-' + li[1] + '\t' + length
#                 else:
#                     length = li[3].split('length:')[1]
#                     line = li[0] + '-' + li[1] + '-' + li[2] + '\t' + length
#             else:
#                 line = line + '\t' + i.strip() + '\t' + type + '\n'
#                 w.write(line)
#                 print(line)
#                 line = ''
#     w.close()
#
# for i in os.listdir(path_1):
#     fasta = path_1 + i
#     if i.split('_')[2] == 'phage':
#         type = i.split('_')[0] + ' ' + i.split('_')[1] + ' phages Peptides'
#     else:
#         type = i.split('_')[0] + ' ' + i.split('_')[1] + ' Peptides'
#     out = path_2 + i + '.txt'
#     cal(fasta,out,type)
#


# for i in os.listdir(path_2):
#     print(i.split('.')[-1])
#     os.system("paste %s %s > %s" % (path_2 + i.split('.')[0] + '.' + i.split('.')[1] + '.txt',
#                                   path_2 + i.split('.')[0] + '.' + i.split('.')[1] + '.out',
#                                   path_2 + i.split('.')[0] + '.' + i.split('.')[1] + ".result"))

# for i in os.listdir(path_2):
#     if i.split('.')[-1] == 'result':
#         with open('/home/rzli/ff/peptide/' + i.split('.')[0] + '_' + i.split('.')[1] + '.csv', 'w') as w:
#             f = open(path_2 + i)
#             count = 1
#             for j in f:
#                 print(count, j.strip().split('\t')[1], j.strip().split('\t')[4])
#                 if float(j.strip().split('\t')[4]) >= 0.9:
#                     line = str(count) + '\t' + j.strip() + '\t' + 'High' + '\n'
#                     w.write(line)
#                     count += 1
#                 elif float(j.strip().split('\t')[4]) > 0.5 and float(j.strip().split('\t')[4]) < 0.9:
#                     line = str(count) + '\t' + j.strip() + '\t' + 'Medium' + '\n'
#                     w.write(line)
#                     count += 1
#         w.close()

# os.system("cat /home/rzli/ff/peptide/*csv > %s" % (path_2 + 'tmp.csv'))

f = open('/home/rzli/ff/peptide/tmp.csv')
count = 1

with open('/home/rzli/ff/peptide/peptide.csv','w') as w:
    for j in f:
        line = str(count) + '\t' + j.strip() + '\t' + 'Seq' + '\n'
        w.write(line)
        count += 1
        print(line)
w.close()

