import participants as p


def main():
    all_participants = p.Participant.load_participants()
    p.Participant.select_gift_to(all_participants)
    for participant in all_participants:
        participant.send_email()


if __name__ == "__main__":
    main()
