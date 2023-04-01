"""
This is the main file in our backend. Views are in charge to respond 
the HTTP requests received. Each HTTP request arrives to an specific endpoint, each
endpoint is related to a specific view and the view has the logic to resolve the request.
The views have properties such as permissions, to know which kind of users can retrieve or 
send information to the server, parser classes to know which kind of data
can receive, as JSON data or also files and a serializer class to know
how to format or how to map data recived on post requests.

Since we are creating an API inside of our backend we are importing
django rest framwork classes and functions for it. DRF is a Django framework
to create REST APIs so it offers built-in views and ways to respond to the server.
Here we overwrite some of this methods related to DRF built-in views so we can 
addour logic and respond to the browser according to our needs. 
"""


import csv
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.dispersion_models import DispersionModels
from app.api.efective_medium_theories import EfectiveMediumTheories
from app.api.serializers import TransferSerializer
from app.api.transfer_matrix_method import TransferMatrixMethod
from app.api.utils import (
    chi_square,
    create_file,
    format_graph_data,
    format_number,
    get_current_vector,
    get_dielectric_funtion_from_nk,
    get_inclusions,
    get_range_list,
    get_reflectance_from_file,
    get_values_from_file,
    group_materials,
    order_materials,
    process_file,
)


class CalculateDataView(APIView):
    """
    View to receive POST data from the VUE components about the different
    materials and retrieve graphics data
    """

    # Allow requests without CSRF token (to any user on internet)
    permission_classes = [AllowAny]
    # Allow files on post data and input form data
    parser_classes = [MultiPartParser, FormParser]
    # SerializeR for initial parameters
    serializer_class = TransferSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # Serialize initial parameters to read them as float and not as strings
        serializer = self.serializer_class(data=request.data)
        # Validate that the data recived for initial parameters corresponds to the
        # expected data types (string, float, integer)
        serializer.is_valid(raise_exception=True)
        # Get data as a dic after being serialized
        initial_parameters = serializer.data
        # Transform Querydict into python dict
        data = dict(request.data)
        # Get materials apart from initial parameters
        materials = data.get("materials")
        # Get each initial parameter as an individual variable
        # to call just the name of the variable in the next lines of code
        answer = initial_parameters.get("answer")
        steps = initial_parameters.get("steps")
        polarization = initial_parameters.get("polarization")
        initial_parameter = (
            initial_parameters.get("initialAngle")
            if answer == "angular"
            else initial_parameters.get("initialWaveLength")
        )
        final_parameter = (
            initial_parameters.get("finalAngle")
            if answer == "angular"
            else initial_parameters.get("finalWaveLength")
        )
        fixed_parameter = (
            initial_parameters.get("waveLength")
            if answer == "angular"
            else initial_parameters.get("angle")
        )
        units = initial_parameters.get("units")

        # Initialize list to store n,k values
        refractive_indexes = []
        refractive_indexes_by_material = {}
        # Initialize thicknesses list
        thicknesses = []

        # Initialize volume list
        volumes = []

        # Group materials (create nested dictionaries with the info)
        materials = group_materials(materials)

        # Order materials (Substrate, layers, host)
        materials = order_materials(materials)

        # Iterate over materials to get n, k
        # according to the method selected for each material

        for material in materials:
            # There is just one key per dict (1 material = 1 dict in the list of dicts materials)
            for material_name in material.keys():
                material = material.get(material_name)
                option = material.get("option")
                refractive_indexes_by_material[material_name] = {}

                # Add layer thickness to the vector
                if "thickness" in material:
                    thicknesses.append(float(material.pop("thickness")))

                # MANUAL OPTION
                if option == "manual":
                    n = float(material.get("n"))
                    k = float(material.get("k"))
                    method_result = complex(n, k)

                # DIELECTRIC FUNCTION OPTION: LORENZ
                if option == "lorenz":
                    ne = float(material.get("ne"))
                    wo = float(material.get("wo"))
                    w = float(material.get("w"))
                    r = float(material.get("r"))

                    lorenz_parameters = [ne, wo, w, r]
                    method = DispersionModels(lorenz_parameters)
                    method_result = method.get_lorenz_model()

                # DIELECTRIC FUNCTION OPTION: DRUDE
                if option == "drude":
                    ne = float(material.get("ne"))
                    e = float(material.get("e"))
                    w = float(material.get("w"))
                    r = float(material.get("r"))

                    drude_parameters = [ne, e, w, r]
                    method = DispersionModels(drude_parameters)
                    method_result = method.get_drude_model()

                # DIELECTRIC FUNCTION OPTION: SELLMEIER
                if option == "sellmeier":
                    a = float(material.get("a"))
                    b = float(material.get("b"))
                    lambda_0 = float(material.get("lambdaO"))
                    lambda_f = float(material.get("lambda"))

                    sellmeier_parameters = [a, b, lambda_f, lambda_0]
                    method = DispersionModels(sellmeier_parameters)
                    method_result = method.get_sellmeier_model()

                # DIELECTRIC FUNCTION OPTION: CAUCHY
                if option == "cauchy":
                    a = float(material.get("a"))
                    b = float(material.get("b"))
                    c = float(material.get("c"))
                    lambda_f = float(material.get("lambda"))

                    cauchy_parameters = [a, b, c, lambda_f]
                    method = DispersionModels(cauchy_parameters)
                    method_result = method.get_cauchy_model()

                # EFFECTIVE MEDIUM THEORIES: MAXWELL
                if option == "maxwell":

                    # Dielectric
                    if "e" in material:
                        # Dielectric function selected
                        e1m = float(material["e"]["e1m"])
                        e2m = float(material["e"]["e2m"])
                        comp = complex(e1m, e2m)

                    # File selected
                    elif "file" in material:
                        file_ = material.get("file")
                        comp = process_file(file_, initial_parameters, answer, steps)

                        if isinstance(comp, list):
                            comp = [
                                get_dielectric_funtion_from_nk(val.real, val.imag)
                                for val in comp
                            ]
                        else:
                            comp = get_dielectric_funtion_from_nk(comp.real, comp.imag)

                    # Refractive index selected
                    else:
                        nm = float(material["nk"]["nm"])
                        km = float(material["nk"]["km"])
                        comp = get_dielectric_funtion_from_nk(nm, km)

                    inclusions = get_inclusions(material)
                    e_list_inclusions = []
                    for inclusion in inclusions:
                        # Dielectric function selected
                        if inclusion.get("option") == "e":
                            inclusion_e1m = float(inclusion["e1m"])
                            inclusion_e2m = float(inclusion["e2m"])
                            comp_inclusion = complex(inclusion_e1m, inclusion_e2m)
                            e_list_inclusions.append(comp_inclusion)

                        # File selected
                        elif "file" in inclusion:
                            file_ = inclusion.get("file")
                            comp_inclusion = process_file(
                                file_, initial_parameters, answer, steps
                            )
                            if isinstance(comp_inclusion, list):
                                comp_inclusion = [
                                    get_dielectric_funtion_from_nk(val.real, val.imag)
                                    for val in comp_inclusion
                                ]
                            else:
                                comp_inclusion = get_dielectric_funtion_from_nk(
                                    comp_inclusion.real, comp_inclusion.imag
                                )
                            e_list_inclusions.append(comp_inclusion)

                        # Refractive index selected
                        else:
                            inclusion_nm = float(inclusion["nm"])
                            inclusion_km = float(inclusion["km"])
                            comp_inclusion = get_dielectric_funtion_from_nk(
                                inclusion_nm, inclusion_km
                            )
                            e_list_inclusions.append(comp_inclusion)

                        volume = float(inclusion["volume"])
                        volumes.append(volume)

                    if answer == "angular":
                        method = EfectiveMediumTheories(
                            epsilon_host_mg=comp,
                            volume_fractions_mg=volumes,
                            epsilon_inclusions_mg=e_list_inclusions,
                        )
                        method_result = method.get_maxwell_garnett()
                    else:
                        method_result = []
                        for index in range(len(e_list_inclusions[0])):
                            current_e_inclusions_vector = get_current_vector(
                                e_list_inclusions, index
                            )
                            method = EfectiveMediumTheories(
                                epsilon_host_mg=comp[index],
                                volume_fractions_mg=volumes,
                                epsilon_inclusions_mg=current_e_inclusions_vector,
                            )
                            method_current_result = method.get_maxwell_garnett()
                            method_result.append(method_current_result)

                # EFFECTIVE MEDIUM THEORIES: LORENTZ
                if option == "lorentz":

                    # File selected for em
                    if "em" in material:
                        em = material.get("em")
                        file_ = em.get("file")
                        comp = process_file(file_, initial_parameters, answer, steps)
                        if isinstance(comp, list):
                            comp = [
                                get_dielectric_funtion_from_nk(val.real, val.imag)
                                for val in comp
                            ]
                        else:
                            comp = get_dielectric_funtion_from_nk(comp.real, comp.imag)

                    # Manual dielectric function selected for em
                    if "e-em" in material:
                        eem = material.get("e-em")
                        e1m = eem.get("e1m")
                        e2m = eem.get("e2m")
                        comp = complex(float(e1m), float(e2m))

                    # Manual refractive index selected for em
                    if "nk-em" in material:
                        eem = material.get("nk-em")
                        nm = eem.get("nm")
                        km = eem.get("km")
                        comp = get_dielectric_funtion_from_nk(float(nm), float(km))

                    # File selected for ei
                    if "ei" in material:
                        ei = material.get("ei")
                        volume = float(material.get("volume"))
                        file_ = ei.get("file")
                        comp_inclusion = process_file(
                            file_, initial_parameters, answer, steps
                        )
                        if isinstance(comp_inclusion, list):
                            comp_inclusion = [
                                get_dielectric_funtion_from_nk(val.real, val.imag)
                                for val in comp_inclusion
                            ]
                        else:
                            comp_inclusion = get_dielectric_funtion_from_nk(
                                comp_inclusion.real, comp_inclusion.imag
                            )

                    # Manual selected for ei
                    if "e-ei" in material:
                        eei = material.get("e-ei")
                        e1i = eei.get("e1i")
                        e2i = eei.get("e2i")
                        volume = float(eei.get("volume"))
                        comp_inclusion = complex(float(e1i), float(e2i))

                    if "nk-ei" in material:
                        eei = material.get("nk-ei")
                        ni = eei.get("ni")
                        ki = eei.get("ki")
                        volume = float(eei.get("volume"))
                        comp_inclusion = get_dielectric_funtion_from_nk(
                            float(ni), float(ki)
                        )

                    if answer == "angular":
                        method = EfectiveMediumTheories(
                            epsilon_host_ll=comp,
                            volume_fractions_ll=volume,
                            epsilon_inclusion_ll=comp_inclusion,
                        )
                        method_result = method.get_lorentz_lorenz()
                    else:
                        method_result = []
                        for index in range(len(comp_inclusion)):
                            method = EfectiveMediumTheories(
                                epsilon_host_ll=comp[index],
                                volume_fractions_ll=volume,
                                epsilon_inclusion_ll=comp_inclusion[index],
                            )
                            method_current_result = method.get_lorentz_lorenz()
                            method_result.append(method_current_result)

                # EFFECTIVE MEDIUM THEORIES: BRUGGEMAN
                if option == "bruggeman":

                    e_list_components = []
                    volumes = []

                    for component_name in material.keys():
                        if component_name == "option":
                            continue

                        component = material[component_name]

                        # Dielectric function
                        if component.get("option") == "e":
                            e1i = float(component.get("e1i"))
                            e2i = float(component.get("e2i"))
                            comp = complex(float(e1i), float(e2i))

                        # Refractive index
                        elif component.get("option") == "nk":
                            ni = float(component.get("ni"))
                            ki = float(component.get("ki"))
                            comp = get_dielectric_funtion_from_nk(float(ni), float(ki))

                        # File
                        else:
                            file_ = component.get("file")
                            comp = process_file(
                                file_, initial_parameters, answer, steps
                            )
                            if isinstance(comp, list):
                                comp = [
                                    get_dielectric_funtion_from_nk(val.real, val.imag)
                                    for val in comp
                                ]
                            else:
                                comp = get_dielectric_funtion_from_nk(
                                    comp.real, comp.imag
                                )

                        e_list_components.append(comp)
                        volume = float(component.get("volume"))
                        volumes.append(volume)

                    if answer == "angular":
                        method = EfectiveMediumTheories(
                            volume_fractions_br=volumes,
                            epsilon_components_br=e_list_components,
                        )
                        method_result = method.get_bruggeman()

                    else:
                        method_result = []
                        for index in range(len(e_list_components[0])):

                            current_e_components_vector = get_current_vector(
                                e_list_components, index
                            )
                            method = EfectiveMediumTheories(
                                volume_fractions_br=volumes,
                                epsilon_components_br=current_e_components_vector,
                            )
                            method_current_result = method.get_bruggeman()
                            method_result.append(method_current_result)

                # Reading an InMemoryFile
                if option == "upload-file":
                    # Set material as the uploaded file
                    material = material.get("file")

                    # Get interpolation result from file
                    method_result = process_file(
                        material, initial_parameters, answer, steps
                    )

                # Format data table to 4 decimals
                material_index = method_result
                # Add refractive index to the corresponding material
                if isinstance(material_index, list):
                    material_index = [
                        format_number(number) for number in material_index
                    ]
                else:
                    material_index = format_number(material_index)

                refractive_indexes_by_material[material_name] = str(material_index)

                # Add n,k to the refractive indexes list
                # Angular method always adds a number
                # it is just a list of numbers
                if answer == "angular":
                    refractive_indexes.append(method_result)
                else:
                    # Spectral methods always add a list
                    # it creates a list of lists
                    if isinstance(method_result, list):
                        refractive_indexes.append(method_result)
                    else:
                        refractive_indexes += [method_result]

        # Get values for 'x' axis
        x_range = get_range_list(initial_parameter, final_parameter, steps)

        # Initialize final
        reflectances = []
        transmittances = []
        absortances = []
        # import ipdb; ipdb.set_trace()
        # Calculate 'y' axis values using Transfer Matrix Method
        if answer == "angular":
            for x in x_range:
                method = TransferMatrixMethod(
                    theta=x,
                    l=fixed_parameter,
                    n=refractive_indexes,
                    thicknesses=thicknesses,
                    polarization=polarization.upper(),
                )
                reflectance = method.get_reflectance()
                reflectances.append(reflectance)

                transmittance = method.get_transmittance()
                transmittances.append(transmittance)

                absortance = method.get_absortance()
                absortances.append(absortance)
        else:
            for index in range(len(refractive_indexes[0])):
                current_indexes_vector = get_current_vector(refractive_indexes, index)
                method = TransferMatrixMethod(
                    theta=fixed_parameter,
                    l=x_range[index],
                    n=current_indexes_vector,
                    thicknesses=thicknesses,
                    polarization=polarization.upper(),
                )
                reflectance = method.get_reflectance()
                reflectances.append(reflectance)

                transmittance = method.get_transmittance()
                transmittances.append(transmittance)

                absortance = method.get_absortance()
                absortances.append(absortance)

        # Format data to be just real numbers of float type with 2 decimal places
        data = {
            "reflectance": format_graph_data(reflectances),
            "transmittance": format_graph_data(transmittances),
            "absortance": format_graph_data(absortances),
            "x_range": format_graph_data(x_range),
            "refractive_indexes_by_material": refractive_indexes_by_material,
            "x_table": fixed_parameter,
        }
        # Return a response with the graphics data and a confirmation to the browser about
        # the correct result of the POST request
        return Response(data, status=status.HTTP_200_OK)


class DownloadDataView(APIView):
    """
    View to receive POST data to create the file
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        source = request.data.get("source")
        data = request.data.get("data")
        answer = data.pop("answer")
        graph_type = request.data.get("type")
        response = HttpResponse(content_type="text/csv")
        response = create_file(response, source, data, answer, graph_type=graph_type)
        return response


class CompareExperimentalDataView(APIView):
    """
    View to receive POST with experimental data
    to calculate Chi
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Get data from POST
        answer = request.data.get("answer")
        theorical_reflectance = request.data.get("calculated_reflectance")
        theorical_reflectance = theorical_reflectance.split(",")
        theorical_reflectance = [float(value) for value in theorical_reflectance]
        file_ = request.data.get("file")
        initial_param = float(request.data.get("initial_param"))
        final_param = float(request.data.get("final_param"))
        steps = int(request.data.get("steps"))

        # Read file with experimental data
        x_experimental, experimental_reflectance = get_reflectance_from_file(file_)

        # Calculate chi
        chi, y_experimental = chi_square(
            experimental_reflectance,
            x_experimental,
            theorical_reflectance,
            initial_param,
            final_param,
            steps,
        )

        data = {
            "experimental_reflectance": y_experimental,
            "x_vector": x_experimental,
            "chi": round(chi, 4),
            "filename": file_.name,
        }
        return Response(data, status=status.HTTP_200_OK)
