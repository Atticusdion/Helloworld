path = 'Annotation/coding_qual_input.txt'

def decode(message_file):

    step = 1
    pos = 1
    code = ""

    with open(message_file, 'r') as file:
        
        lines = file.readlines()
        len(lines)

        while pos <= len(lines):
            for line in lines:   
                words = line.strip().split()

                if words and int(words[0]) == pos:
                    code = code + words[1] + " "
            step += 1
            pos += step

    return code

print(f"The decoded text is '{decode(path)}'")