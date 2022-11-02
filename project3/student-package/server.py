import socket
import signal
import sys
import random

# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" name = "button"/>
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % port

#### Helper functions
# Printing.
def print_value(tag, value):
    print("Here is the", tag)
    print("\"\"\"")
    print(value)
    print("\"\"\"")
    print

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)

# TODO: put your application logic here!
# Read login credentials for all the users
passwords = {}
passwordFile = open('passwords.txt', 'r')
lines = passwordFile.readlines()
for line in lines:
    creds = line.split(' ')
    username = creds[0].strip('\n')
    password = creds[1].strip('\n')
    passwords[username] = password
passwordFile.close()

# Read secret data of all the users
secrets = {}
secretFile = open('secrets.txt', 'r')
lines = secretFile.readlines()
for line in lines:
    info = line.split(' ')
    username = info[0].strip('\n')
    secret = info[1].strip('\n')
    secrets[username] = secret
secretFile.close()

start = True

cookies = {}

headers_to_send = ''

### Loop to accept incoming HTTP connections and respond.
while True:
    client, addr = sock.accept()
    req = client.recv(1024)

    if start:
        print('Start Program')
        html_content_to_send = login_page
        # clear the cookie
        # headers_to_send = 'Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT\r\n'
        start = False
    else: 
        # Let's pick the headers and entity body apart
        header_body = req.decode('utf-8').split('\r\n\r\n')
        headers = header_body[0]
        body = '' if len(header_body) == 1 else header_body[1]
        print()
        print('---------------------------------------------')
        print()
        print_value('headers', headers)
        print_value('entity body', body)

        # TODO: Put your application logic here!
        # Parse headers and body and perform various actions
        # print(cookieStatus)
        # extract the cookie and see if it is in cookies[]
        headerlines = headers.split('\n')
        cookieStatus = False
        cookie = ''
        if 'Cookie: token=' in headerlines[len(headerlines) - 1]:
            print('\nCookie Found')
            cookieStatus = True
            cookie = headerlines[len(headerlines) - 1][14:]
            print('\nCookie is ' + cookie)
        # if it is, authenticiate immediatley and skip the login
        if cookieStatus: 
            print(cookies)
            #this if is not working currently
            if int(cookie) in cookies.keys():
                print('\nCookie Found in dictionary')
                html_content_to_send = success_page + secrets[cookies[int(cookie)]]

        # if it is not, send to bad login page
        if 'action=logout' in body:
            print('LOGOUT ACCOUNT')
            html_content_to_send = login_page
            headers_to_send = 'Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT\r\n'
        else: 
        # if there is no cookie, send to login_page
            if body == '':
                #html_content_to_send = login_page
                print('EMPTY BODY/ NOT USED')
            else:
                credentials = body.strip('\n').split('&')
                _, username = credentials[0].split('=')
                if username == 'logout':
                    print('LOGOUT ACCOUNT')
                    html_content_to_send = login_page
                    headers_to_send = 'Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT\r\n'
                else:
                    _, password = credentials[1].split('=')
                    _, submit = credentials[2].split('=')
                    if (username in passwords and passwords[username] == password):
                        html_content_to_send = success_page + secrets[username]
                        rand_val = random.getrandbits(64)
                        cookies[rand_val] = username
                        headers_to_send = 'Set-Cookie: token=' + str(rand_val) + '\r\n'
                        print('CREDENTIALS MATCH')
                    else:
                        html_content_to_send = bad_creds_page
                        print('BAD MATCH')

    # You need to set the variables:
    # (1) `html_content_to_send` => add the HTML content you'd
    # like to send to the client.
    # Right now, we just send the default login page.
    #html_content_to_send = login_page
    # But other possibilities exist, including
    # html_content_to_send = success_page + <secret>
    # html_content_to_send = bad_creds_page
    # html_content_to_send = logout_page
        
    # (2) `headers_to_send` => add any additional headers
    # you'd like to send the client?
    # Right now, we don't send any extra headers.    
    

    # Construct and send the final response
    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)    
    client.send(response.encode('utf-8'))
    client.close()
            
    print("Served one request/connection!")
    print

# We will never actually get here.
# Close the listening socket
sock.close()
