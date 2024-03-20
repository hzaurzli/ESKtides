import argparse
import os,sys,re
import subprocess as sub
from subprocess import *
import glob
import shutil
from Bio import SeqIO
from Bio import AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils.ProtParam import ProteinAnalysis


class tools:
    def __init__(self):
        self.pharokka = 'pharokka.py'
        self.cdHit = '/home/runzeli/software/cdhit/cd-hit/cd-hit'
        self.rundbcan = 'run_dbcan.py'
        self.hmmsearch = 'hmmsearch'
        self.tmhmm = '/home/runzeli/software/tmhmm/tmhmm-2.0c/bin/tmhmm'


    def run(self, cmd, wkdir=None):
        sys.stderr.write("Running %s ...\n" % cmd)
        p = Popen(cmd, shell=True, cwd=wkdir)
        p.wait()
        return p.returncode

    def run_pharokka(self, fastain, out, database, prefix):
        cmd = '%s -i %s -o %s -t 8 -d %s -p %s -f' % (self.pharokka, fastain, out, database, prefix)
        return cmd

    def run_cdhit(self, inputfile, out, cutoff):
        cmd = '%s -i %s -o %s -c %s -M 0' % (self.cdHit, inputfile, out, cutoff)
        return cmd

    def scan_dbscan(self, inputfile, out, db):
        cmd = '%s %s protein -t hmmer --out_dir %s --db_dir %s' % (self.rundbcan, inputfile, out, db)
        return cmd

    def run_hmmsearch(self, tblout, e_val, hmm, inputfile):
        cmd = '%s --tblout %s -E %s --cpu 2 %s %s' % (self.hmmsearch, tblout, e_val, hmm, inputfile)
        return cmd

    def run_tmhmm(self, input_fa, out):
        cmd = '%s %s > %s' % (self.tmhmm, input_fa, out)
        return cmd


def molecular_weight(protein_fa,protein_filter_fa):
    protein_fa_info = open(protein_fa, "r")
    out_file = open(protein_filter_fa, "a")
    molecular_weight = open("./molecular_weight.txt", "w")
    for record in SeqIO.parse(protein_fa_info, "fasta"):
        ID_contig = record.id
        Seq_use = record.seq
        Desp = record.description
        protein_seq = str(Seq_use)
        if 'X' not in protein_seq and '*' not in protein_seq[:-1]:
            X = ProteinAnalysis(protein_seq)
            MW_cal = "%0.2f" % X.molecular_weight()
            if float(MW_cal) <= 40000:
                element_record = SeqRecord(Seq_use, id=ID_contig, description=Desp)
                SeqIO.write(element_record, out_file, "fasta")
                molecular_weight.write(ID_contig + "\t" + MW_cal + "\n")

    protein_fa_info.close()
    molecular_weight.close()






def main():
    tl = tools()
    # step 1 pharokka annotates ORFs
    curr_dir = sub.getoutput('pwd')
    os.chdir(Args.workdir)
    if os.path.isdir('./pharokka_result/') == True:
        pass
    else:
        os.mkdir('./pharokka_result/')

    target = Args.path
    curr_dir_target = curr_dir
    if target[-1] == '/':
        target = target
    elif target[-1] != '/':
        target = target + '/'

    if target[0] == '.':
        if target[1] == '/':
            target_suffix = target[1:]
        elif target[1] == '.':
            curr_dir_target = os.path.abspath(os.path.join(os.path.dirname(curr_dir + '/'), os.path.pardir))
            target_suffix = target[2:]
    else:
        target_suffix = target
        curr_dir_target = ''

    os.mkdir('./pharokka_result/')
    for i in os.listdir(curr_dir_target + target_suffix):
        name = i.split('.')[0]
        suffix = i.split('.')[1]
        cmd_1 = tl.run_pharokka(curr_dir_target + target_suffix + i,
                              './pharokka_result/' + name + '/', name, type_annotation)
        tl.run(cmd_1)


