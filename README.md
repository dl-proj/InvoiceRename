# InvoiceRename

## Overview

This project is to extract the invoice number from the pdf file on AWS s3 bucket using AWS Textract and move the file into
the renamed file with the extracted invoice number on the new s3 bucket.

## Structure

- src

    The main source code for AWS s3 & OCR using Textract

- utils

    The tool for management of the files and folders of this project
    
- app

    The main execution file
    
- config

    The configuration with AWS account information

- requirements

    All the dependencies for this project
    
- settings

    Several settings including path
    
## Installation

- Environment

    Ubuntu 18.04, Windows 10, Python 3.6
    
- Dependency Installation

    Please go ahead to this project directory and run the following command in the terminal.
    ```
        pip3 install -r requirements.txt
    ```

## Execution

- Please set all the configurations in config.cfg file with your AWS account information like access_key_id, secret_access_key,
region_name, source_s3_bucket_name, new_s3_bucket_name.

- Please run the following command in the terminal.

    ```
        python3 app.py
    ```
 