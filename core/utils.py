def get_file_lines(filepath):
    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    return lines
