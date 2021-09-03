from flask_blog import create_app

app = create_app()

if __name__ == '__main__':
	from sys import argv
	from getopt import getopt
	debug = False
	host='0.0.0.0'
	port=8080

	opts, args = getopt(argv[1:], 'dp:h:', ['debug', 'port=', 'host='])
	
	for opt, val in opts:
		if opt in ['-d', '--debug']:
			debug=True
		elif opt in ['-p', '--port']:
			port=int(val)
		elif opt in ['-h', '--host']:
			host=val

	app.run(host=host, port=port, debug=debug)
