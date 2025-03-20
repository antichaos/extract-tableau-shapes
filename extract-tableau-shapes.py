import argparse
import base64
import os
import re
import zipfile
import shutil

def cleanup(tmp_dir):
    # Delete the tmp directory
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    print(f"Deleted temporary directory: {tmp_dir}")

def mkdirs(output_dir, tmp_dir):
    # Create the output and tmp directories if they don't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"Created directory: {output_dir}")
    else:
        print(f"Directory already exists: {output_dir}")

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir, exist_ok=True)
        print(f"Created directory: {tmp_dir}")
    else:
        print(f"Directory already exists: {tmp_dir}")

def extract_shapes(tableauworkbook, output_dir="./Shapes", tmp_dir="./tmp"):
    print("\n\033[1m*** Extracting custom shapes from Tableau workbook ***\033[0m")
    print("\033[1m*** Created By Johan de Groot @ Antichaos ***\033[0m")

    print("output_dir: ", output_dir)
    print("tmp_dir: ", tmp_dir)
    mkdirs(output_dir, tmp_dir)
    # If the workbook is a .twbx file, extract the .twb file
    if tableauworkbook.endswith('.twbx'):
        with zipfile.ZipFile(tableauworkbook, 'r') as zip_ref:
            # Extract the .twb file from the .twbx archive
            for file in zip_ref.namelist():
                if file.endswith('.twb'):
                    print("Extracting workbook from .twbx file...")
                    zip_ref.extract(file, tmp_dir)
                    tableauworkbook = os.path.join(tmp_dir, file)
                    print("Extracted workbook to:\033[34m ", tableauworkbook, "\033[0m")
                    break

    # Read the content of the .twb file
    with open(tableauworkbook, 'r') as file:
        content = file.read()

    # Find all base64 encoded PNG data
    shape_data_list = re.findall(r'<shape name=\'(.*?)\'>(.*?)</shape>', content, re.DOTALL)

    # Decode and save each Shape file
    for i, shape_data in enumerate(shape_data_list):
        shape_filename = shape_data[0]
        print("Shapefile: \033[34m", shape_filename, "\033[0m")
        png_bytes = base64.b64decode(shape_data[1])
        directory = os.path.dirname(shape_filename)

        os.makedirs(output_dir + "/" + directory, exist_ok=True)

        with open(f'{output_dir}/{shape_filename}', 'wb') as shape_file:
            shape_file.write(png_bytes)

    # print(f"Extracted {len(shape_data_list)} Shapes from workbook \033[1m{tableauworkbook}\033[0m to \033[1m{output_dir}\033[0m.")
    print(f"\nExtracted \033[34m{len(shape_data_list)} shapes\033[0m from workbook \033[34m{tableauworkbook_orig}\033[0m to \033[34m{output_dir}\033[0m.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Extract all custom shapes from a Tableau workbook.',
        usage='python extract-tableau-shapes.py path/to/your/workbook.twb(x)'
    )
    parser.add_argument('workbook', type=str, nargs='?', default=None, help='Path to the Tableau workbook file (.twb or .twbx)')
    parser.add_argument('outputdir', type=str, nargs='?', default="./Shapes", help='Path to the output directory, default current directory/Shapes')
    parser.add_argument('tmpdir', type=str, nargs='?', default="./tmp", help='Path to the temp directory, default current directory/tmp')
    args = parser.parse_args()

    if args.workbook:
        tableauworkbook_orig = args.workbook

        # if not ends with .twb or .twbx, exit
        if not args.workbook.endswith('.twb') and not args.workbook.endswith('.twbx'):
            print("Please the name and path of a Tableau workbook (.twb or .twbx).")
            exit()

        # check if file exists
        if not os.path.exists(args.workbook):
            print("This file does not seem to exist. Please check the path and the name.")
            exit()

        output_dir = args.outputdir
        tmp_dir = args.tmpdir


        extract_shapes(args.workbook)
        # cleanup(tmp_dir)

        print("\n\n\033[1m\033[34mDone!\033[0m")



    else:
        print("\033[1m*** No workbook file provided. Please specify the path to the Tableau workbook file. ***\033[0m")
    print("\n")
    print("\033[37m-------------------------------------------------------------\033[0m")
    print("\033[37m---- Created By Johan de Groot @ Antichaos ------------------\033[0m")
    print("\033[37m---- https://antichaos.net ----------------------------------\033[0m")
    print("\033[37m---- Questions, suggestions? tableaudev@antichaos.net -------\033[0m")
    print("\033[37m-------------------------------------------------------------\033[0m")