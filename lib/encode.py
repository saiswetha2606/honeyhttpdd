import gzip
import zlib
import base64

def encode_gzip(data):
    """
    Compress data using Gzip encoding.
    """
    data = bytes(data, 'utf-8')  # Ensure data is in bytes
    return gzip.compress(data)

def encode_deflate(data):
    """
    Compress data using Deflate (zlib) encoding.
    """
    data = bytes(data, 'utf-8')  # Ensure data is in bytes
    return zlib.compress(data)

def encode_plain(data):
    """
    Return plain data as bytes.
    """
    return data.encode('utf-8')  # Convert string to bytes

def decode_base64(data):
    """
    Decode data from Base64 format.
    """
    data_bytes = data.encode("utf-8")  # Convert to bytes
    decoded_bytes = base64.b64decode(data_bytes)  # Decode Base64
    return decoded_bytes.decode("utf-8")  # Convert bytes back to string

def decode_plain(data):
    """
    Return plain data as string.
    """
    return data.decode('utf-8')  # Convert bytes to string
