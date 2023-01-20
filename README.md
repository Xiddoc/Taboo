# Taboo

## Liabiltiy / Warning
⚠ **Use this program on your OWN LIABILITY and for EDUCATIONAL PURPOSES ONLY** ⚠

## Summary

A LinkedIn scraper on steroids. Many people accidentally leak confidential information there- this program will 
collect all of it and try and assess patterns with statistics.

## Installing & Setup
We will need to install a few modules for the program to work, you can do this with this command:
```cmd
pip install -r requirements.txt
```

Taboo offers a few built-in output formats for the data, once collected. To create the output, Taboo uses packages
which might be quite large in file size (namely `pandas`), so keep this in mind when installing the Python requirements.

Go ahead and make a `.env` file, which the program will use to login to LinkedIn with. The contents of the `.env` 
file will include the LinkedIn credentials to use, they should be formatted like so:
```.env
email@domain.com=password123
test@example.com=otherpass567
```

## Usage
This README might not be fully updated, feel free to check out all the options and settings by running:
```cmd
python taboo.py -h
```
You will need to specify an output format, otherwise Taboo will just download the data and cache it, then quit. So far
the only offered output format is `excel`. You can specify this target output with the `-f` flag like this:
```cmd
-f excel
```

Taboo offers 2 modes to run the engine. The first allows you to query Google and automatically scrape all the search
results there with the assumption that they are LinkedIn URLs (it will use the path to grab the username). Here's an
example of using this mode to search up cybersecurity researchers at the NSA:
```cmd
python taboo.py -f excel --query +NSA cyber security researcher site:linkedin.com
```
If you already have a curated list of LinkedIn profiles you want to analyze, put them into a file with 
one link on each line, like the following:
```text
https://www.linkedin.com/in/hacker12
https://www.linkedin.com/in/nsa-expert321
https://us.linkedin.com/in/nsa-ceo1234
```
Then you can let Taboo sic the list with the following command:
```cmd
python taboo.py -f excel --infile input_file_list.txt
```