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
	c_e_f = defaultdict(int)
	c_e = defaultdict(int)
	c_j_i_l_m = defaultdict(int)
	c_i_l_m = defaultdict(int)

	for (nu, (de, en)) in enumerate(bitext):
		for (nu, dei) in enumerate(de):
			d_i = defaultdict(float)
			for (nu, eni) in enumerate(en+["###"]):
				d_i[dei] += jointdist[(dei,eni)]
			for (nu, eni) in enumerate(en+["###"]):
				d_i_j = jointdist[(dei,eni)] / d_i[dei]
				c_e_f[(eni,dei)] += d_i_j
				c_e[eni] += d_i_j

	for (nu, (de, en)) in enumerate(bitext):
		for dei in de:
			for eni in en+["###"]:
				if c_e[eni] > 0:
					jointdist[(dei,eni)] = 1.0* c_e_f[(eni,dei)] / c_e[eni]



# Print output
outfile = open("output.txt", "w")
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