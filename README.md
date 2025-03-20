This script extracts custom shapes from a Tableau workbook file (.twb or .twbx) and saves them to a specified output directory. Below is a description of its functionality for a README file:

---

## Extract Tableau Shapes Script

This script extracts all custom shapes from a Tableau workbook file (.twb or .twbx) and saves them to a specified output directory.

### Features

- Extracts custom shapes from Tableau workbook files (.twb or .twbx).
- Saves extracted shapes to a specified output directory.
- Creates necessary directories if they do not exist.
- Prints messages indicating the creation of directories or if they already exist.
- Cleans up temporary directories after extraction.

### Usage

```bash
python extract-tableau-shapes.py path/to/your/workbook.twb(x) [outputdir] [tmpdir]
```

- `workbook`: Path to the Tableau workbook file (.twb or .twbx).
- `outputdir` (optional): Path to the output directory. Default is `./Shapes`.
- `tmpdir` (optional): Path to the temporary directory. Default is `./tmp`.

### Example

```bash
python extract-tableau-shapes.py my_workbook.twbx ./Shapes ./tmp
```

### Functions

- `cleanup(tmp_dir)`: Deletes the temporary directory.
- `mkdirs(output_dir, tmp_dir)`: Creates the output and temporary directories if they do not exist.
- `extract_shapes(tableauworkbook, output_dir, tmp_dir)`: Extracts custom shapes from the Tableau workbook and saves them to the output directory.

### Author

Created by Johan de Groot @ Antichaos
For questions or suggestions, contact: tableaudev@antichaos.net