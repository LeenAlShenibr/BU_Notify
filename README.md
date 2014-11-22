BU_Notify
========

An application that Notifies user of an available seat in some specific class.

It uses your gmail and password (doesn't store it), to send you an email and a text message when the course becomes available.

Features
--------

- Checks every 60 seconds for courser availability.
  (Can be changed.)
  Look for ```t = threading.Timer(60, runUntilFound)```
  and change the 60 to the frequency you want in seconds.

- Sends Email and SMS notifications.

Installation
------------

1. The project requires python, which is installed by default in OSX. Windows users must install python version 2.7 .

2. The project requires that you have ```pip``` installed, if you don't, follow the instruction [over here to install it](https://pip.pypa.io/en/latest/installing.html).

3. ```pip install -r requirements.txt```

  If it fails, you may need  upgraded privileges,
so either use ```sudo``` or run the project in ```virtualenv```


Use
---

You can run the script with parameters in the following format:

```bash
python courseNotifier.py  semester year college department class section phoneNumber email
```

*or*

```python courseNotifier.py``` and respond to the prompts.

**Note:** In both cases you will be prompted for a password.


**Example:**

```bash
python courseNotifier.py spring 2014 cas cs 235 a1 phoneNumber leenshe@bu.edu
```

Known Limitations
=================

Notifactions only work with google based email accounts [@gmail, @bu.edu], and phone numbers in that AT&T network.

TODO
----

* Support more types email.
* Support more cell providers.
* Make it more user friendly.
* GUI? Or, simple web app?
* Allow adding multiple courses.

Support
-------

Email leenshe[at]bu.edu or tmtaybah[at]bu.edu   with any problems, questions, or comments.

Keep in mind that this is incomplete and is provided as is, if you want to help with this project, please contact us.

License
-------

The project is licensed under the [MIT License](LICENSE.txt).
