from flask_blog import create_app

app = create_app()

if __name__ == '__main__':
	from sys import argv
	debug = False
	for arg in argv:
		if arg in ['-d', '--debug', 'debug']:
			debug=True
	app.run(host='0.0.0.0', port=8080, debug=debug)
