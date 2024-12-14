# makefilename

Takes an input string + extension and turns it into a sanitized filename.

    from makefilename import make_filename

    name_game = "Counter-Strike 2"

    filename = make_filename(name_game, extension=".json")
    # filename == "Counter_Strike_2.json"
