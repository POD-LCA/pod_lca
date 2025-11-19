import base64
import os


def save_key(key, filename):
    encoded_key = base64.b64encode(key).decode("utf-8")

    with open(filename, "w") as file:
        file.write(encoded_key)


folder = os.path.dirname(os.path.abspath(__file__))
binary_key = b"podlcamatmaster"
save_key(binary_key, folder + "\key.txt")
