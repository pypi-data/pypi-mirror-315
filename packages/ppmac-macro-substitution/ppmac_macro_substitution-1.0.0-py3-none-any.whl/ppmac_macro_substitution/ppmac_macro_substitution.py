import fileinput
from pathlib import Path


def generate(
    substitutes,
    template_files,
    template_source_folder="configure/coord_templates",
    destination_folder="configure/coord_substitutions",
):
    """
    Gets substitutes and template files (stored in template_source_folder),
    uses them to generate files (primarily kinematics).

    The generated files are put in destination_folder which defaults to
    configure/coord_substitution.

    Naming convention for generated kinematics:
        cs_<coordinate_system_number>_<name_of_template_file>
    and for other files:
        tmp_<name_of_template_file>

    Args:
        substitutes (dict):
            A dictionary that holds names of all substitutes and their values.
        template_files (list):
            A list of template file names.
        template_source_folder (Str, optional):
            A folder in which the template files are kept.
            Defaults to:
            configure/coord_templates.
        destination_folder (Str, optional):
            A folder in which the generated files are put.
            Defaults to:
            configure/coord_substitutions
    """
    for template_file in template_files:
        if "$(COORD)" in substitutes:
            destination_file = Path(destination_folder).joinpath(
                Path("cs" + substitutes["$(COORD)"] + "_" + template_file)
            )

        else:
            destination_file = Path(destination_folder).joinpath(
                Path("tmp_" + template_file)
            )
        header = (
            "// DO NOT MODIFY: File created from template file: " + template_file + "\n"
        )
        if destination_file.exists():
            f = open(destination_file, "w")
            f.write(header)
        else:
            f = open(destination_file, "x")
            f.write(header)
        template_file_path = Path(template_source_folder).joinpath(template_file)
        for line in fileinput.input(template_file_path):
            for key in substitutes:
                if key in line:
                    line = line.replace(key, substitutes[key])
            f.write(line)
