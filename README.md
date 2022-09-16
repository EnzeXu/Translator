Enze's Translator
===========================
This document is used to show the detailed description of Enze's Translator project.

See `https://github.com/EnzeXu/Translator` or
```shell
$ git clone https://github.com/EnzeXu/Translator.git
```

Set virtual environment and install packages:
```shell
$ python -m venv ./venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Install package `words` in advance:
```shell
(venv) $ python -m nltk.downloader words -d venv/nltk_data 
```

Edit file `baidu_account_example.py` and then rename it as `baidu_account.py` in advance:
```shell
(venv) $ vi baidu_account_example.py
(venv) $ mv baidu_account_example.py baidu_account.py
```

Run
```shell
(venv) $ python run.py -p ${PDF_FILE_PATH}
(venv) $ mv baidu_account_example.py baidu_account.py
```

Exit virtual environment
```shell
(venv) $ deactivate
$ 
```
