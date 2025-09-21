from myapp import create_app

app, socketIo = create_app()

if __name__ == "__main__":
    socketIo.run(app, debug=True)

