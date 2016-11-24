#HTTP Server 1.0 . Build on Python 2.7.12 . Serves HTML,CSS,JS and many more
import socket


def get_resource_name(request):
	request=str(request.splitlines()[0]).split(" ")[1]
	if request=='/':
		return 'index.html'
	else:
		return request[1:]


def get_content_type(resource_name): #gets the MIME type of the requested file 
	res_type=resource_name.split('.')[1]
	if res_type=='html':
		return 'Content-Type: text/html'
	elif res_type=='png':
		return 'Content-Type: image/png'
	elif res_type=='jpeg':
		return 'Content-Type: image/jpeg'
	elif res_type=='gif':
		return 'Content-Type: image/gif'
	elif res_type=='bmp':
		return 'Content-Type: image/bmp'
	elif res_type=='js':
		return 'Content-Type: appication/javascript'
	elif res_type=="css":
		return 'Content-Type: text/css'
	elif res_type=='ico':
		return 'Content-Type: image/vnd.microsoft.icon'
	elif res_type=='pdf':
		return 'Content-Type: application/pdf'


def get_file_status(resource_name):#gets the status of the requested file. whether exists or not
	try:
		# print "this is the resource name:"+resource_name
		file=open(resource_name,'r')
		file.close()
		return "200 OK"
	except IOError:
		return "404 Not Found"


def set_res_header(status,content_type=None,resource=None):
	if((content_type==None) or (resource==None)):
		header="""HTTP/1.1 """+status+""""\r\nServer: Pasan/1.0\r\n\r\n"""
	else:
		header="""HTTP/1.1 """+status+""""\r\n"""+content_type+"""\r\nServer: Pasan/1.0\r\n\r\n"""
	return header


def create_Socket(host,port):
	onlinesocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	onlinesocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	onlinesocket.bind((host,port))
	onlinesocket.listen(2)
	print 'Serving HTTP Server on port %s ' %port
	return onlinesocket


def start_Server(socket):
	while True:
		connection,conn_address=socket.accept()
		request=connection.recv(1024)
		# print 'Client Address'+conn_address
		print request

		http_response=''

		if(request=='' or request==' '):
			continue
		else:
			try:
				resource_name=get_resource_name(request)


				file_status=get_file_status(resource_name)

				if(file_status=='200 OK'):
					content_type=get_content_type(resource_name)

					header=set_res_header(file_status,content_type,resource_name)

					body=open(resource_name,'rb').read()

					http_response=header+body
				else:
					header=set_res_header(file_status)
					body="""<html>
								<head><title>Page Not Found</title></head>
								<body>
									<h1>404 Page Not Found</h1>
									<p>The page you requested does not exist</p>
								</body>
							</html>"""
					http_response=header+body

				connection.send(http_response)
				connection.close()
			except IndexError:
				continue


start_Server(create_Socket('',9000)) #starting the Server
