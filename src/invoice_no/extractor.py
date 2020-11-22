import boto3
import configparser

from settings import CONFIG_FILE


class InvoiceExtractor:
    def __init__(self):
        params = configparser.ConfigParser()
        params.read(CONFIG_FILE)
        self.textract = boto3.client('textract', region_name=params.get("DEFAULT", "region_name"),
                                     aws_access_key_id=params.get("DEFAULT", "access_key_id"),
                                     aws_secret_access_key=params.get("DEFAULT", "secret_access_key"))

    def extract_invoice_no(self, image_path):
        invoice_no = ""
        with open(image_path, 'rb') as document:
            image_bytes = bytearray(document.read())

        # Call Amazon Textract
        response = self.textract.detect_document_text(Document={'Bytes': image_bytes})
        invoice_info = response["Blocks"][1:]

        # Print detected text
        for i, item in enumerate(invoice_info):
            if "Invoice" in item["Text"]:
                invoice_no = invoice_info[i + 1]["Text"]
                break

        return invoice_no


if __name__ == '__main__':
    InvoiceExtractor().extract_invoice_no(image_path="")
