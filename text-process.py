# -*-coding:utf-8-*-  
from __future__ import print_function
import os  
import struct  
import collections  
from tensorflow.core.example import example_pb2  
# import tf
  
# We use these to separate the summary sentences in the .bin datafiles  
SENTENCE_START = '<s>'  
SENTENCE_END = '</s>'  
  
train_file = "./raw_data/train.txt"  
val_file = "./raw_data/val.txt"  
test_file = "./raw_data/test.txt"

# finished_files_dir='./Sougou'
finished_files_dir = "./Big_Sougou"  
  
VOCAB_SIZE = 200000  


  
def read_text_file(text_file):  
  lines = []  
  with open(text_file, "r") as f:  
    for line in f:  
      lines.append(line.strip())  
  return lines  

def write_to_bin(input_file,out_file, makevocab=False):  

  if makevocab:
    vocab_counter = collections.Counter()
    vocab_counter_pos = collections.Counter()


  with open(out_file,'wb') as writer:
  # read the  input text file , make even line become article and odd line to be abstract（line number begin with 0）  
    lines = read_text_file(input_file)  
   # print(lines[0])
    for i, new_line in enumerate(lines):  
      if i % 3 == 0:  
        article = lines[i]  
      if i % 3 == 1: 
      	abstract = "%s %s %s" % (SENTENCE_START, lines[i], SENTENCE_END)  
      if i % 3 == 2:
        POS_tag= lines[i]
        if len(article.split()) == 0 or len(POS_tag.split()) == 0:
          continue
        # Write to tf.Example  
        tf_example = example_pb2.Example()
        tf_example.features.feature['article'].bytes_list.value.extend([article])  
        tf_example.features.feature['abstract'].bytes_list.value.extend([abstract])  
        tf_example.features.feature['POS_tag'].bytes_list.value.extend([POS_tag])

        tf_example_str = tf_example.SerializeToString()  

        str_len = len(tf_example_str)  
        writer.write(struct.pack('q', str_len))  
        writer.write(struct.pack('%ds' % str_len, tf_example_str))  

        #Write the vocab to file, if applicable  
        if makevocab:
          art_tokens = article.split(' ')
          abs_tokens = abstract.split(' ') 
          pos_tokens = POS_tag.split(' ')

          abs_tokens = [t for t in abs_tokens if t not in [SENTENCE_START, SENTENCE_END]] # remove these tags from vocab  
          tokens = art_tokens + abs_tokens  
          tokens = [t.strip() for t in tokens] # strip  
          tokens = [t for t in tokens if t!=""] # remove empty  

          vocab_counter.update(tokens)  
          vocab_counter_pos.update(pos_tokens)
    
  if makevocab:
    print ("Writing word vocab file..."  )
    with open(os.path.join(finished_files_dir, "vocab"), 'w') as writer:  
      for word, count in vocab_counter.most_common(VOCAB_SIZE):
        writer.write(word + ' ' + str(count) + '\n') 

    print('Writing word Part_of_speech vocab file...')
    with open(os.path.join(finished_files_dir, "vocab_pos"), 'w') as writer:  
      for word, count in vocab_counter_pos.items():  
        writer.write(word + ' ' + str(count) + '\n')  
      
    print ("Finished writing vocab file")
  print ("Finished writing file %s\n" % out_file)
  
   

def split_text():
  fc = open('./source_data/content_fenci_exp','r')
  ft = open('./source_data/title_fenci_exp','r')
  fpos = open('./source_data/POS_feature')

  article = [line for line in fc]
  title = [line for line in ft]
  POS_feature = [line for line in fpos]

  print('article num:',len(article))
  cnt_article = 0
  if len(article)!=len(title) or len(POS_feature) != len(article) or len(title) != len(POS_feature):
  	raise Exception('Article content and title and POS_feature should have same length')
  for idx in range(len(article)):
  	len1 = len(article[idx].strip().split())
  	len3 = len(POS_feature[idx].strip().split())
  	if len3 != len1:
  		print(idx,len1,len3)
  		print(article[idx],POS_feature[idx])
  		raise Exception('One example of content and POS should have the same length')
  # exit(0)
  
  fcw = open(train_file,'w')
  for idx in range(2000,len(article)):
    fcw.write(article[idx])
    fcw.write(title[idx])
    fcw.write(POS_feature[idx])
  fcw.close()

  fcw = open(val_file,'w')
  for idx in range(2000):
    fcw.write(article[idx])
    fcw.write(title[idx])
    fcw.write(POS_feature[idx])
  fcw.close()

  fcw = open(test_file,'w')
  for idx in range(2000):
    fcw.write(article[idx])
    fcw.write(title[idx])
    fcw.write(POS_feature[idx])
  fcw.close()

# def write_vocab():
  


if __name__ == '__main__':  
  split_text()
  if not os.path.exists(finished_files_dir): 
    os.makedirs(finished_files_dir)  

  # Read the text file, do a little postprocessing then write to bin files  
  write_to_bin(test_file, os.path.join(finished_files_dir, "test.bin"))  
  write_to_bin(val_file, os.path.join(finished_files_dir, "val.bin"))  
  write_to_bin(train_file, os.path.join(finished_files_dir, "train.bin"),makevocab=True) 

  # write_vocab()
