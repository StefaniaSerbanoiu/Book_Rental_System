def get_properties(filepath, separator='='):
    properties = {}
    with open(filepath, "rt") as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                key_value = stripped_line.split(separator)
                key = key_value[0].strip()
                value = separator.join(key_value[1:]).strip().strip('"')
                properties[key] = value
    return properties




