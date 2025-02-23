from weddingwrangle.models import Guest
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from qr_code.qrcode.maker import QRCodeOptions, make_qr_code_image
from django.urls import  reverse

LINE_SPACING = 80
PARAGRAPH_SPACING = 160
# Image size: to A5 - bleed margins of 6 pixels in each direction * 300ppi
WIDTH = 1748
HEIGHT = 2480
X_CENTRE = WIDTH // 2
FONT = ImageFont.truetype("weddingwrangle/static/fonts/CharisSILR.ttf", 50)

def print_and_move_cursor(
    image_object: ImageDraw.Draw,
    current_y_position: float, 
    text: str, 
    paragraph_drop: bool
):
    image_object.text(
        (X_CENTRE, current_y_position),
        text,
        font=FONT,
        fill=(40, 123, 121),
        anchor="mm",
    )

    if paragraph_drop:
        current_y_position += PARAGRAPH_SPACING
    else:
        current_y_position += LINE_SPACING

    return image_object, current_y_position


def generate_invite(image_object, invitee: dict):

    text_lines = [
        f"{invitee['name']}, we would be delighted",
        "if you could join us at our wedding.",
        "Please arrive for 1.30pm at",
        "Childerley Hall, Cambridge",
        "Visit wedding.beccy.willthong.com",
        f"rsvp/{invitee['rsvp_link']} or scan the code",
        "overleaf to RSVP & for more",
        "information.",
        "Carriages at midnight."
    ]

    current_y_position = HEIGHT * 0.5

    for index, text_line in enumerate(
        text_lines
    ):
        paragraph_drop = index in [1, 3, 7]
        image_object, current_y_position = print_and_move_cursor(
            image_object, current_y_position, text_line, paragraph_drop
        )

    return 

def generate_qr_image(rsvp_link, current_site, protocol):
    qr_options = QRCodeOptions(image_format="png", size="s", dark_color=(40,123,121))
    path = reverse("rsvp", args=[rsvp_link])
    rsvp_url = f"{protocol}://{current_site}{path}"
    qr_image = Image.open(BytesIO(make_qr_code_image(rsvp_url, qr_options)))
    qr_width, qr_height = qr_image.size
    blank_page = Image.new('RGB', (WIDTH, HEIGHT), "white")
    x_position = (WIDTH - qr_width) // 2
    y_position = (WIDTH - qr_height) // 2
    blank_page.paste(qr_image, (x_position, y_position))
    return blank_page

def generate_invites(invite_template, current_site, protocol):

    guests = Guest.objects.all()
    invite_data, partners_done = [], set()
    for guest in guests:
        if guest in partners_done:
            continue
        this_guest = {}
        this_guest["name"] = guest.first_name
        if guest.partner:
            this_guest["name"] += " & " + guest.partner.first_name
            partners_done.add(guest.partner)
        this_guest["rsvp_link"] = guest.rsvp_link
        invite_data.append(this_guest)

    for index, invitee in enumerate(invite_data):

        base_image = invite_template.resize((WIDTH, HEIGHT)).copy()
        image_object = ImageDraw.Draw(base_image)
        generate_invite(image_object, invitee)
        if index == 0:
            base_image.save("generated_invites.pdf")
        else:
            base_image.save("generated_invites.pdf", append=True)

        qr_page = generate_qr_image(invitee["rsvp_link"], current_site, protocol)
        qr_page.save("generated_invites.pdf", append=True)

        print(f"Printed invite to {invitee['name']}")

    return
