# skyward-datcom-parser
A simple Python script to parse Missile Datcom Output File

This simple Command Line script converts the for006.dat Missile Datcom 97 output file to a MATLAB .mat file. It has been implement to retrieve the data for a standard simulation without deflections. 

The version is pre-alpha so it could behave very buggy. 

## Usage ##

```
python datcom_parser.py filename
```

The filename is optional. Without it the parser will look for the `for006.dat' file.

## Output File ###
The Output file is composed by two structures: `Coeffs` and `State`. 
`Coeffs` contains all the aerodynamic coefficients interpolated over the 4 states (AoA, Mach, Altitude, Sidesplip angles) and the struct `State` contains the set of states (Aoa, Mach, Altitude, Sideslip Angle) the coefficients have been calculated on and the position of the center of gravity.

```
Coeffs = 

      CAQ: [4-D double]
     CLNP: [4-D double]
      CMA: [4-D double]
    CL_CD: [4-D double]
      CMQ: [4-D double]
     CLNB: [4-D double]
      CYR: [4-D double]
      CYP: [4-D double]
     CMAD: [4-D double]
      CNQ: [4-D double]
      CYB: [4-D double]
     CNAD: [4-D double]
      CLL: [4-D double]
      CLN: [4-D double]
       CN: [4-D double]
       CM: [4-D double]
       CL: [4-D double]
       CA: [4-D double]
       CD: [4-D double]
       CY: [4-D double]
     CLNR: [4-D double]
      CNA: [4-D double]
     CLLB: [4-D double]
     CLLP: [4-D double]
     CLLR: [4-D double]
    X_C_P: [4-D double]
```
State = 

      Altitudes: [3x1 double]
         Alphas: [19x1 double]
    Mom. Center: 1.5500
          Betas: [5x1 double]
          Machs: [3x1 double]

```
