import requests
from time import sleep
from os import listdir, rename, path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def gen_usd_to_brl_number(bill_type='USD-BRL'):
    link = f'https://economia.awesomeapi.com.br/last/{bill_type}'

    dol_res = requests.get(link)
    dol_json = dol_res.json()

    high_value = dol_json['USDBRL']['high']

    return float(high_value)


def rename_img(img, img_path):
    d = path.getctime(f'{img_path}/{img}')

    rename(f'{img_path}/{img}', f'{img_path}/{d}.png')
    sleep(2)


def add_text_to_image(text='texto'):
    image_path = './imagens'

    [rename_img(img, image_path) for img in listdir(image_path)]
    images = listdir(image_path)

    print('\nImagens listadas e renomeadas..')

    last_img_path = images[-1]

    img = Image.open(f'{image_path}/{last_img_path}')
    if img.height < 700:
        size = (1000, 700); img = img.resize(size)

    x = img.width // 2
    y = img.height // 2

    print('Última imagem selecionada e redimensionada..')

    # Fonte Definida
    f = ImageFont.truetype('Roboto-Bold.ttf', 90)

    # Colocando blur atrás do texto
    blurred = Image.new('RGBA', img.size)
    draw = ImageDraw.Draw(blurred)
    draw.text((x, y + 270), text=text, fill='black', font=f, anchor='mm')
    blurred = blurred.filter(ImageFilter.BoxBlur(7))
    img.paste(blurred, blurred)

    # Colocando o texto
    draw = ImageDraw.Draw(img)
    draw.text((x, y + 270), text=text, fill='white', font=f, anchor='mm')

    print('Texto desenhado..\n')

    return img.show()


actual_bill = gen_usd_to_brl_number()
fifty_cent = str(round(actual_bill / 2, 2))

add_text_to_image(text=f'R$ {fifty_cent}')
