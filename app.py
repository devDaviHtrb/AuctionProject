from app import create_app


instance = create_app()

if __name__ =="__main__":
    instance["socket"].run(instance["app"], debug=True)