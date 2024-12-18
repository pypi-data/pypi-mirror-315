import os
import re
import base64
import os.path
import requests


def extract_version(file_name: str) -> str:
    version_pattern = r'version="(\d+\.\d+\.\d+)"'
    version = None

    with open(file_name, "r") as file:
        file_contents = file.read()
        match = re.search(version_pattern, file_contents)
        if match:
            version = match.group(1)

    return version


def hello_world_html():
    fname = 'hello_world.py'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fpath = os.path.join(current_dir)
    with open(f"{fpath}/{fname}", 'r') as f:
        code_lines = f.readlines()

    html_lines = [
        '<div style="font-size:1.1em;padding:15px;background-color:#fdffc7; display: block;line-height:1.2em !important;"><pre><code style="white-space: pre-wrap;">']
    for line in code_lines:
        line = line.replace('import sys', '')
        line = line.replace('import os', '')
        line = line.replace("sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))", "")
        line = line.replace('import main as ws', 'import webslides as ws')
        html_line = line.rstrip().replace('<', '&lt;').replace('>', '&gt;')
        html_lines.append(html_line)
    html_lines.append('</code></pre></div>')

    # add copy button
    html_lines.append(
        """<br><br><button style="font-size: 1.3em; background-color: #00bb00;color: white;border-color: #c7c7c7 !important; border-radius: 6px;" onclick="navigator.clipboard.writeText(`""" + '\n'.join(
            html_lines[1:-1]) + """`);alert('Code copied to clipboard');"><b>COPY CODE</b></button>""")

    return '\n'.join(html_lines)


def code_to_html(code):
    return f'<div style="background-color:#fdffc7; display: block;font-size:1.1em;padding:15px;"><pre><code>{code}</code></pre></div>'


def retrieve_image_src(url, embed_images):
    """
    param url: str filepath or web url
    return: str with src data to embed in html page
    """


    # don't embed images
    if not embed_images and url is not None and 'http' in url:

        # test if provided url is valid
        # Download the image using requests
        response = requests.get(url)
        if response.status_code == 200:  # Check if the download was successful
            return url
        else:
            print(f'Image {url} not found, using default')
            return None

    # embed images
    else:

        # default image
        IMAGE_SRC = None

        # check if image is provided, otherwise swap for Webslides logo HTML
        if url and len(url) > 0:

            if 'http' in url:

                # Download the image using requests
                response = requests.get(url)
                if response.status_code == 200:  # Check if the download was successful
                    # Convert the image to Base64
                    base64_string = base64.b64encode(response.content).decode('utf-8')
                    # Create the data:image string
                    IMAGE_SRC = f"data:image/jpeg;base64,{base64_string}"
                else:
                    print(f"WARNING: Error while fetching the image {url}: {response.status_code}, using default")

            # check if local image file exists
            elif os.path.exists(url):

                # Open het bestand in binaire modus
                with open(url, 'rb') as file:
                    file_content = file.read()

                # Encodeer de inhoud naar Base64
                base64_string = base64.b64encode(file_content).decode('utf-8')

                # Create the data:image string
                IMAGE_SRC = f"data:image/jpeg;base64,{base64_string}"

            # image not found, using default
            else:
                print(f"WARNING: image {url} not found, using default")

        # no image url provided, load default webslides logo
        else:
            print(f'INFO: image {url} not found, using default')

        return IMAGE_SRC
