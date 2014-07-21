# SimpleVanity Address Generator

## About
This is a vanity address generator for simplewallet. It was tested with Monero's version of simplewallet, but I think it should work for other CryptoNote currencies as well. The script is written in Python and requires only built in modules, and so it should work on Windows, Linux, and Mac. It's tested on Win7 and Debian, and it seems to be a bit faster on Debian.

The script is currently only capable of executing a single thread, and it has to open simplewallet, check output address, and then delete generated files for each address generated. This is slow. I am getting 2 (Windows) to 4 (Debian) addresses generated per second.

## Requirements
You need Python 2.7 (possibly other versions work) and a binary of simplewallet (a new enough version that it produces the electrum seed during wallet generation).

## Usage
The program is run from the terminal, and it must have simplewallet in the same directory. The arguments are passed as follows:
```
./simplevanity.py wallet_file_name wallet_pw target_string
```
if the -m option is specified, then it will attempt to match the target string anywhere in the address rather than just at the beginning
```
./simplevanity.py -m wallet_file_name wallet_pw target_string
```
The program will inform you how many attempts it expects to have to make when you launch it. You can estimate the amount of time it will take based on this number and the number of attempts you are getting per second.

## Issues
For some reason, the second character in the address is not able to be all values, only 0-9, A, and B. So, by default, the program attempts to match from the 3rd character onwards. If you include the -m flag, then it will try and match your target string anywhere in the address. 

Also, it's slow. I may try and make it multi-threaded if I get a chance.