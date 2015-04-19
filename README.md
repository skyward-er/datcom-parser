# skyward-datcom-parser
A simple Python script to parse Missile Datcom Output File

This simple Command Line script converts the for006.dat Missile Datcom 97 output file to a MATLAB .mat files. It has been implement to retrieve the data for a standard simulation without deflections. 

The version is pre-alpha so it could behave very buggy. 

## Usage ##

```
python datcom_parser.py filename
```

The filename is optional. Without it the parser will look for the `for005.dat' file.
