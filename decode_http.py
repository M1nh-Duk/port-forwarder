from gzip import GzipFile
from io import BytesIO 

def httpDecodeContent(http_content): # parameter: string
    try:
        # Split the HTTP response and extract the body
        header, body = http_content.split('\r\n\r\n')

        # Convert the body to bytes
        body_bytes = bytes(body, 'latin1')  # latin1 encoding is used for binary

        # Use GzipFile to decode the content
        decoded_body = GzipFile(fileobj=BytesIO(body_bytes)).read()
        decoded_body = decoded_body.decode("latin1")
        response = header + decoded_body
        
        return response
    
    except Exception as e: 
        print(e)
        return http_content

def isHTTP(data): # parameter: str
    if data.startswith("HTTP"):
            return True
    return False

# def isHTTP(data): # parameter: byte
#     try:
#         data = data.decode()
#         if data.startswith("HTTP"):
#             return True
#         return False
#     except:
#             try:
#                 data = data.decode("latin1")
#                 if data.startswith("HTTP"):
#                     return True
#             except:
#                 return False
    