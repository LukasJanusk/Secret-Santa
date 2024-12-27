from participants import Participant


def main():
    all_participants = Participant.load_participants()
    Participant.select_gift_to(all_participants)
    Participant.send_emails(all_participants)


if __name__ == "__main__":
    main()
