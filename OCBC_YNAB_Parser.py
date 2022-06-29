import csv
import sys
import os

# https://github.com/fongming/OCBC-YNAB-Parser

def clean_csv(filename, outfile):
    """
    input: filename (str) - path to raw csv file to be processed
           outfile (str) - path to save the processed csv. Will append suffix _credit or _debit
    """
    if check_file_processed(outfile):
        print('File already processed. Skipping: [', outfile,']')
        return
    print('Reading file:[',filename,']')
    file1 = open(filename) # opens the csv file to read
    file2 = open(outfile,'wt') # opens the csv file to write
    reader = csv.reader(file1)
    writer = csv.writer(file2)
    csvList = list(reader)
    category = ''
    if "Available" in csvList[1][0]:
        myList = list(filter(None, csvList[6:]))   # remove header lines of account information from file
                                            # also removes empty rows
        for row in myList:
            del row[1]                      # remove "Value date" column
            row.insert(4, "")               # insert empty column at end for "Payee"

        for i in range(0,len(myList)):
            if myList[i][0] == '':          # copy description of transaction to previous row's "Payee" column
                myList[i-1][4] = myList[i][1]

        myList = [row for row in myList if row[0] != ""]    # remove rows with empty first cell
        writer.writerow(("Date", "Memo", "Outflow", "Inflow", "Payee"))
        writer.writerows(myList)
        category = 'debit'

    elif "Credit limit" in csvList[1][0]:
        myList = list(filter(None, csvList[7:]))   # remove header lines of account information from file
        myList = [row for row in myList if row[0][0].isdigit()] # remove header lines of supp cards
        writer.writerow(("Date", "Payee", "Outflow", "Inflow"))
        writer.writerows(myList)
        category='credit'

    else:
        print('Error, unrecognized file')
    file1.close()
    file2.close()

    new_outfile = outfile.replace('.csv', '_'+category+'.csv')
    os.rename(outfile, new_outfile)
    print('Processed csv to: [', new_outfile, ']')

def check_file_processed(outfile):
    """
    input: outfile (string) - output path of csv
    output: Boolean - True if file has already been processed
    """

    new_outfile_debit = outfile.replace('.csv', '_debit.csv')
    new_outfile_credit = outfile.replace('.csv', '_credit.csv')
    if os.path.exists(new_outfile_debit):
        return True
    if os.path.exists(new_outfile_credit):
        return True
    return False