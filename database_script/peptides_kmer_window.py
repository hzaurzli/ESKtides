import os


def load_fa(path):
    """a function to read fasta file from the path and store in a dict"""
    genes_seq = {}  #将序列存入字典
    with open(path,"r") as sequences:  #以读取方式打开文件
        lines = sequences.readlines()

    for line in lines:
        if line.startswith(">"):
            genename = line.split()[1]  #这个地方需要灵活调整
            genes_seq[genename] = ''  #序列为字符串
        else:
            genes_seq[genename] += line.strip()

    return genes_seq


def build_kmers(seq, k_size,shift):
    """a function to calculate kmers from seq"""
    kmers = []  # k-mer存储在列表中
    n_kmers = len(seq) - k_size + 1

    for i in range(0,n_kmers,int(shift)+1):
        kmer = seq[i:i + k_size]
        kmers.append(kmer)

    return kmers

#
# with open('/home/rzli/Salmonella-6.fasta','w') as w:
#     for key in aa:
#         # print(build_kmers(aa[key],10))
#         bb = build_kmers(aa[key],6,0)
#         count = 1
#         for i in bb:
#             print(i)
#             f = '>' + key + '-' + str(count) + '\n'
#             s = i + '\n'
#             line = f + s
#             w.write(line)
#             count += 1
# w.close()


# with open('/home/rzli/Ecoli-peptide.fasta','w') as w:
#     for j in range(6,61):
#         for key in aa:
#             # print(build_kmers(aa[key],10))
#             bb = build_kmers(aa[key],j,0)
#             count = 1
#             for i in bb:
#                 print(i)
#                 f = key + '-' + str(count) + '-' + 'length:' + str(j) + '\n'
#                 s = i + '\n'
#                 line = f + s
#                 w.write(line)
#                 count += 1
# w.close()

for i in os.listdir('/home/rzli/aa'):
    aa = load_fa('/home/rzli/aa/' + i)
    j = i.split('.')[0]
    with open('/home/rzli/' + j + '-peptide.fa','w') as w:
        for j in range(35,45):
            for key in aa:
                # print(build_kmers(aa[key],10))
                bb = build_kmers(aa[key],j,0)
                count = 1
                for i in bb:
                    # print(i)
                    f = '>' + key + '-' + str(count) + '-' + 'length:' + str(j) + '\n'
                    s = i + '\n'
                    line = f + s
                    w.write(line)
                    count += 1
    w.close()

