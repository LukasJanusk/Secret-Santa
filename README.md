# Secret Santa App

This is a simple Secret Santa app that randomly assigns gifts to participants and sends them an email with their assigned gift recipient.

## Setup

### 1. **Create `sender.json`**

This file stores the email and Gmail App password for the sender (the email account used to send gift notifications).

Here is an example of the `sender.json` format:

```json
{
  "email": "your_sender_email@gmail.com",
  "password": "your_gmail_app_key"
}
```

Replace "your_sender_email@gmail.com" with the email address you want to send the Secret Santa notifications from.

Replace "your_gmail_app_key" with your Gmail App password. You can generate this password via your Google account settings.

### 2. **Create `participants.json`**

This file contains an array of participants, each with a name and an email address. There must be a minimum of 3 participants.

Here is an example of the participants.json format:

```json
[
  { "name": "name1", "email": "myemail1@gmail.com" },
  { "name": "name2", "email": "myemail2@gmail.com" },
  { "name": "name3", "email": "myemail3@gmail.com" }
]
```

Replace name1, name2, name3 with the names of the participants.
Replace myemail1@gmail.com, myemail2@gmail.com, and myemail3@gmail.com with the participants' actual email addresses.

You can also add gift wishlist under key 'wishes' for each of participants in a format:

```json
[
  { "name": "name1",
    "email": "myemail1@gmail.com",
    "wishes": [
      {
      "gift": "gift-example1",
      "url": "www.example-link1.com"
      },
        {
      "gift": "gift-example2",
      "url": "www.example-link2.com"
      },
]}
]
```  
## Run

Once required files created you can run the program:

```python
python main.py
```
