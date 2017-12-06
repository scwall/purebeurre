def search_quote(command):
    if "'" in command:
        cut_string = list(command)
        for index, character in enumerate(cut_string):
            if character is "'":
                cut_string[int(index)] = str("''")
        command = "".join(cut_string)
        return str("'") + command + str("'")

    else:
        return str("'") + command + str("'")
