#!/usr/bin/env python
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
from collections import Counter
 
def word_matches(h, ref):
  return sum(1 for w in h if w in ref)
  # or sum(w in ref for w in f) # cast bool -> int
  # or sum(map(ref.__contains__, h)) # ugly!

def pr(h, ref):
  hset = set(h)
  rset = set(ref)
  com = hset & rset
  p = float(len(com))/len(hset)
  r = float(len(com))/len(rset)
  return p, r


def fscore(p, r, a):
  b = (a**2)*p + r
  if b==0: return 0
  return ((1+(a**2))*p*r)/b

def ng(st, n):
  ngs = []
  for i in range(len(st)-n+1):
    ngs.append(' '.join(st[i:i+n]))
  return ngs

 
def main():
  parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
  # PEP8: use ' and not " for strings
  parser.add_argument('-i', '--input', default='data/train-test.hyp1-hyp2-ref',
            help='input file (default data/train-test.hyp1-hyp2-ref)')
  parser.add_argument('-n', '--num_sentences', default=None, type=int,
            help='Number of hypothesis pairs to evaluate')
  parser.add_argument('-g', '--gold', help='gold data for dev')
  # note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
  opts = parser.parse_args()

  # we create a generator and avoid loading all sentences into a list
  def sentences():
    with open(opts.input) as f:
      for pair in f:
        yield [sentence.strip().lower().decode('utf8').split() for sentence in pair.split(' ||| ')]
 
  # note: the -n option does not work in the original code
  for h1, h2, ref in islice(sentences(), opts.num_sentences):
    h1 += ng(h1, 2) + ng(h1, 3)
    h2 += ng(h2, 2) + ng(h2, 3)
    ref += ng(ref, 2) + ng(ref, 3)
    h1_p, h1_r = pr(h1, ref) 
    h2_p, h2_r = pr(h2, ref) 
    h1_f, h2_f = fscore(h1_p, h1_r, 3), fscore(h2_p, h2_r, 3)
    print(-1 if h1_f > h2_f else 
           (0 if h1_f == h2_f
             else 1)) 
 
# convention to allow import of this file as a module
if __name__ == '__main__':
    main()