# -*- coding: utf-8 -*-

''' Function library for
for006.dat MISSILE DATCOM output file
parsing
Author: Ruben Di Battista <ruben.dibattista@skywarder.eu>
Version: 0.01a
License: Read LICENSE file

 '''

import re;
import numpy as n;
import scipy.io as s;

''' Function to split the output file in all the blocks
that contains the aerodynamic values. It returns a list
with all the blocks'''

def block_split(file_handler):
    pattern = re.compile(r'\*+ \bFLIGHT CONDITIONS AND REFERENCE QUANTITIES \*+');
    linestring = file_handler.read();

    blocks=pattern.split(linestring);
    #Useless first block
    blocks = blocks[1:len(blocks)];
    
    return blocks;

''' This function is intended to retrieve all the starting values
of each block parsed by block_split()'''

def get_data(blocks):
    pattern1 = re.compile(r' *\bMACH NO\b *= * (-*[\d]+.[\d]*)');
    pattern2 = re.compile(r' *\bALTITUDE\b *= * (-*[\d]+.[\d]*)');
    pattern3 = re.compile(r' *\bSIDESLIP\b *= * (-*[\d]+.[\d]*)');
    pattern4 = re.compile(r' *\bMOMENT CENTER\b *= * (-*[\d]+.[\d]*)')


    machs=[];
    alts=[];
    sslips=[];
    mcenter=[];
    
    for block in blocks:
        machs.append(float(pattern1.search(block).group(1)));
        alts.append(float(pattern2.search(block).group(1)));
        sslips.append(float(pattern3.search(block).group(1)));
        mcenter.append(float(pattern4.search(block).group(1)));
    
    return (n.asarray(machs), n.asarray(alts), n.asarray(sslips),
            n.asarray(mcenter));
            
''' This small function replace all the bad character in a list of strings
with a _ and a '' (last character) '''

def replaceBadChars(listofStrings):
    list = [];
    pattern = re.compile(r'[./\-]');
    
    for name in listofStrings:
        list.append(pattern.sub('_',name[0:len(name)-1])+
        pattern.sub('',name[len(name)-1]));
        
    return list;

''' This function strip the whitespaces among coefficients name and
returns a list with the name of the coefficients for each block '''

def get_coeffs_name(blocks):
    cnames = [];
    pattern = re.compile(r' *\bALPHA\b *([\w -/]*)');


    for block in blocks:
        cnames.append(pattern.findall(block));
    
        cnames_ok = [];

        #Loop for stripping middle whitespaces
        for cname in cnames:
            ''' If coefficient are written in two lines i have for single cname a list object. I join the multiple list in one
            then i strip the extra whitespaces'''
            if len(cname)>1:
                dummy=' '.join(cname);
                dummy = dummy.split();
                dummy = replaceBadChars(dummy);
                cnames_ok.append(dummy);
            else:
                for c in cname:
                    dummy = c.split();
                    dummy = replaceBadChars(dummy);
                    cnames_ok.append(dummy);

    return cnames_ok;
''' This function loop over the blocks and returns all the data in a 
list
---- OUTPUT 
- raw_data: the output tuple with all the cofficients
- alpha: the AoA values
'''
def get_rawdata(blocks):
    #All the numbers or dashes followed by a number;
    pattern = re.compile('[-\d](?=[\d\.])')
    pattern2 = re.compile(r'\n\t?')

    raw_data = []
    
    for block in blocks:
        # Splitting the block in lines
        lines = pattern2.split(block);
        new_1 = [];
        
        #Looping over the lines,
        # if they match the pattern
        # i get the values
        for line in lines:
            line = line.strip();
            
            if pattern.match(line):
                new_2=[];
                service_list = line.split();
                
                for num in service_list:
                    new_2.append(float(num));
                new_1.append(new_2);
                
                #END FOR SERVICE_LIST
            #ENDIF
        #ENDFOR LINE
    
        # Dividing the alphas value from 
        # the coefficients value;
        alpha = [];
        new_1_1 = [];
        for row in new_1:
            alpha.append(row[0]);
            new_1_1.append(row[1:len(new_1)]);
        size = len(new_1_1[0]);
        new_1 = new_1_1;
    
            
        # Checking if the current block has
        # two tables
    
    
        i=0;
        for row in new_1_1:
            if not(len(row)==size):
                break;
            i = i+1;
    
        # If it has "i" less than the length 
        # of the array new_1_1 I have to merge the rows
        # of the first block with the second
        if i<len(new_1_1):
            new_1 = [];
            new_2_2=new_1_1[i:len(new_1_1)];
            new_1_1=new_1_1[0:i];
        
            for row1,row2 in zip(new_1_1,new_2_2):
                new_1.append(row1+row2);

                
            #And the alpha array is got twice
            # so it has to be splitted
        
                alpha = alpha[0:len(alpha)/2];      

     
    
            
    
        #Create Array    
        raw_data.append(n.asanyarray(new_1));

    return n.asarray(alpha),raw_data;

''' Main function that parse all the text file and save the data
tables in .mat file '''

def savemat (filename):  
    import numpy as n;
    #Open the file
    fh = open(filename);
    
    #Use the filename for output
    filename = filename.split('.dat')[0];
    
    #Split the blocks 
    blocks = block_split(fh);
    
    #Retrieve Coeffs name
    names = get_coeffs_name(blocks);
    
    #Retrieve reference values of Mach NO, Altitude , Sideslip
    [M,A,B,XM] = get_data(blocks);
    
    #Coefficients "matrix" and AoA values
    alpha,data = get_rawdata(blocks);
    
    #Creating the coefficient list without replications
    realM = [];
    realA = [];
    realB = [];
    realXM = [];
    
    realM.append(M[0]);
    realA.append(A[0]);
    realB.append(B[0]);
    realXM.append(XM[0]);
    
    for i in range(len(M)):
        if not(M[i] in realM):
            realM.append(M[i]);
        if not(A[i] in realA):
            realA.append(A[i]);
        if not(B[i] in realB):
            realB.append(B[i]);
        if not(XM[i] in realXM):
            realB.append(XM[i]);
    
    # Creating State Dictionary with all the state variables
    stateDict = {'Machs':realM,
                 'Alphas':alpha,
                 'Betas':realB,
                 'Altitudes':realA,
                 'Mom. Center':realXM
                 };
        
    
    #Num. of elements
    lM = len(realM);
    lA = len(realA);
    lB = len(realB);
    lalpha = len(alpha);
    
    #Checking how many indipendent blocks i have
    cname = names[0][0];
    j=1;
    for i in range(len(blocks)):
        new_cname = names[i+1][0];
        
        if new_cname == cname:
            break;
        j=j+1;
        
    #Joining all the coefficients names of the j indipendent blocks
    totalc = [];
    for i in range(j):
        totalc = totalc + names[i];
    
        
    #Number of coefficients
    numofc = len(totalc);
    
    final_data = {};
    #I have to generate <numofc> 4D matrixes (preallocation)
    for i in range(numofc):
        final_data[totalc[i]]=n.zeros((lalpha,lM,lB,lA));
    
    # Filling the 4D matrixes with data
    currentBigBlock = n.zeros((lalpha,numofc));
    
    iM = 0;
    iB = 0;
    iA = 0;
    for i in range(0,len(blocks),j):
        
        #Joining the j indipendent blocks in one
        l=0;
        for k in range(i,i+j,1):
            #Sizes
            n,m = data[k].shape;
            currentBigBlock[:,l:l+m]=data[k];
            l=l+m;
            
        #Populating the final data matrix
        for cname,iC in zip(totalc,range(numofc)):
            final_data[cname][:,iM,iB,iA] = currentBigBlock[:,iC]
        
        #Checking which parameter has changed
        
        if iM < lM-1:
            iM=iM+1;
        else:
            iM=0;
            if iB < lB-1:
                iB = iB+1;
            else:
                iB=0;
                iA = iA+1;
            
    #Salvo in Matlab
    s.savemat(filename+'.mat',mdict={'Coeffs':final_data,
                                'State':stateDict
                                });
    

