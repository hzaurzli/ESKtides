with open('/home/rzli/Salmonella-peptide.fasta') as f:
    with open('/home/rzli/Salmonella-peptide-select-6-20.fasta','w') as w:
        for i in f:
            if i.startswith('>'):
                if int(i.strip().split(':')[1]) <= 20 and int(i.strip().split(':')[1]) >= 6:
                    line = i
                else:
                    pass
            else:
                if len(i.strip()) <= 20 and len(i.strip()) >= 6:
                    line = line + i.strip() + '\n'
                    print(line)
                    w.write(line)
    w.close()
f.close()