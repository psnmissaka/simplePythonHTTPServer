import socket

def get_resource_name(request):
	request=str(request.splitlines()[0]).split(" ")[1]
	if(request=="/"):
		return 'index.html'
	else:
		return request[1:]

def get_content_type(resource_name): #gets the MIME type of the requested file
	res_type=resource_name.split('.')[1]
	if(res_type=='html'):
		return 'Content-Type: text/html'
	elif(res_type=='png'):
		return 'Content-Type: image/png'
	elif(res_type=='jpeg'):
		return 'Content-Type: image/jpeg'
	elif(res_type=='js'):
		return 'Content-Type: appication/javascript'
	elif(res_type=='ico'):
		return 'Content-Type: image/vnd.microsoft.icon'

def get_file_status(resource_name):#gets the status of the requested file. whether exists or not
	try:
		print("this is the resource name:"+resource_name)
		file=open(resource_name,'r')
		file.close()
		return "200 OK"
	except FileNotFoundError:
		return "404 Not Found"

def set_res_header(status,content_type=None,resource=None):
	if((content_type==None) or (resource==None)):
		header="""HTTP/1.1 """+status+""""\r\nServer: Netx/1.0\r\n\r\n""" #HTTP/1.1 200 OK Content-Type: text/html Server: myserver
	else:
		header="""HTTP/1.1 """+status+""""\r\nServer: Netx/1.0\r\n\r\n"""
	return header

HOST, PORT = '', 9000

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(2)
print ('Serving HTTP on port %s ...' % PORT)


while True:   #when there's a request
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print(client_address)
    print(request)

    http_response=''
    if(request=='' or request==" " or request==None or request=="b''"):
    	break
    else:
    	try:
    		resource_name=get_resource_name(request.decode('utf-8'))
    		file_status=get_file_status(resource_name)
    		if(file_status=='200 OK'):
    			header=set_res_header(file_status,get_content_type(resource_name),resource_name)
    			try:
    				body=open(resource_name).read()
    				http_response=header+body
    				print(http_response)
    				# print("Have file")
    			except UnicodeDecodeError:
    				continue
    		else:
    			print(set_res_header(file_status))
    			#http_response=set_res_header(file_status)
    			#print("Dont have it"+http_response)
    		client_connection.sendall(http_response.encode('utf-8'))
    		client_connection.close()
    	except IndexError:
    		continue
    	