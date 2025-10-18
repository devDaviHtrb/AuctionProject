from myapp import create_app
from myapp.services.Messages import auth_message


app, socketIo = create_app()

if __name__ == "__main__":
    socketIo.run(app, debug=True)

