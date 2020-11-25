import boto3
import configparser
import os
import numpy as np
import cv2

from pdf2image import convert_from_path
from src.invoice_no.extractor import InvoiceExtractor
from settings import PDF_IMAGES_DIR, CONFIG_FILE, PDF_RET


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
                if PDF_RET:
                    invoice_no = self.invoice_extractor.extract_invoice_no_pdf(pdf_name=filename,
                                                                               s3_bucket_name=self.source_bucket)
                else:
                    file_path = os.path.join(PDF_IMAGES_DIR, filename)
                    frame_path = os.path.join(PDF_IMAGES_DIR, f"{filename.replace('.pdf', '')}.jpg")
                    print(f"[INFO] {filename} downloading...")
                    self.s3.download_file(self.source_bucket, obj["Key"], file_path)
                    pdf_images = [np.array(page) for page in convert_from_path(file_path, 200)]

                    cv2.imwrite(frame_path, cv2.cvtColor(pdf_images[0], cv2.COLOR_BGR2RGB))
                    invoice_no = self.invoice_extractor.extract_invoice_no_frame(image_path=frame_path)
                copy_source = {'Bucket': self.source_bucket, 'Key': filename}
                self.s3.copy(copy_source, self.new_bucket, f"{invoice_no}.pdf")
                self.s3.delete_object(Bucket=self.source_bucket, Key=filename)
                print(f"[INFO] Copied to {self.new_bucket}/{invoice_no}.pdf")

        return


if __name__ == '__main__':
    AWSManager().main()
