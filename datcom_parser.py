# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 00:16:41 2013
'Main Scripting Function'
@author: rubendibattista
"""
if __name__ == "__main__":
    import functions as f
    import argparse
    
    parser = argparse.ArgumentParser(description='Parse the DATCOM output file');
    
    parser.add_argument('filename',nargs='?',help='''The name of the DATCOM 
    output file. Default: "for006.dat"''',default='for006.dat');
    
    args = parser.parse_args();
    
    f.savemat(args.filename);