# -*-coding:utf-8-*-  
from __future__ import print_function
import os  
import struct  
import collections  
from tensorflow.core.example import example_pb2 

article = 'welcome to china'
title = 'so what'
tf_example = example_pb2.Example()

# tf_example.features.feature['article'].bytes_list.value.extend([article])  
# tf_example.features.feature['title'].bytes_list.value.extend([title])
# tf_example_str = tf_example.SerializeToString()  
# str_len = len(tf_example_str)

# print(str_len,tf_example_str)	
# writer = open('learn_writer','wb')
# writer.write(struct.pack('q', str_len))  
# writer.write(struct.pack('%ds' % str_len, tf_example_str)) 
# print(struct.pack('q',str_len))
# print(struct.pack('%ds' % str_len, tf_example_str))
reader = open('learn_writer', 'rb')
len_bytes = reader.read(8)
print(len_bytes)
str_len = struct.unpack('q', len_bytes)[0]
print(str_len)