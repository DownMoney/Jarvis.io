import Modules
import pyjsonrpc

class RequestHandler(pyjsonrpc.HttpRequestHandler):

	modules = []

	for m in Modules.__all__:
	    mod = m.split('.')
	    modules += [__import__(m, globals(), locals(), [mod[len(mod)-1]], -1)]

	methods = {}

	for m in modules:
		methods = dict(methods.items() + m.getMethods().items())

	print methods['GetCurrentLocation']()
# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 6478),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:6478"
http_server.serve_forever()




