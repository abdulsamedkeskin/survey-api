from api import create_app

if __name__ == '__main__':
    create_app('config.py').run(debug=True)