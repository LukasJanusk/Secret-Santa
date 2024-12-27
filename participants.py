import json
import random
import sys
from dataclasses import dataclass
from typing import List, Dict
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os


@dataclass
class Participant:
    name: str
    email: str
    wishes: List[Dict[str, str]]
    gifts_to: str = ''

    def __post_init__(self):
        if self.wishes is None:
            self.wishes = []

    @staticmethod
    def load_participants():
        "creates array of Participant objects from participants.json"

        try:
            with open("participants.json", "r") as file:
                data = json.load(file)
                participants = [Participant(**item) for item in data]
            return participants

        except FileNotFoundError:
            print("Error: The file 'participants.json' was not found.")
        except json.JSONDecodeError:
            print("Error: The file 'participants.json' contains invalid JSON.")
        except TypeError as e:
            print(f"Error: There is a problem with the data format. {e}")
        except PermissionError:
            print("Error: Permission denied accessing 'participants.json'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def select_gift_to(participants: List["Participant"]):
        "Asings each participant with secret santa"

        if len(participants) < 3:
            print("3 or more participants needed to assign gifts to.")
            return
        random.shuffle(participants)
        for i in range(len(participants)):
            participants[i].gifts_to = (
                participants[(i - 1)].name
                )
        for participant in participants:
            if participant.name == participant.gifts_to:
                sys.exit(
                    "One or more participants gift to themselves."
                    + " Make sure there are no dublicate names")

    def parse_wishes(self):
        """
        Expects wishes to contain dictionaries where
        under 1st key is a gift, 2nd url.
        """
        wishes = "\nPageidaujamų dovanų sąrašas:\n"
        for index, wish in enumerate(self.wishes):
            keys = list(wish.keys())
            gift = wish[keys[0]]
            url = wish[keys[1]]
            message = f"\n{index + 1}. {gift}\n{url}.\n"
            wishes += message
        return wishes

    def parse_message(self):
        start = f"\nSveiki!\n\nŠiais metais Jūsų dovanos lauks - {self.gifts_to}\n"
        middle = ''
        if self.wishes:
            middle = self.parse_wishes()
        end = "\nGražių švenčių!"
        message = start + middle + end
        return message

    def send_email(self):
        "Sends email from email specified in sender.json to the participant"

        receiver = self.email
        message = self.parse_message()

        try:
            with open("sender.json", "r") as file:
                data = json.load(file)
                sender = data["email"]
                password = data["password"]

        except FileNotFoundError:
            print("Error: The file 'sender.json' was not found.")
        except json.JSONDecodeError:
            print("Error: The file 'sender.json' contains invalid JSON.")
        except TypeError as e:
            print(f"Error: There is a problem with the data format. {e}")
        except PermissionError:
            print("Error: Permission denied accessing 'sender.json'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        em = EmailMessage()
        em["From"] = sender
        em["To"] = receiver
        em["Subject"] = "TESTAS - Kalėdų senelis"
        em.set_content(message)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_app_password = password

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as client:
                client.starttls()
                client.login(sender, smtp_app_password)
                client.send_message(em)
                print(f"Email sent to {self.name}")

        except KeyError as e:
            sys.exit(f"Key Error occured sending to {self.name}: {e}")
        except smtplib.SMTPAuthenticationError as e:
            sys.exit(f"Authentication error sending to {self.name}: {e}")
        except smtplib.SMTPServerDisconnected as e:
            sys.exit(f"Server disconnected sending to {self.name}: {e}")
        except smtplib.SMTPException as e:
            sys.exit(f"SMTP error occurred sending to {self.name}: {e}")
        except Exception as e:
            sys.exit(f"Error occurred sending email to {self.name}: {e}")

    @staticmethod
    def send_emails(participants: List["Participant"]):
        for participant in participants:
            participant.send_email()
        log_message = ''
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = os.path.join(logs_dir, f"{current_time}.txt")
        for index, participant in enumerate(participants):
            message = (
                f"{index + 1}. {participant.name} dovaną dovanoja: "
                + f"{participant.gifts_to}.\n")
            log_message += message
        with open(file_path, "w") as file:
            file.write(log_message + "\n")
            print(f"{current_time}.txt saved")
