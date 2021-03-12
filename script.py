from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import argparse
import base64
import os
import subprocess
import sys
import tempfile

def get_file_attachment(path, args):
    with open(path, 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    return Attachment(
        FileContent(encoded_file),
        FileName(os.path.basename(path)),
        FileType(args.type),
        Disposition('attachment')
    )


def send_file(path, args):
    message = Mail(
        from_email=args.sender,
        to_emails=args.target,
        subject=os.path.basename(path),
        html_content='_')
    message.attachment = get_file_attachment(path, args)

    return sg.send(message)


## Main ##

parser = argparse.ArgumentParser(description='Send big file by splitting it')
parser.add_argument('path', help='The path of the file to send')
parser.add_argument('sender', help='Set the sender mail (needs to be same as config on sendgrid)')
parser.add_argument('target', help='Destination mail address')
parser.add_argument('-s', '--size', help='Max size of each file', default='19M')
parser.add_argument('-t', '--type', help='Default type (mime) of sent attachment', default='application/zip')
args = parser.parse_args()

if not os.path.isfile(args.path):
    print ("File not exist")
    exit(1)

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
temp_dir = tempfile.TemporaryDirectory()
zip_to_create = os.path.join(temp_dir.name, os.path.basename(args.path) + '.zip')

cp = subprocess.run(["zip","-s", args.size, zip_to_create, args.path])

for filename in os.listdir(temp_dir.name):
    file_to_send=os.path.join(temp_dir.name, filename)
    try:
        send_file(file_to_send, args)
        print(f"{filename} sent")
    except Exception as e:
        print(e)

temp_dir.cleanup()
