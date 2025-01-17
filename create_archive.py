
from sigmf import SigMFFile, sigmffile

import sigmf as smf




import datetime as dt
import numpy as np
import os
import sigmf
from sigmf import SigMFFile
from sigmf.utils import get_data_type_str
import zipfile

import os


def create_sigmf_archive(directory, archive_name):
    """
    Creates a ZIP archive containing all SIGMF files in the specified directory.
    
    Parameters:
        directory (str): The path to the directory containing SIGMF files.
        archive_name (str): The name for the ZIP archive (without extension).
        
    Returns:
        None
    """
    try:
        # Create a zip file
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_STORED) as archive:
            # Walk through the directory and add all SIGMF files
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.sigmf-data') or file.endswith('.sigmf-meta'):
                        # Add each SIGMF file to the archive
                        file_path = os.path.join(root, file)
                        archive.write(file_path, os.path.relpath(file_path, directory))
                        print(f"Adding {file_path} to archive.")
        
        print(f"Archive created successfully: {archive_name}")
    
    except Exception as e:
        print(f"An error occurred: {e}")




# Example usage:
directory_path = "SigMF and csv files";#input("Enter the directory path: ")
archive_name = "Compressed SigMF files"
create_sigmf_archive(directory_path, f"{archive_name}.zip")

