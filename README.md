# Internationalization Testing (i18n)
Library for Robot Framework automated web testing which support internationalization.

Introduction
--------------
In the past, the test object of one acceptance test script based on Robot Framework was often limited to web page in one language. However, nowadays a web page may have multiple language versions for people live in different countries. Therefore, tester often need to write more repetitive test scripts, and the cost of testing will also increase.

So this library can allow a same test script run on different languages' websites.

By the way, this is the 2nd version of i18n. See [my repository](https://github.com/Rexmen/i18n).

If you want see the 1st version,please go to [ChuGP's repository](https://github.com/ChuGP/i18n).

Installation
--------------
* With pip

    pip install RF-i18n-tool

See more detail on [RF-i18n-tool of PYPI](https://pypi.org/project/RF-i18n-tool/).

How to use
--------------
* Set Additional Robot Framework arguments: (RED->Window->Preferences->Default Launch Configurations)

If you want to use the i18n default JSON language files:

    -d out -L debug --listener %YOUR_PYTHON_PATH%/Lib/site-packages/i18n/listeners/I18nListener.py:YOUR_LOCALE:i18njson

Else if you want to use your own JSON language files:

    -d out -L debug --listener %YOUR_PYTHON_PATH%/Lib/site-packages/i18n/listeners/I18nListener.py:YOUR_LOCALE

* note:

Your language files should follow the structure:

YOUR_PROJECT_DIR/languageFiles/YOUR_LOCALE(ex:zh-TW)/xxxYOUR_LOCALE.json