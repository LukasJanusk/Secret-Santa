from participants import Participant


def main():
    all_participants = Participant.load_participants()
    Participant.select_gift_to(all_participants)
    for participant in all_participants:
        participant.send_email()


if __name__ == "__main__":
    main()
