import boto3
import configparser
import os

from src.invoice_no.extractor import InvoiceExtractor
from settings import CONFIG_FILE


class AWSManager:
    def __init__(self):
        params = configparser.ConfigParser()
        params.read(CONFIG_FILE)
        self.s3 = boto3.client('s3', aws_access_key_id=params.get("DEFAULT", "access_key_id"),
                               aws_secret_access_key=params.get("DEFAULT", "secret_access_key"))
        self.source_bucket = params.get("DEFAULT", "source_s3_bucket_name")
        self.new_bucket = params.get("DEFAULT", "new_s3_bucket_name")
        self.invoice_extractor = InvoiceExtractor()

    def main(self):
        object_listing = self.s3.list_objects_v2(Bucket=self.source_bucket)

        for obj in object_listing['Contents']:
            path, filename = os.path.split(obj["Key"])
            if "pdf" in filename:
                invoice_no = self.invoice_extractor.extract_invoice_no(pdf_name=filename,
                                                                       s3_bucket_name=self.source_bucket)
                copy_source = {'Bucket': self.source_bucket, 'Key': filename}
                self.s3.copy(copy_source, self.new_bucket, f"{invoice_no}.pdf")
                self.s3.delete_object(Bucket=self.source_bucket, Key=filename)
                print(f"[INFO] Copied to {self.new_bucket}/{invoice_no}.pdf")

        return


if __name__ == '__main__':
    AWSManager().main()
