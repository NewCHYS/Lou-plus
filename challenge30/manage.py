from simpledu.app import create_app

app = create_app('development')

if __name__ == '__main__':
	app.run(host='192.168.10.128')

