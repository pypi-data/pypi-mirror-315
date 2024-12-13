"""Module to download weather files from CliDApp API.

:author: J. St.Rose [#]_,
    C.O. Mbengue [#]_,
    A. Popo [#]_

:created on: 2024-02-07

This module contains the following class:

        - :class:`CliDApp4Rhino` - A class to handle weather file downloads from CliDApp API.

This module contains the following functions:
        - :func:`run_command` - Run the command.


.. [#] jstrose@ec-intl.com.
.. [#] cmbengue@ec-intl.com.
.. [#] apopo@ec-intl.com.
"""
import json
import os
import ssl

import Eto.Forms as forms
import Rhino
import urllib2

# Set the command name
__commandname__ = "CliDApp4Rhino"


class CliDApp4Rhino(forms.Dialog):
    """Class to handle weather file downloads from CliDApp API."""

    # Define the epoch ranges
    epoch_ranges = [[1979, 1989], [1990, 2009], [2010, 2023]]

    # Define start and end years
    startyear, endyear = 1979, 2023

    def __init__(self):
        """Initialize the form."""
        self.__path__ = None
        self.__base_url__ = None
        self.__request_url__ = None
        self.Title = "Configure your file for download"
        self.Resizable = False

        self.city_code = forms.Label(Text="Select a city:")
        self.city_dropdown = forms.DropDown()

        # Create an SSL context
        context = ssl._create_unverified_context()

        # Get the response from the url
        web_response = urllib2.urlopen(
            "https://ecodesign.clima.caltech.edu/server/cities", context=context
        )

        # Parse the JSON response
        data = json.load(web_response)

        # Extract the ids list
        ids = data["ids"]

        # Create the dictionary from the ids list
        self.cities = {city.encode("utf-8"): code.encode("utf-8") for code, city in ids}

        # Set the items in the dropdown and sort in alphabetical order
        self.city_dropdown.DataStore = sorted(list(self.cities.keys()))

        self.weatherfile = forms.Label(Text="Select a weather file")
        self.weatherfile_dropdown = forms.DropDown()

        with open(
            os.path.join(os.path.dirname(__file__), "inputs", "weather_files.json")
        ) as f:
            self.weather_files = json.load(f)

        self.weatherfile_dropdown.DataStore = list(self.weather_files.keys())
        self.weatherfile_dropdown.SelectedIndexChanged += (
            self.OnStartYearWeatherFileChanged
        )

        self.datatype_label = forms.Label(Text="Select Data Type:")
        self.datatype_dropdown = forms.DropDown()
        self.datatype_dropdown.DataStore = ["OBSERVATIONS"]
        self.datatype_map = {"OBSERVATIONS": "obs"}

        # Set the start year label and dropdown
        self.start_year_label = forms.Label(Text="Select Start Year:")
        self.start_year_dropdown = forms.DropDown()
        self.start_year_dropdown.DataStore = list(
            range(self.startyear, self.endyear + 1)
        )

        self.start_year_dropdown.SelectedIndexChanged += (
            self.OnStartYearWeatherFileChanged
        )

        # Set the end year label and dropdown
        self.end_year_label = forms.Label(Text="Select End Year:")
        self.end_year_dropdown = forms.DropDown()

        # Set the file type label and dropdown
        self.file_type_label = forms.Label(Text="Select file type:")
        self.file_type_dropdown = forms.DropDown()
        # Load dictionary of file types from json file
        with open(
            os.path.join(os.path.dirname(__file__), "inputs", "filetype_map.json"), "r"
        ) as f:
            self.file_type_map = json.load(f)
        # Set the DataStore to the display names
        self.file_type_dropdown.DataStore = self.file_type_map.keys()

        # Set the download path label and text box
        self.download_path_label = forms.Label(Text="Download Path (Absolute Path):")
        self.download_path_textbox = forms.TextBox()

        self.ok_button = forms.Button(Text="OK")
        self.ok_button.Click += self.OnOKButtonClick

        layout = forms.DynamicLayout()
        layout.AddRow(self.city_code, self.city_dropdown)
        layout.AddRow(self.weatherfile, self.weatherfile_dropdown)
        layout.AddRow(self.datatype_label, self.datatype_dropdown)
        layout.AddRow(self.start_year_label, self.start_year_dropdown)
        layout.AddRow(self.end_year_label, self.end_year_dropdown)
        layout.AddRow(self.file_type_label, self.file_type_dropdown)
        layout.AddRow(self.download_path_label, self.download_path_textbox)
        layout.AddRow(None, self.ok_button)

        self.Content = layout

    def OnStartYearWeatherFileChanged(self, sender, e):
        """Update the end year dropdown when the start year or weatherfile is changed.

        :param forms.DropDown sender: The dropdown that triggered the event.
        :param forms.EventArgs e: The event arguments.
        """
        # Get the selected start year
        sel_start_yr = self.start_year_dropdown.SelectedValue

        if sel_start_yr is not None:
            # Set the end year to the selected start year for the 'AMY'
            if self.weatherfile_dropdown.SelectedValue == "AMY":
                self.end_year_dropdown.DataStore = [sel_start_yr]

            # Set the end year to the next epoch for the 'FTMY'
            elif self.weatherfile_dropdown.SelectedValue == "FTMY":
                # Find the end bound for the selected start year
                end_bound = next(
                    (
                        end
                        for start, end in self.epoch_ranges
                        if start <= sel_start_yr <= end
                    ),
                    self.epoch_ranges[-1][-1],
                )
                self.end_year_dropdown.DataStore = list(
                    range(sel_start_yr + 1, end_bound + 1)
                )

            else:
                # Set the end year to the maximum year for other weather files
                self.end_year_dropdown.DataStore = list(
                    range(sel_start_yr, self.endyear + 1)
                )

    def OnOKButtonClick(self, sender, e):
        self.download_file()
        self.Close()

    def __get_path__(self):
        """Create the default path for the directory to save the file.

        **Implementation**

        Set path as a string.
        """
        # Set the directory to save the file
        selected_file_type = self.file_type_dropdown.SelectedValue
        dir_path = self.download_path_textbox.Text or os.path.join(
            os.path.expanduser("~"), "Downloads", "clidapp", selected_file_type
        )

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        self.__path__ = dir_path

    def __get_base_url__(self):
        """Create the base url for the CliDApp web app and save as base_url.

        **Implementation**

        Save base_url as a string.
        """
        self.__base_url__ = "https://ecodesign.clima.caltech.edu/server/"

    def construct_request_url(self):
        """Construct the request URL based on the selected values.

        **Implementation**

        Get the selected values for the city, weather file, start year, end year, and file type.
        Construct the request URL using the selected values.
        """
        # Get the selected values
        city_code = self.cities[self.city_dropdown.SelectedValue]
        weatherfile = self.weather_files[self.weatherfile_dropdown.SelectedValue]
        datatype = self.datatype_map[self.datatype_dropdown.SelectedValue]
        start_year = self.start_year_dropdown.SelectedValue
        end_year = self.end_year_dropdown.SelectedValue
        file_type = self.file_type_map[self.file_type_dropdown.SelectedValue]
        self.__get_base_url__()

        # Construct request url
        request_url = "{}{}/{}/{}/{}/{}/{}".format(
            self.__base_url__,
            city_code,
            weatherfile,
            datatype,
            start_year,
            end_year,
            file_type,
        )
        self.__request_url__ = request_url

    def download_file(self):
        """Download the file from the request URL and save it to the specified path.

        **Implementation**

        Construct the request URL.
        Get the download path.
        Extract the file name from the URL.
        Append the file name to the download path.
        Use urllib2 to download the file.
        """
        # Create the default path for the directory to save the file

        # Construct the request URL
        self.construct_request_url()

        # Get the download path
        path = self.download_path_textbox.Text
        if not path:
            # If no download path is specified, use the default path
            self.__get_path__()
            path = self.__path__

        # Extract the file name from the URL
        url_parts = self.__request_url__.split("/")
        # Join the last 5 parts of the URL with '-' and add '.' before the file extension
        file_name_fields = url_parts[-6:-4] + url_parts[-3:-1]
        file_name = "-".join(file_name_fields) + "." + url_parts[-1]

        # Append the file name to the download path
        full_path = os.path.join(path, file_name)

        # Use urllib2 to download the file
        try:
            response = urllib2.urlopen(self.__request_url__)
            # Open the file and write the response to it
            with open(full_path, "wb") as out_file:
                out_file.write(response.read())
            print("Full Path: %s" % full_path)
        except urllib2.HTTPError as e:
            print(
                "The file requested is currently unavailable for download, HTTP Error: %s"
                % e.code
            )


def RunCommand(is_interactive):
    form = CliDApp4Rhino()
    form.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


if __name__ == "__main__":
    RunCommand(True)
