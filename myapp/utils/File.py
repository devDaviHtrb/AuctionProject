def erase_file(src:str, content:str = ""):
    with open(src, 'w') as file:
        file.write(content)


def write_file(src:str, content:str) -> None:
    with open(src, 'a') as file:
        file.write(content)