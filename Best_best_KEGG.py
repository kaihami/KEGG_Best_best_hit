'''
@author: Gilberto Kaihami
Find best-best hit from KEGG DB
'''

import os
from bs4 import BeautifulSoup
from urllib2 import urlopen
from multiprocessing import cpu_count, Pool
import datetime
from Bio.KEGG.REST import kegg_get
import itertools
import sys


def KEGG_best_hit(locus):
    # Save best_genes herewhile True:

    # Open page
    open_kegg = urlopen('http://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=' + locus)
    best_list = []
    page = open_kegg.read()

    # make soup
    soup = BeautifulSoup(page)

    # find best genes
    tt = soup.find_all("input", {'type': 'checkbox'})
    for elem in tt:
        value = elem.get('value')
        if value:
            best_list.append(value)
    return best_list

def NCBI_DB(Fasta_file, output_file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    makeblastdb_path = os.path.join(dir_path, 'makeblastdb.exe')
    os.system(makeblastdb_path+" -in " + Fasta_file + " -dbtype prot -out " + output_file)

def BLAST(q, DB, output):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    command_path = os.path.join(dir_path,'blastp.exe' )
    os.system(command_path+' -db ' + DB + " -query " + q + " -outfmt 5 -num_alignments 2000" + " -out " + output)

def Muscle(fasta_file, output,logoutput):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    command_path = os.path.join(dir_path, 'muscle.exe')
    os.system(command_path + " -in " +fasta_file+ " -out "+ output+ " -log "+ logoutput)


class someClass():
    def __init__(self):
        self.haha = "haha"
        pass

    def is_best_best(self,args):


        (locus, gene) = args
        c = ""

        while True:
            try:

                start_mid = datetime.datetime.now().replace(microsecond=0)
                # Open page
                open_kegg = urlopen('http://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=' + gene)
                page = open_kegg.read()

                # make soup
                soup = BeautifulSoup(page)

                tt = soup.find_all("input", {'type': 'checkbox'})
                for elem in tt:
                    value = elem.get('value')
                    if value:
                        if locus in value:
                            c = gene

                end_mid = datetime.datetime.now().replace(microsecond=0)
                print "Parcial time: %s" % (end_mid - start_mid)

            except:
                continue
            break
        return c

    def go(self,to_find,query1):
        #a = n+m
        #p = Pool(4)
        #sc = p.map(self, range(a))
        #print sc
        #self.is_best_best((to_find,query1))
        self.number_processes = (cpu_count() - 1)*8
        self.pool = Pool(self.number_processes)

        results = self.pool.map(self, itertools.izip(itertools.repeat(to_find), query1))
        self.pool.close()
        self.pool.join()

        return results

    def __call__(self, args):
        return self.is_best_best(args)
    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict
    def __setstate__(self, state):
        self.__dict__.update(state)

class AnotherStupidClass():
    def __init__(self):
        self.haha = "haha"
        pass

    def find_kegg_fasta(self,args):
        (locus) = args

        c = []
        get_fasta_protein1 = kegg_get(locus, "aaseq")

        fasta_locus_protein1 = get_fasta_protein1.read()
        fasta_formatted_protein1 = fasta_locus_protein1.split('\n')
        without_space_protein1 = ''.join(fasta_formatted_protein1[1:len(fasta_formatted_protein1)])
        c.append(locus)
        c.append(without_space_protein1)

        return c

    def go(self,locus):
        #a = n+m
        #p = Pool(4)
        #sc = p.map(self, range(a))
        #print sc
        #self.is_best_best((to_find,query1))
        self.number_processes = (cpu_count() - 1)*12
        self.pool = Pool(self.number_processes)

        results = self.pool.map(self, locus)
        self.pool.close()
        self.pool.join()
        return results

    def __call__(self, args):
        return self.find_kegg_fasta(args)
    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict
    def __setstate__(self, state):
        self.__dict__.update(state)
def main():
    # print command line arguments
    for arg in sys.argv[1:]:
        print arg
    locus = sys.argv[1]
    print locus
    print "Getting Best Hit of:", locus
    PA00800 =KEGG_best_hit(locus)
    print "total:", str(len(PA00800))
    query_2_class = someClass()

    go_best_best_2 = query_2_class.go(locus,PA00800) #locus, list of genes
    a = []
    for ele in go_best_best_2:
        if ele != "":
            print ele
            a.append(ele)
    fasta_protein_class1 = AnotherStupidClass()
    go_fasta_protein1 = fasta_protein_class1.go(a)
    dr = os.path.dirname(os.path.realpath(__file__))
    out_dir = os.path.join(dr,locus.split(":")[1]+".txt")
    for ele2 in go_fasta_protein1:
        if ele2 != "":
            with open(out_dir, 'a') as fi:
                head = ele2[0]
                seq = ele2[1]
                fi.write(">")
                fi.write(head)
                fi.write("\n")
                fi.write(seq)
                fi.write("\n")
if __name__ == "__main__":
    main()
