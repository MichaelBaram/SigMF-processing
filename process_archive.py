from sigmf import SigMFFile, sigmffile

import zipfile
import os
def unzip_archive(archive_name, output_directory):
    """
    Extracts all files from a ZIP archive to the specified directory.
    
    Parameters:
        archive_name (str): The name of the ZIP archive (with extension).
        output_directory (str): The directory where the files should be extracted.
    
    Returns:
        None
    """
    try:
        # Open the ZIP archive
        with zipfile.ZipFile(archive_name, 'r') as archive:
            # Extract all contents to the specified directory
            archive.extractall(output_directory)
            print(f"Archive extracted to {output_directory}\n")
    
    except Exception as e:
        print(f"An error occurred: {e}\n")




def list_files_without_extension(directory):
    """
    Returns a list of all files in the directory without extensions, removing duplicates.
    
    Parameters:
        directory (str): Path to the directory.
    
    Returns:
        list: List of file names without extensions, without duplicates.
    """
    try:
        # List all files in the directory (excluding directories)
        file_list = [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # Remove duplicates by converting the list to a set and then back to a list
        file_list = list(set(file_list))
        
        return file_list
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' was not found.")
        return []


def read_SigMF_recording(name_of_recording):
    """
    Parameters:
        name_of_recording (str): A SigMF recording, i.e. a file name that 
        corresponds to a .sigmf-data and a .sigmf-meta. For example, "test_sigmf_v3"

    Returns:
        Nothing

    """
    signal = sigmffile.fromfile(name_of_recording)

    # Get some metadata and all annotations
    print("Name of the recording:",name_of_recording)
    sample_rate = signal.get_global_field(SigMFFile.SAMPLE_RATE_KEY)
    print("Sample rate: ",sample_rate)
    print("Data type: ",signal.get_global_field(SigMFFile.DATATYPE_KEY))
    print("Description: ",signal.get_global_field(SigMFFile.DESCRIPTION_KEY))
    print("Center frequency: ",signal.get_global_field(SigMFFile.FREQUENCY_KEY))
    print("Datatype : ",signal.get_global_field(SigMFFile.DATATYPE_KEY))
    print("Time : ",signal.get_global_field(SigMFFile.DATETIME_KEY))
    #gps_latitude = signal.get('capture', [{}])[0].get('gps:latitude', 'Unknown')
    print("Latitude: ",signal.get_captures()[0].get('gps:latitude', 'Unknown'))
    print("Longitude: ",signal.get_captures()[0].get('gps:longitude', 'Unknown'))
    print("Altitude: ",signal.get_captures()[0].get('gps:altitude', 'Unknown'))


    sample_count = signal.sample_count
    print("Number of samples:", sample_count)
    #signal_duration = sample_count / sample_rate
    #annotations = signal.get_annotations()
    data = signal.read_samples()
    print("Data: ", data)
    print("\n")


# Example usage:
archive_name = "Compressed SigMF files.zip" #input("Enter the path to the ZIP archive (with extension): ")
output_directory = "Decompressed SigMF files"#input("Enter the directory to extract the contents to: ")

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)
unzip_archive(archive_name, output_directory)


# Example usage:
directory_path = output_directory
files_without_extension = list_files_without_extension(directory_path)

if files_without_extension:
    print("Processed SigMF recordings: \n")
    for file in files_without_extension:
        read_SigMF_recording(directory_path+"/"+file)
else:
    print("No files found or the directory does not exist.")
