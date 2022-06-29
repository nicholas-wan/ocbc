import time
import os
import pandas as pd
import argparse
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import OCBC_YNAB_Parser

parser = argparse.ArgumentParser()
parser.add_argument('--download', '-d', choices=['yes','no'], default='yes', type=str, help='yes to obtain the latest stats, else no')
parser.add_argument('--types', '-t', choices=['credit','debit','both'], default='both', type=str)

args = parser.parse_args()

csv_dir = os.path.join(os.getcwd(), 'csv')
raw_data_dir = os.path.join(csv_dir, 'raw_data')
processed_data_dir = os.path.join(csv_dir, 'processed')

if __name__=="__main__":

    ##########################################
    #### Downloads CSVs from OCBC website ####
    ##########################################

    if args.download=='yes':
        # Sets default download directory to to path of your choice
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : raw_data_dir }
        chromeOptions.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(options=chromeOptions)

        # Visits the singpass login page directly. 
        driver.get('https://internet.ocbc.com/internet-banking/Login/Login?sp=true')

        def wait_for_element(xpath, seconds = 20):
            WebDriverWait(driver, seconds).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

        while 'Login' in driver.current_url:
            time.sleep(1)
            if 'Dashboard' in driver.current_url:
                break

        # Download CSV for Debit Account
        if args.types in ['debit','both']:
            try:
                wait_for_element("//a[contains(@href, 'DepositAccountDetail')]")
                debit_page = driver.find_element(By.XPATH,"//a[contains(@href, 'DepositAccountDetail')]").get_attribute('href')
                driver.get(debit_page)

                wait_for_element("//a[@id='btn-download']")
                driver.get('https://internet.ocbc.com/internet-banking/DepositAccountDetail/ExportCSV')
            except:
                print('Error obtaining debit transaction CSV')
            
            driver.get('https://internet.ocbc.com/internet-banking/dashboardpage/')

        if args.types in ['credit','both']:
            # Download CSV for Debit Account
            try:
                wait_for_element("//a[contains(@href, 'CCAccountDetail/Index/')]")
                credit_page = driver.find_element(By.XPATH,"//a[contains(@href, 'CCAccountDetail/Index/')]").get_attribute('href')
                driver.get(credit_page)
                wait_for_element("//a[@class='btn-download']")
                driver.get('https://internet.ocbc.com/internet-banking/CCAccountDetail/ExportCSV')
            except:
                print('Error obtaining credit transaction CSV')

        time.sleep(3)
        driver.close()

    ##################################
    #### Process Downloaded CSVs  ####
    ##################################

    raw_files = [x for x in os.listdir(raw_data_dir) if '.csv' in x]
    
    ### Get balance in debit account

    debit_balance = -1

    for i in range(len(raw_files)):
        filepath = os.path.join(raw_data_dir, raw_files[i])
        f = open(filepath, encoding="ISO-8859-1").read()
        if 'DEBIT' in f:
            f = f.split('\n')
            debit_balance = float([x for x in f if 'Available' in x][0].split(',')[1])
            
    print('Debit Balance: ', debit_balance)

    ### Process the CSV files with the parser

    for f in raw_files:
        input_file = os.path.join(raw_data_dir, f)
        output_file = os.path.join(processed_data_dir, f)
        OCBC_YNAB_Parser.clean_csv(input_file, output_file)
