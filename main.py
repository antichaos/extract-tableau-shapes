import argparse
import base64
import os
import re
import zipfile
import shutil

output_dir = './Shapes'
os.makedirs(output_dir + output_dir, exist_ok=True)

tmp_dir = 'tmp'
os.makedirs(tmp_dir, exist_ok=True)


def extract_shapes(tableauworkbook):
    if tableauworkbook.endswith('.twbx'):
        with zipfile.ZipFile(tableauworkbook, 'r') as zip_ref:
            # Extract the .twb file from the .twbx archive
            for file in zip_ref.namelist():
                if file.endswith('.twb'):
                    zip_ref.extract(file, tmp_dir)
                    tableauworkbook = os.path.join(tmp_dir, file)
                    break

    # Read the content of the .twb file
    with open(tableauworkbook, 'r') as file:
        content = file.read()

    # Find all base64 encoded PNG data
    shape_data_list = re.findall(r'<shape name=\'(.*?)\'>(.*?)</shape>', content, re.DOTALL)

    # Decode and save each Shape file
    for i, shape_data in enumerate(shape_data_list):
        shape_filename = shape_data[0]
        print("file: ", shape_filename)
        png_bytes = base64.b64decode(shape_data[1])
        directory = os.path.dirname(shape_filename)

        with open(f'{output_dir}{shape_filename}', 'wb') as shape_file:
            shape_file.write(png_bytes)

    # Delete the tmp directory
    shutil.rmtree(tmp_dir)

    # print(f"Extracted {len(shape_data_list)} Shapes from workbook \033[1m{tableauworkbook}\033[0m to \033[1m{output_dir}\033[0m.")
    print(f"Extracted \033[34m{len(shape_data_list)} shapes\033[0m from workbook \033[34m{tableauworkbook_orig}\033[0m to \033[34m{output_dir}\033[0m.")

def extract_parameters(tableauworkbook):
    # get all parameters from this workbook
    with open(tableauworkbook, 'r') as file:
        content = file.read()

        # find all parameters
        parameters = re.findall(r'<datasource-dependencies datasource=\'Parameters\'>(.*?)\'', content)
        print(parameters)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Extract all custom shapes from a Tableau workbook.',
        usage='python main.py path/to/your/workbook.twb(x)'
    )
    parser.add_argument('workbook', type=str, nargs='?', default=None, help='Path to the Tableau workbook file (.twb or .twbx)')
    args = parser.parse_args()

    if args.workbook:

        tableauworkbook_orig = args.workbook

        # if not ends with .twb or .twbx, exit
        if not args.workbook.endswith('.twb') and not args.workbook.endswith('.twbx'):
            print("Please provide a Tableau workbook file (.twb or .twbx).")
            exit()

        # check if file exists
        if not os.path.exists(args.workbook):
            print("File does not exist.")
            exit()

        extract_shapes(args.workbook)

    else:
        print("No workbook file provided. Please specify the path to the Tableau workbook file.")

