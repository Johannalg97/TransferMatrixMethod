import csv

from mpmath import sqrt

"""
This file contains functions that will be used multiple times
across out project. They are written here since we can import them
from different files to use them. This functions are usually called from
views.py where all the logic of the app is executed. This functions
also help pur views to be shorter and less complex to read since we separate
some of the code and logic in different functions.
"""


import ast
import json

import numpy as np


from app.api.interpolacion import interpolation


def get_nk(d):
    """
    This funtion return a list of tuplas: [(lambda, n, k )]
    """
    aux = []
    data = d["DATA"]
    for j, v in enumerate(data):
        if v.get("type").startswith("tabulate"):
            for j in v["data"].split("\n"):
                tupla = tuple(j.split())
                aux.append(tupla)
    return aux


def get_range_list(initial_value, final_value, pasos):
    """
    function that returns a list with the list of angles
    or wavelengths that the program will traverse.

    """
    a = initial_value
    incremento = (final_value - initial_value) / pasos
    range_list = []
    while len(range_list) < pasos:
        a = a + incremento
        range_list.append(a)
    return range_list


def get_nk_from_dielectric_fuction(epsilon_1, epsilon_2):
    """
    This funtion:
    *Calculate los valores de n and k from the dielectic funtion
    *Receives the valuos of the dielectic funtion (epsilon_1 and epsilon_2)
    * Retur a list with two values n and k
    """
    a = sqrt(epsilon_1**2 + epsilon_2**2)
    n = sqrt((epsilon_1 + a) / 2)
    k = sqrt((-epsilon_1 + a) / 2)
    return complex(float(n), float(k))


def get_dielectric_funtion_from_nk(n, k):
    """
    This funtion:
    *Calculate los valores de epsilon_1 and epsilon_1 from the n and k
    *Receives the valuos of n and k
    * Retur a list with two values (epsilon_1 and  epsilon_2)
    """
    epsilon_1 = n**2 - k**2
    epsilon_2 = 2 * n * k
    return complex(float(epsilon_1), float(epsilon_2))


def format_graph_data(data):
    """
    Returns just the real part of every value from
    the data
    """
    return [round(float(value.real), 4) for value in data]


def get_values_from_file(file_, file_type):
    wl_list = []
    n_list = []
    k_list = []
    current_parameter = "n"

    if file_type == "csv":
        file_ = csv.DictReader(file_)
        for line in file_:
            # Getting two possible values from the row
            current_wl = line.get("wl")
            current_value = line.get("n")
            try:
                # Try to convert the numbers to float
                current_wl = float(current_wl)
                current_value = float(current_value)
            except ValueError:
                # The current row does not contain number,
                # it has a new title where the k values start
                current_parameter = "k"
            else:
                # As wl is repeated we are going to append values
                # just when they don't exist in the current list
                if current_wl not in wl_list:
                    wl_list.append(current_wl)

                # Check the current parameter to add it to the corresponding list
                n_list.append(
                    current_value
                ) if current_parameter == "n" else k_list.append(current_value)

    if file_type == "plain":
        file_ = csv.reader(file_, delimiter="\t")
        for line in file_:
            # Skip empty line
            if not len(line):
                continue

            # Files with three columns (w,n,k)
            if isinstance(line, list) and len(line) == 1:
                line = line[0].strip()
                current_wl, current_n, current_k = line.split(" ")

                try:
                    wl_list.append(float(current_wl))
                    n_list.append(float(current_n))
                    k_list.append(float(current_k))
                # skip the title
                except ValueError:
                    continue
            else:
                # Files with two columns and k appears at the middle of the file
                # Getting two possible values from the row
                current_wl = line[0]
                current_value = line[1]
                try:
                    # Try to convert the numbers to float
                    current_wl = float(current_wl)
                    current_value = float(current_value)
                except ValueError:
                    # The current row does not contain number,
                    # it has a new title where the k values start
                    if current_value == "k":
                        current_parameter = "k"
                else:
                    # As wl is repeated we are going to append values
                    # just when they don't exist in the current list
                    if current_wl not in wl_list:
                        wl_list.append(current_wl)

                    # Check the current parameter to add it to the corresponding list
                    n_list.append(
                        current_value
                    ) if current_parameter == "n" else k_list.append(current_value)

    if file_type == "x-yaml":
        reading_data = False
        for line in file_:
            # We found the start of the data in the file
            if "data:" in line:
                reading_data = True
                # Skip this line to start reading data in the next line
                continue

            # Start read data from each row. In this case
            # each row is a string with numbers separeted by spaces
            if reading_data:
                # Delete spaces at the beginning and at the end of the row
                line = line.strip()
                # Get a list with values using the space as a separator
                current_wl, current_n, current_k = line.split(" ")

                # Add the values to the lists
                wl_list.append(float(current_wl))
                n_list.append(float(current_n))
                k_list.append(float(current_k))

    if len(k_list) == 0:
        k_list = [0] * len(wl_list)

    return wl_list, n_list, k_list


def get_inclusions(material):

    inclusions = []
    for item_name in material:
        if "inclusion" in item_name:
            inclusions.append(material[item_name])
    return inclusions


def order_materials(materials):
    """
    Order materials:
    1. Substrate
    2. Layers
    3. Host
    """
    ordered_materials = []
    substrate = None
    host = None

    for material_name in materials:
        material = materials[material_name]
        if material_name == "substrate":
            substrate = material
        elif material_name == "host":
            host = material
        else:
            ordered_materials.append({material_name: material})

    # Add substrate at first position
    if substrate:
        ordered_materials.insert(0, {"substrate": substrate})

    # Add host to last position
    if host:
        ordered_materials.append({"host": host})

    return ordered_materials


def group_materials(materials):
    """
    Creates a bid dictionary with the nested data for
    each material, adding inclusions, components and files
    under one single key, the name of the material
    """
    grouped_materials = {}

    for material in materials:
        if isinstance(material, str):
            # Plain data
            material = json.loads(material)
            for material_name in material.keys():
                if material_name not in grouped_materials:
                    grouped_materials[material_name] = {}

                for parameter in material[material_name]:
                    grouped_materials[material_name][parameter] = material[
                        material_name
                    ][parameter]
        else:
            # File
            material_name = material.name
            method = "upload-file"

            if "maxwell" in material_name:
                material_name = material_name.split("-maxwell")[0]
                method = "maxwell"

            if "lorentz" in material_name:
                material_name = material_name.split("-lorentz")[0]
                method = "lorentz"

                if "em" in material_name or "ei" in material_name:
                    current_submaterial = "em" if "em" in material_name else "ei"
                    base_material_name = material_name.split(f"-{current_submaterial}")[
                        0
                    ]

                    # Add material key of doesnt exist on the grouped materials
                    if base_material_name not in grouped_materials:
                        grouped_materials[base_material_name] = {}

                    # Option already added to em
                    if current_submaterial in grouped_materials[base_material_name]:
                        grouped_materials[base_material_name][current_submaterial][
                            "file"
                        ] = material
                    else:
                        # Add em to material
                        grouped_materials[base_material_name][current_submaterial] = {}
                        grouped_materials[base_material_name][current_submaterial][
                            "file"
                        ] = material

                # Add method and move to the next material
                grouped_materials[base_material_name]["option"] = method
                continue

            if "bruggeman" in material_name:
                material_name = material_name.split("-bruggeman")[0]
                method = "bruggeman"

            if "inclusion" in material_name or "component" in material_name:
                base_material_name = material_name.split(
                    "-inclusion" if "inclusion" in material_name else "-component"
                )[0]
                # Material already in dictionary keys
                if base_material_name in grouped_materials:
                    # Inclusion/component already in material dictionary
                    if material_name in grouped_materials[base_material_name]:
                        grouped_materials[base_material_name][material_name][
                            "file"
                        ] = material
                    else:
                        # Add inclusion/component and file to material dictionary
                        grouped_materials[base_material_name][material_name] = {}
                        grouped_materials[base_material_name][material_name][
                            "file"
                        ] = material
                else:
                    # Add material to dict
                    grouped_materials[base_material_name] = {}
                    material_name = base_material_name

            else:
                if material_name not in grouped_materials:
                    grouped_materials[material_name] = {}

                grouped_materials[material_name]["file"] = material
                grouped_materials[material_name]["option"] = method

    return grouped_materials


def process_file(file_, initial_parameters, answer, steps):
    # Get extension
    file_type = file_.content_type.split("/")[1]

    # Read file
    decoded_file = file_.read().decode("utf-8").splitlines()

    # Set initial parameters
    w_i = (
        initial_parameters.get("waveLength")
        if answer == "angular"
        else initial_parameters.get("initialWaveLength")
    )
    w_f = w_i if answer == "angular" else initial_parameters.get("finalWaveLength")

    # Get list of values for wl, n and k
    wl_list, n_list, k_list = get_values_from_file(decoded_file, file_type)

    # Calculate interpolation
    result = interpolation((wl_list, n_list, k_list), w_i, w_f, steps, respuesta=answer)

    return result


def format_number(number):
    if isinstance(number, float) or isinstance(number, str) or isinstance(number, int):
        number = round(number, 4)
    if isinstance(number, complex):
        number = complex(round(number.real, 4), round(number.imag, 4))
    return number


def create_file(response, data_source, data, answer, graph_type=None):
    writer = csv.writer(response)
    if data_source == "table":
        headers = []
        headers.append("Wave Length")
        for material_name in data:
            # Headers
            if material_name != "x":
                headers.append(material_name.capitalize())
        writer.writerow(headers)
        # Actual data
        x = data.get("x")
        if isinstance(x, float) or isinstance(x, int):
            x = [x]

        for index in range(len(x)):
            current_row = []
            # Add wavelength
            x_value = format_number(x[index])
            current_row.append(x_value)

            # Add material refractive indexes
            for material_name in data:
                if material_name != "x":
                    material_data = ast.literal_eval(data[material_name])
                    value = (
                        material_data[index]
                        if isinstance(material_data, list)
                        else material_data
                    )
                    value = format_number(value)
                    current_row.append(value)

            # Write row on csv file
            writer.writerow(current_row)

    else:
        # Headers
        writer.writerow(
            [
                "Wave Length" if answer == "espectral" else "Angle",
                graph_type.capitalize(),
            ]
        )
        x = data.get("x")
        y = data.get("y")

        # Actual data
        for index in range(len(x)):
            x_value = f"{float(x[index]):.4n}"
            y_value = f"{float(y[index]):.4n}"
            writer.writerow(
                [
                    x_value,
                    y_value,
                ]
            )
    filename = f"TransferMatrixMethod_{data_source}.csv"
    response["Content-Disposition"] = "attachment; filename=%s" % filename
    return response


def get_current_vector(refractive_indexes, position):
    return [
        refractive_indexes[material][position]
        for material in range(len(refractive_indexes))
    ]


def get_reflectance_from_file(file_):
    file_type = file_.content_type.split("/")[1]
    decoded_file = file_.read().decode("utf-8").splitlines()
    x_vector = []
    y_vector = []

    for line in decoded_file:
        current_x, current_y = line.split(",")
        try:
            # Try to convert the numbers to float
            current_x = float(current_x)
            current_y = float(current_y)
        except ValueError:
            continue
        else:
            x_vector.append(current_x)
            y_vector.append(current_y)

    print(x_vector, y_vector)
    return x_vector, y_vector


def chi_square(
    y_experimental, x_experimental, y_theorical, initial_param, final_param, steps
):
    x = np.linspace(initial_param, final_param, steps)
    y_experimental = np.interp(x, x_experimental, y_experimental)
    n = 0
    accum = 0
    while n < len(y_theorical):
        accum += (y_experimental[n] - y_theorical[n]) ** 2
        n += 1
    return accum, y_experimental
