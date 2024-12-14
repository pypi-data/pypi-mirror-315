def make_filename(
    name: str,
    extension: str = "",
    max_length: int = 100,
    ) -> str:
    characters_to_remove = [
        "\\", "/", ".", "'", "\"", "™", "`", "!", "?", "®", "©", "*", 
        "<", ">", "(", ")", "[", "]", "{", "}", "#", "$", "%", "^", 
        "€", "£", "¥", "§", "°", "¬", "¦", "´", "¨" ,"\0", ","
    ]  
    for character in characters_to_remove:
        name = name.replace(character, "")

    characters_to_replace_with_space = ["|", "~", "-", "–", "—", "―", ":", ";", "：", "+"]
    for character in characters_to_replace_with_space:
        name = name.replace(character, " ")
  
    name = name.replace("&", " and ")

    name = '_'.join(name.split())

    if len(name) > max_length:
        name = name[:max_length]

    if len(name) > 0 and name[-1] == "_":
        name = name[:-1]

    if len(extension) > 0 and extension[0] != ".":
        extension = "." + extension

    name = name + extension

    return name
