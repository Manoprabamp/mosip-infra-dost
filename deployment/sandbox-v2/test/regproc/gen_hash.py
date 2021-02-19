#!/bin/python3.6
# This scripts generates packet hash and OSI hash. 
# Usage (example):
# ./gen_hash.py data/packet/packet1/unencrypted/id/packet_meta_info.json 

import sys
import json
import os
import hashlib 
import glob

def gen_path_dict(base):
    # Generate file path dictionary
    file_paths = glob.glob(os.path.join(base, '**'), recursive=True)
    path_dict = {}
    for f in file_paths:
        path_dict[os.path.basename(f).split('.')[0]] = f
    return path_dict

def gen_hash(j, label, path_dict):
    '''
    j: meta info json
    label: as in 'hashSequence1', 'hashSequence2' as defined in meta
    '''
    if len(j['identity'][label]) == 0:
        return ''

    files =  [x['value'] for x in j['identity'][label]]
    files = [x for f in files for x in f]  # Flatten 
    h = hashlib.sha256()
    for f in files:
        h.update(open(path_dict[f], 'rb').read()) 

    return h.hexdigest().upper()


def main():
    meta_path = sys.argv[1]

    fp = open(meta_path, 'rt')
    meta_j = json.load(fp)

    base = os.path.dirname(meta_path)
    path_dict =  gen_path_dict(base)
    hash1 = gen_hash(meta_j, 'hashSequence1', path_dict)
    if hash1:
        open(os.path.join(base, 'packet_data_hash.txt'), 'wb').write(hash1.encode())

    hash2 = gen_hash(meta_j, 'hashSequence2', path_dict)
    if hash2:
        open(os.path.join(base, 'packet_operations_hash.txt'), 'wb').write(hash2.encode())
    
if __name__== '__main__':
    main()






