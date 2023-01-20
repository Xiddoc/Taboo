# Taboo
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