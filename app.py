import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import qrcode


def create_rounded_rectangle(width, height, radius, fill):
    rectangle = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(rectangle)

    draw.rectangle(
        [(radius, 0), (width - radius, height)],
        fill=fill
    )
    draw.rectangle(
        [(0, radius), (width, height - radius)],
        fill=fill
    )

    draw.pieslice([(0, 0), (radius * 2, radius * 2)], 180, 270, fill=fill)
    draw.pieslice([(width - radius * 2, 0), (width, radius * 2)], 270, 360, fill=fill)
    draw.pieslice([(0, height - radius * 2), (radius * 2, height)], 90, 180, fill=fill)
    draw.pieslice([(width - radius * 2, height - radius * 2), (width, height)], 0, 90, fill=fill)

    return rectangle


def create_image(text_lines):
    width, height = 1058, 500
    background_color = (255, 255, 255, 255)  # White with full opacity
    text_color = (0, 0, 0, 255)  # Black
    corner_radius = 20

    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    rounded_rect = create_rounded_rectangle(width, height, corner_radius, background_color)
    img.paste(rounded_rect, (0, 0), rounded_rect)

    draw = ImageDraw.Draw(img)

    font_path = "Poppins-Regular.ttf"
    font_size = 50

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        st.error(f"Could not load font {font_path}. Using default font.")
        font = ImageFont.load_default()

    line_height = int(font.getbbox("Ay")[3] * 1.5)

    total_text_height = line_height * len(text_lines)

    start_y = (height - total_text_height) / 2

    for i, line in enumerate(text_lines):
        wrapped_text = textwrap.fill(line, width=40)

        text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (width - text_width) / 2
        text_y = start_y + i * line_height

        draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill=text_color, align='center')

    return img


def create_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data_text = ''
    for i in data:
        data_text += (i + '\n')

    qr.add_data(data_text)
    qr.make(fit=True)

    img_qr = qr.make_image(fill='black', back_color='white')
    return img_qr


st.set_page_config(
    page_title="Shipping Label Maker",
    page_icon="✉️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("✉️ Shipping Label Maker")

# User input for the three lines of text
line1 = st.text_input("Name", value="")
line2 = st.text_input("Address - line 1", value="")
line3 = st.text_input("Address - line 2", value="")

confirm_checkbox = st.checkbox("Generate a QR code for this label ✅")


if st.button("Generate Label"):
    text_lines = [line1, line2, line3]
    img = create_image(text_lines)
    qr_image = create_qr_code(text_lines)
    qr_image_crop = qr_image.crop()

    file_name = f"{line1.replace(' ', '_')}.png"
    file_name_qr = f"{line1.replace(' ', '_')}_qr.png"
    

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    qr_byte_arr = io.BytesIO()
    qr_image_crop.save(qr_byte_arr, format='PNG')
    qr_byte_arr = qr_byte_arr.getvalue()

    if confirm_checkbox:
        st.image(img, caption="Generated Label", use_column_width=True)

        st.download_button(label="Download Label",
                        data=img_byte_arr,
                        file_name=file_name,
                        mime="image/png")
        
        st.image(qr_image_crop, caption="Generated qr code", use_column_width=True)

        st.download_button(label="Download qr code",
                        data=qr_byte_arr,
                        file_name=file_name_qr,
                        mime="image/png")
    else:
        st.image(img, caption="Generated Label", use_column_width=True)

        st.download_button(label="Download Label",
                        data=img_byte_arr,
                        file_name=file_name,
                        mime="image/png")
