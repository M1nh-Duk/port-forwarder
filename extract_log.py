import decode_http
import codecs
import sys

if len(sys.argv) < 3:
    print("Usage: python extract_log.py <LOGFILE> <ID> <DECODE(True/False)> ")
    sys.exit(1)

log_file_path = sys.argv[1] # "HTTP_access.log" 
request_id = sys.argv[2]  #"1699092421.783685" 
decode = True if len(sys.argv) == 4  else False

request = []
response = []
request_found = False
response_found = False

def convert_byte_string_to_bytes(byte_str):
    # Remove the leading 'b' and single quotes
    byte_str = byte_str[2:-1]

    # Replace escaped characters with their actual representations
    byte_str = codecs.decode(byte_str, 'unicode_escape')

    # Convert the string to bytes using utf-8 encoding
    byte_obj = byte_str.encode('utf-8')

    return byte_obj

def print_content(data,decode):
    for line in data:
        if decode and isinstance(line,bytes):
            # Try to decode using default utf-8, if fail try latin1
            try:                 
                line = line.decode()
            except:	  
                try: 
                    line = line.decode("latin1")
                except:
                    line = str(line)
            if decode_http.isHTTP(line) and "Content-Encoding: gzip" in line : # Decode HTTP if compressed by gzip
                line = decode_http.httpDecodeContent(line)
                #print(line)
                
            
        print(str(line))

# Open the log file for reading
with open(log_file_path, 'r') as log_file:
    for log_entry in log_file:
        ######## REQUEST #########
        if "[id:" in log_entry and log_entry.startswith("[INFO] Request"):
            # Extract the ID from the log entry
            current_id = log_entry.split("[id:")[1].split("]")[0].strip()
            if current_id == request_id:
                request_found = True
                request.append(log_entry.strip())
                continue
        if request_found:
            if log_entry.startswith("[INFO]"):
                request_found = False
                
            else:
                request.append(log_entry.strip())

        ######## RESPONSE #########
        if "[id:" in log_entry and log_entry.startswith("[INFO] Response"):
            # Extract the ID from the log entry
            current_id = log_entry.split("[id:")[1].split("]")[0].strip()
            if current_id == request_id:
                response_found = True
                response.append(log_entry.strip())
                continue
        if response_found:
            if log_entry == "\n":
                response_found = False
                continue
            else:
                if log_entry.startswith("b'") or log_entry.startswith("b\""): # convert back to bytes if any byte object
                    response.append(convert_byte_string_to_bytes(log_entry.strip()))
                    continue
                response.append(log_entry.strip())

if len(request) == 0 and len(response) == 0 :
    print("ID not found !")
else:       
    if len(response) > 2:    # concat the byte stream of response so that it becomes 1 stream only
        byte_string = bytes()
        for res in response:
            if isinstance(res,bytes):
                byte_string += res
    response = [response[0],byte_string]

    # Result
    print("######## REQUEST #########\n")
    print_content(request,decode)

    print("\n######## RESPONSE #########\n")
    print_content(response,decode)



