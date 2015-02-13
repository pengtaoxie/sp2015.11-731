import optparse
import sys
from collections import defaultdict

bitext = [[sentence.strip().split() for sentence in pair.split(' ||| ')] for pair in open("data/dev-test-train.de-en")][:sys.maxint]
jointdist = defaultdict(float)
for (nu, (de, en)) in enumerate(bitext):
	for dei in de:
		for eni in en+["###"]:
			jointdist[(dei,eni)] = 1.0
# EM learning
for it in range(0,20):
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
#decoding
outfile = open("output_iters7.txt", "w")
for (de, en) in bitext:
	de_en = []
	for (i, dei) in enumerate(de):
		ipos = 1.0 * i / len(de)
		maxen = 0
		jmax = 0
		posmax = sys.float_info.max
		for (j, enj) in enumerate(en):
			jpos = 1.0 * j / len(en)
			if jointdist[(dei,enj)] > maxen or ( jointdist[(dei,enj)] == maxen and abs(jpos-ipos) < abs(posmax-ipos) ):
				maxen = jointdist[(dei,enj)]
				jmax = j
				posmax = jpos
		de_en += [ (i,jmax) ]
	en_de = []
	for (j, enj) in enumerate(en):
		jpos = 1.0 * j / len(en)
		maxde = 0
		imax = 0
		posmax = sys.float_info.max
		for (i, dei) in enumerate(de):
			ipos = 1.0 * i / len(de)
			if jointdist[(dei,enj)] > maxde or ( jointdist[(dei,enj)] == maxde and abs(ipos-jpos) < abs(posmax-jpos) ):
				maxde = jointdist[(dei,enj)]
				imax = i
				posmax = ipos
		en_de += [ (imax,j) ]
	for (i,j) in set(de_en) & set(en_de):
		outfile.write("%i-%i " % (i,j))
	outfile.write("\n")
outfile.close()