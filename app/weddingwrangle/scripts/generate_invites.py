from weddingwrangle.models import (
    Title,
    Position,
    RSVPStatus,
    Dietary,
    Guest,
    Audience,
)

def generate_invites(invite_template):
    print(type(invite_template))

    # for row in reader:
    #     guest = Guest.objects.get_or_create(
    #         title=Title.objects.get(name=row[1]),
    #         first_name=row[2],
    #         surname=row[3],
    #         email_address=row[4],
    #         position=Position.objects.get(name=row[5]),
    #         rsvp_status=RSVPStatus.objects.get(name="Pending"),
    #     )
    #
    #     guest[0].audiences.add(
    #         Audience.objects.get(name="All potential guests (excludes Declined)")
    #     )
    #     guest[0].audiences.add(Audience.objects.get(name="All guests yet to RSVP"))
    #
    #     try:
    #         for dietary in row[9].split(","):
    #             dietary = dietary.replace("[", "").replace("]", "").replace("'", "")
    #             guest[0].dietaries.add(Dietary.objects.get(name=dietary))
    #     except Dietary.DoesNotExist:
    #         pass
    #
    #     if row[8]:
    #         partners[guest[0]] = {"First name": row[8], "Surname": row[9]}
    #
    #     guest[0].save()
    #
    # for guest, partner in partners.items():
    #     guest.partner = Guest.objects.filter(
    #         first_name=partner["First name"], surname=partner["Surname"]
    #     )[0]
    #     guest.save()
    #
    return
