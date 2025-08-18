from app import createApp


instance = createApp()

if __name__ =="__main__":
    instance["socket"].run(instance["app"], debug=True)