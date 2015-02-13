import optparse
import sys
from collections import defaultdict

bitext = [[sentence.strip().split() for sentence in pair.split(' ||| ')] for pair in open("data/dev-test-train.de-en")][:sys.maxint]
jointdist = defaultdict(float)
for (nu, (de, en)) in enumerate(bitext):
	for dei in de:
		for eni in en+["###"]:
			jointdist[(dei,eni)] = 1.0

for it in range(0,6):
	sys.stderr.write("EM Iterations "+str(it)+"\n")
	condi_en_de = defaultdict(int)
	condi_en = defaultdict(int)
	## E step
	for (nu, (de, en)) in enumerate(bitext):
		for dei in de:
			margin_de = defaultdict(float)
			for eni in en+["###"]:
				margin_de[dei] += jointdist[(dei,eni)]
			for eni in en+["###"]:
				cd_en_de = jointdist[(dei,eni)] / margin_de[dei]
				condi_en_de[(eni,dei)] += cd_en_de
				condi_en[eni] += cd_en_de
	## M step
	for (nu, (de, en)) in enumerate(bitext):
		for dei in de:
			for eni in en+["###"]:
				if condi_en[eni] > 0:
					jointdist[(dei,eni)] = 1.0* condi_en_de[(eni,dei)] / condi_en[eni]



# Print output
outfile = open("output2.txt", "w")
for (f, e) in bitext:
	list_f_e = []
	for (i, f_i) in enumerate(f):
		i_pos = 1.0 * i / len(f)
		max_e_j_value = 0
		max_j = 0
		max_pos = sys.float_info.max
		for (j, e_j) in enumerate(e):
			j_pos = 1.0 * j / len(e)
			if jointdist[(f_i,e_j)] > max_e_j_value or ( jointdist[(f_i,e_j)] == max_e_j_value and abs(j_pos-i_pos) < abs(max_pos-i_pos) ):
				max_e_j_value = jointdist[(f_i,e_j)]
				max_j = j
				max_pos = j_pos
		list_f_e += [ (i,max_j) ]

	list_e_f = []
	for (j, e_j) in enumerate(e):
		j_pos = 1.0 * j / len(e)
		max_f_i_value = 0
		max_i = 0
		max_pos = sys.float_info.max
		for (i, f_i) in enumerate(f):
			i_pos = 1.0 * i / len(f)
			if jointdist[(f_i,e_j)] > max_f_i_value or ( jointdist[(f_i,e_j)] == max_f_i_value and abs(i_pos-j_pos) < abs(max_pos-j_pos) ):
				max_f_i_value = jointdist[(f_i,e_j)]
				max_i = i
				max_pos = i_pos
		list_e_f += [ (max_i,j) ]

	for (i,j) in set(list_f_e) & set(list_e_f):
		outfile.write("%i-%i " % (i,j))
	outfile.write("\n")

outfile.close()