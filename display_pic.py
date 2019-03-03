
from PIL import Image
from io import BytesIO
import base64, binascii

bytes_pic = str.encode('/home/mason/websiteC/0to100/avatars//home/mason/websiteC/0to100/avatars')

im = Image.open(BytesIO(base64.b64decode(bytes_pic)))

im.show()
