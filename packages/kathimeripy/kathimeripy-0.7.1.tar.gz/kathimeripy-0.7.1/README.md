# Kathimeripy

Use your [Kathimerini](https://www.kathimerini.gr/), [GMail](https://mail.google.com/) and [Kindle Email](https://www.amazon.com/hz/mycd/digital-console/alldevices)

## Installation

`pip install kathimeripy`

## Setup

First run the following to set up the application
```sh
python -m kathimeripy configure \
    --kathimerini-user YOUR_LOGIN_EMAIL@SERVER.com \
    --kathimerini-pass YOUR_PASS \
    --gmail-user GMAIL_ACCOUT@gmail.com \
    --gmail-pass GMAIL_APPLICATION_PASSWORD  \
    --kindle-email KINDLE_EMAIL@kindle.com
```
### Manual configuration

You can also configure the application by editing the configuration file located at `$HOME/.config/kathimeripy/config.json`.

The configuration file is in JSON format and should contain the following keys:

- `kathimerini-user`: Your Kathimerini login email.
- `kathimerini-pass`: Your Kathimerini password.
- `gmail-user`: Your Gmail account email.
- `gmail-pass`: Your Gmail application password.
- `kindle-email`: Your Kindle email address.
- `news-categories`: A list of news categories to be fetched. See below a list of accepted categories.

## Usage

To fetch and send the news to your Kindle, simply run: `python -m kathimeripy run`
Or, you can also use the `python -m kathimeripy schedule` command to run it daily through crontab. By default this is run at 08:00 every day.


Optionaly you can alse set news categories you're interested in like so:

```python -m kathimeripy news-categories "Επιστημη"  "Ελληνικη Οικονομια"  "Διεθνης Οικονομια" ```

Valid categories are the following:

* HARVARD

* Αθλητισμος

* Αμυνα

* Αποψεις

* Αστυνομικο

* Ατζεντα

* Βιβλιο

* Γαστρονομος

* Γραφηματα

* Διεθνης Οικονομια

* Δικαστικο

* Εκπαιδευση

* Ελληνικη Οικονομια

* Εξωτερικη Πολιτικη

* Επιστημη

* Επιχειρησεις

* Ιστορια

* Κοινωνια

* Κοσμος

* Κυβερνηση

* Με την «Κ»

* Οικονομια

* Περιοδικο «Κ»

* Πολιτικη

* Πολιτισμος

* Στηλες

* Ταξιδια

* Υγεια
