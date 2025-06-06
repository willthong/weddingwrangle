from weddingwrangle.models import Guest
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from qr_code.qrcode.maker import QRCodeOptions, make_qr_code_image
from django.urls import  reverse

LINE_SPACING = 70
PARAGRAPH_SPACING = 160
# Image size: to A5 * 300ppi
CONTENT_WIDTH = 1748
CONTENT_HEIGHT = 2480
# Margin: 3mm bleed * 300ppi
MARGIN = 35
WIDTH = CONTENT_WIDTH + (MARGIN * 2)
HEIGHT = CONTENT_HEIGHT + (MARGIN * 2)
X_CENTRE = WIDTH // 2
TITLE_FONT = ImageFont.truetype("weddingwrangle/static/fonts/felixtitlingmt.ttf", 80)
BODY_FONT = ImageFont.truetype("weddingwrangle/static/fonts/CharisSILR.ttf", 43)
TURQUOISE=(117, 0, 5, 133)
TURQUOISE_PNG=(67, 123, 121)

FAMILY_ALIAS = {
    "Elsa": "Poh Poh",
    "Sehu": "Ma Ma", 
    "Jean": "Grandma",
    "William": "Uncle William",
}

def print_and_move_cursor(
    image_object: ImageDraw.Draw,
    current_y_position: float, 
    text: str, 
    drop_distance: int,
    selected_font
):
    image_object.text(
        (X_CENTRE, current_y_position),
        text,
        font=selected_font,
        fill=TURQUOISE,
        anchor="mm",
    )

    current_y_position += drop_distance

    return image_object, current_y_position


def add_title_text(image_object: ImageDraw.Draw):
    current_y_position = HEIGHT * 0.28
    image_object, current_y_position = print_and_move_cursor(
        image_object, current_y_position, "Beccy & Will", 160, TITLE_FONT
    )
    image_object, current_y_position = print_and_move_cursor(
        image_object, current_y_position, "Are Getting Married", 190, TITLE_FONT
    )
    image_object, current_y_position = print_and_move_cursor(
        image_object, current_y_position, "5th July 2025", 0, TITLE_FONT
    )
    return

def add_date_lines(image_object: ImageDraw.Draw):
    mid_point = WIDTH / 2
    line_width = 510
    line_1_y = 987
    line_2_y = 1137
    image_object.line(
        (mid_point - line_width / 2, line_1_y, mid_point + line_width / 2, line_1_y), 
        fill=TURQUOISE, 
        width=2
    )
    image_object.line(
        (mid_point - line_width / 2, line_2_y, mid_point + line_width / 2, line_2_y), 
        fill=TURQUOISE, 
        width=2
    )
    return

def generate_invite(image_object: ImageDraw.Draw, invitee: dict):

    text_lines = [
        f"{invitee['name']}, we would be delighted",
        "if you could join us at our wedding.",
        "Please arrive for 1.30pm at",
        "Childerley Hall, Cambridge.",
        "Visit wedding.beccy.willthong.com",
        f"rsvp/{invitee['rsvp_link']} or scan the code",
        "overleaf to RSVP & for more",
        "information.",
        "Carriages at midnight."
    ]

    current_y_position = HEIGHT * 0.51

    for index, text_line in enumerate(text_lines):
        if index in [1, 3, 7]:
            drop_distance = PARAGRAPH_SPACING
        else:
            drop_distance = LINE_SPACING
        image_object, current_y_position = print_and_move_cursor(
            image_object, current_y_position, text_line, drop_distance, BODY_FONT
        )

    return 

def generate_qr_image(rsvp_link, current_site, protocol):
    qr_options = QRCodeOptions(image_format="png", size="s", dark_color=TURQUOISE_PNG)
    path = reverse("rsvp", args=[rsvp_link])
    rsvp_url = f"{protocol}://{current_site}{path}"
    qr_image = Image.open(BytesIO(make_qr_code_image(rsvp_url, qr_options)))
    qr_image = qr_image.convert("CMYK")
    qr_width, qr_height = qr_image.size
    page = Image.new('CMYK', (WIDTH, HEIGHT), (0,0,0,0))
    x_position = (WIDTH - qr_width) // 2
    y_position = (WIDTH - qr_height) // 2
    page.paste(qr_image, (x_position, y_position))
    return page


def convert_to_cmyk(image):
    if image.mode != 'CMYK':
        return image.convert('CMYK')
    return image

def generate_invites(invite_template, current_site, protocol):
    invite_template = Image.open(invite_template)
    invite_template = convert_to_cmyk(invite_template)
    resized_template = invite_template.resize((CONTENT_WIDTH, CONTENT_HEIGHT)).copy()

    guests = Guest.objects.all()
    invite_data, partners_done = [], set()
    for guest in guests:
        if guest in partners_done or guest.position.name in ["Bride", "Groom"]:
            continue
        this_guest = {}
        if guest.first_name in FAMILY_ALIAS.keys():
            this_guest["name"] = FAMILY_ALIAS.get(guest.first_name)
        else:
            this_guest["name"] = guest.first_name
        if guest.partner:
            this_guest["name"] += " & " + guest.partner.first_name
            partners_done.add(guest.partner)
        this_guest["rsvp_link"] = guest.rsvp_link
        invite_data.append(this_guest)

    for index, invitee in enumerate(invite_data):
        base_image = Image.new("CMYK", (WIDTH, HEIGHT), (0, 0, 0, 0))
        base_image.paste(resized_template, (MARGIN, MARGIN))
        image_object = ImageDraw.Draw(base_image)
        add_date_lines(image_object)
        add_title_text(image_object)
        generate_invite(image_object, invitee)
        if index == 0:
            base_image.save("generated_invites.pdf")
        else:
            base_image.save("generated_invites.pdf", append=True)

        qr_page = generate_qr_image(invitee["rsvp_link"], current_site, protocol)
        qr_page.save("generated_invites.pdf", append=True)
    return
