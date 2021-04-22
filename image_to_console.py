"""
Drawing image with ASCII characters
Image will be downloaded from the AI based webbsite,
'https://thispersondoesnotexist.com/'
"""
import requests
import os
from PIL import Image
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

def is_valid(url):
    """Checks if 'url' is a valid URL"""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    """function reutns the URL to all images on 'url'"""
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue

        img_url = urljoin(url, img_url)

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        
        if is_valid(img_url):
            urls.append(img_url)
        else:
            print("Error: url not valid")     
    return urls

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    file_name = os.path.join(pathname, url.split("/")[-1])
    progress = tqdm(response.iter_content(1024), f"Downloading {file_name}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(file_name + ".jpg", "wb") as f:
        for data in progress:
            f.write(data)
            progress.update(len(data))
    return file_name + ".jpg"
    
def load_image(file):
    """loading image"""
    try:
        return Image.open(file)
    except FileNotFoundError:
        print(f"Error: No image named '{file}' was found")
        return None

def resize_img(image, new_width):
    """function will resize image and making it a square"""
    img_width, img_height = image.size
    new_height = new_width * img_height / img_width
    return image.resize((new_width, int(new_height)))

def greyscale_img(image):
    """function will make image black and white"""
    return image.convert("L")

def pixel_to_ascii(image):
    """Converting pixel to ASCII character, pixel by pixel"""
    ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//25]
    return ascii_str
    
def image_to_file(image, file_name, image_size = 500):
    image = resize_img(image, image_size)

    image_width = image.width

    image = greyscale_img(image)

    image = pixel_to_ascii(image)

    ascii_image = ''
    
    for i in range(0, len(image), image_width):
        print(image[i:i+image_width])
        ascii_image += image[i:i+image_width] + '\n'

    with open(file_name, 'w') as f:
        f.write(ascii_image)

def main():
    """function connecting all other functions"""
    print('This program will convert image to ASCII characters')
    print('---------------------------------------------------')
    print('1. Enter image manualy')
    print('2. All images from website')
    print('3. Image from "thispersondowsnotexist.com"')
    print('0. Exit')
    
    stop = False

    try:
        choise = int(input('Choise: '))
    except ValueError:
        print("Input must be a integer")

    while not stop:
        if choise == 0:
            stop = True
        elif choise == 1:
            image_name = input('Enter image name: ')
            image = load_image(image_name)
            image_to_file(image)
            stop = True
        elif choise == 2:
            url = input('Enter URL: ')
            image_urls = get_all_images(url)
            for index, img in enumerate(image_urls):
                    file_name = download(img, r'C:\Python_Projects\Website')
                    image = load_image(file_name)
                    image_to_file(image, 'image'+str(index)+'.txt')
            stop = True
        elif choise == 3:
            image_url = get_all_images('https://thispersondoesnotexist.com/')[0]   
            file_name = download(image_url, r'C:\Python_Projects\Website')
            image = load_image(file_name)
            text_file_name = file_name[:-4] + ".txt"
            image_to_file(image, text_file_name, 100)
            stop = True
        else:
            print("Error: Number to high")

main()