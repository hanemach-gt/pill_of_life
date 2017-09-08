# appends to output message buffer a string to be displayed to player
def append_output_message(message_output, string_to_be_appended):
    for subline in string_to_be_appended.split("\n"):
        message_output.append([" "] + list(subline))


# clears output message buffer and appends a new string to it
# output_message is a list of lists made of strings to conform to map design
def set_output_message(message_output, string_to_be_printed):
    message_output.clear()
    append_output_message(message_output, "") # empty line
    append_output_message(message_output, string_to_be_printed)
