# coding=utf-8
from __future__ import print_function
from data import Vocab
import numpy as np
import os
from gensim.models.word2vec import Word2Vec
embedding_dim=128
vsize = 200000

def wordvec(train=False):
	if os.path.exists('Sougou.word2vec') and not train:
		word_mat = np.fromfile('Sougou.word2vec')
	else:	
		vocab = Vocab('./Big_Sougou/vocab',max_size=vsize)
		word_mat = np.zeros(shape=(vsize,embedding_dim))

		model = Word2Vec.load('./wordvec/sougou.wordvec.40w')
		for idx in range(vsize):
			word = vocab.id2word(idx)
			if word in model.wv:
				embed = model[word]
			else:
				embed = np.random.rand(embedding_dim)
			word_mat[idx]=embed
		word_mat.tofile("Sougou.word2vec")
	return word_mat

if __name__ == '__main__':
