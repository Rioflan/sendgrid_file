## How to run it ?

Go to https://sendgrid.com to setup an account

```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ echo "export SENDGRID_API_KEY='YOUR_API_KEY'" >sendgrid.env
$ source ./sendgrid.env
$ python script.py <filename>
```
