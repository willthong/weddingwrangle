from weddingwrangle.models import (
    Title,
    Position,
    RSVPStatus,
    Dietary,
    Guest,
    Audience,
)
from PIL import Image, ImageDraw, ImageFont


def generate_invites(invite_template):

    # Set image size to A5 - bleed margins of 6 pixels in each direction * 300ppi
    width, height = 1677, 2409
    invite_template.resize((width, height))
    image_object = ImageDraw.Draw(invite_template)

    font = ImageFont.truetype("weddingwrangle/static/fonts/CharisSILR.ttf", 180)

    text_lines = [
        "Guest, we would be delighted",
        "if you could join us at our wedding.",
        "Please arrive for 1.30pm at\nChilderley Hall, Cambridge",
        """
            Visit wedding.beccy.willthong.com/\n
            rsvp/yapksixQxN or scan the code\n
            overleaf to RSVP & for more\n
            information.
        """,
        "Carriages at midnight.",
    ]

    image_object.text(
        (width * 1.8, height * 2),
        text_lines[0],
        font=font,
        fill=(40, 123, 121),
        anchor="mm",
    )

    image_object.text(
        (width * 1.8, height * 2.2),
        text_lines[1],
        font=font,
        fill=(40, 123, 121),
        anchor="mm",
    )

    invite_template.save("temp.png")

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
