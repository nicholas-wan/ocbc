# OCBC Scraper
Download CSVs for your Debit and Credit card transactions from the OCBC website with Selenium webscraper, then parse and process them into easy to use CSV formats.


# Usage
- Create a conda environment with `python==3.7`
- Install the packages required in `requirements.txt`
- Install `Chromedriver` and ensure you have a matching version of `Google Chrome`
```
>>> python ocbc.py 
```
- Log into the OCBC website with Singpass QR code
- Authorize the web session with your OCBC app

### Parameters

```
# Select the option that suits your OCBC account
-t, --type, choices=['credit','debit','both'], default='both'

# Select yes or no to open a web browser to obtain the altest data
-d, --download, choices=['yes','no'], default='no'

>>> python ocbc.py -t credit
```

### Output
```
+----+------------+----------------------+-----------+----------+------------------------------+
|    | Date       | Memo                 |   Outflow |   Inflow | Payee                        |
+====+============+======================+===========+==========+==============================+
|  0 | 28/06/2022 | DEBIT PURCHASE       |     50    |      nan |  Grab*    S 26/06/22         |
+----+------------+----------------------+-----------+----------+------------------------------+
|  1 | 24/06/2022 | DEBIT PURCHASE       |     50    |      nan |  Grab*    S 22/06/22         |
+----+------------+----------------------+-----------+----------+------------------------------+
|  2 | 07/06/2022 | FUND TRANSFER        |     5.5   |      nan | OTHR - PayNow Transfer       |
+----+------------+----------------------+-----------+----------+------------------------------+
```