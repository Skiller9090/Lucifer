def write_file_exists(output_file, out, write_mode):
    if output_file != "":
        with open(output_file, write_mode) as f:
            f.write(out)
