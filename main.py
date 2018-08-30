
#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import os 
import sys
import chardet
import codecs
import getopt
import sys

subtitle_ext = ['srt', 'ass']

def getSubtitleFile(root_dir): 
    files = []

    if os.path.isfile(root_dir):
        for x in subtitle_ext:
            if root_dir.endswith(x):
                files.append(os.path.abspath(root_dir))
    else:
        for lists in os.listdir(root_dir):
            path = os.path.join(root_dir, lists) 

            if os.path.isfile(path): 
                for x in subtitle_ext:
                    if path.endswith(x):
                        files.append(os.path.abspath(path))
                        break
    return files

def detect_file_encoding(file_path):
    f = open(file_path, 'rb')
    data = f.read()
    predict =  chardet.detect(data)
    f.close()
    return predict['encoding']

def write_file(file_path, content):
    fo = codecs.open(file_path, 'w', 'utf-8')
    fo.write(content)
    fo.close()

def del_file(file_path):
    os.remove(file_path)

def check_codec(file_path, c):

    fi = codecs.open(file_path,'rb',c)

    for x in range(50):
        print(fi.readline())

    fi.close()

    str = input("OK? (yes/others)");
    if str != 'yes':
        return False
    return True


def run():
        
    if len(sys.argv) < 2:
        print('python main.py -p [path]')
        exit()

    quite = False
    path = '.'

    try:
        opts,args = getopt.getopt(sys.argv[1:],'p:q',['path=','quite'])

        for opt_name,opt_value in opts:
            if opt_name in ('-p'):
                path = opt_value
            if opt_name in ('-q',):
                quite = True
    except getopt.GetoptError:
        print('python main.py -p [path]')
        exit()


    files = getSubtitleFile(path)

    for f in files:
        print('file :', f)

        c = detect_file_encoding(f)

        print(c)

        if c == 'utf-8':
            print('skip', f)
            continue
        elif c is None:
            # check_codec(f, 'utf-16')
            print ('error ', f)
            continue

        fi = codecs.open(f,'rb',c, errors = 'ignore')

        if quite == False:

            for x in range(50):
                print(fi.readline())
            print(f)
            str = input("OK? (yes/others)");
            if str != 'yes':
                continue

        content = fi.read()
        fi.close()

        del_file(f)
        write_file(f, content)

        print ('conv file ', f)


if __name__ == '__main__':
    run()

