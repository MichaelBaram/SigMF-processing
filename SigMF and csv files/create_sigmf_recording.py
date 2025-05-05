import datetime as dt
import numpy as np
import csv
import sigmf
from sigmf import SigMFFile
from sigmf.utils import get_data_type_str
from datetime import datetime, timezone
import pytz
import os
#import sys
#print(sys.executable)

#The primary unit of SigMF is a SigMF Recording , which comprises a Metadata file and the Dataset file
#it describes. Collections are an optional feature that are used to describe the relationships between multiple
#Recordings.
#Collections and multiple Recordings can be packaged for easy storage and distribution in a SigMF
#Archive .

#"cf32_le" specifies "complex 32-bit floating-point samples stored in littleendian"
def csv_to_complex_array(csv_file):
    """
    Reads columns 2 and 3 from a CSV file and converts them into a complex NumPy array.
    
    Parameters:
        csv_file (str): Path to the input CSV file.
    
    Returns:
        np.ndarray: Complex NumPy array of type np.complex64.
    """
    real_parts = []
    imag_parts = []
    
    # Open and read the CSV file
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header, if present
        count = 0
        
        for row in reader:
            # Stop once we have processed the required number of samples
            #if count >= num_samples:
            #    break
                
            #print("real part:",float(row[1]))
            #print("Imag part:",float(row[2]))
            # Extract real (column 4) and imaginary (column 5) parts
            real_parts.append(float(row[1]))  # Column 2 (0-indexed)
            imag_parts.append(float(row[2]))  # Column 3 (0-indexed)
            
            count += 1
    
    # Combine real and imaginary parts into a complex array
    complex_array = np.array(real_parts, dtype=np.float32) + 1j * np.array(imag_parts, dtype=np.float32)
    return complex_array.astype(np.complex64)


# np.complex64 uses 64 bits (8 bytes) in total:
# 32 bits (4 bytes) for the real part.
# 32 bits (4 bytes) for the imaginary part.
# Bounds: +- 3.4 x 10^38 (IEEE 754 standard for 32-bit floating-point numbers)

def process_file_with_SigMF(csv_filename_with_extension,gps_lat,gps_lon,gps_alt):
    # Convert CSV to complex array
    complex_array = csv_to_complex_array(csv_filename_with_extension)
    #print("Complex Array:")
    #print(complex_array)
    
    file_name_without_extension = os.path.splitext(csv_filename_with_extension)[0]
    
    # Create the SigMF data file name based on the CSV file name (without extension)
    base_name = file_name_without_extension #os.path.splitext(os.path.basename(csv_file))[0]
    data_file = f'{base_name}.sigmf-data'
    meta_file = f'{base_name}.sigmf-meta'
    
    # Write the complex data to the SigMF data file
    complex_array.tofile(data_file)
    
    # Create the metadata
    meta = SigMFFile(
        data_file=data_file,  # SigMF data file
        global_info = {
            'core:version': '1.0',  # Ensure version is included
            SigMFFile.DATATYPE_KEY: get_data_type_str(complex_array),  # in this case, 'cf32_le'
            SigMFFile.SAMPLE_RATE_KEY: 100000000,
            SigMFFile.AUTHOR_KEY: 'mbaram@nd.edu',
            SigMFFile.DESCRIPTION_KEY: 'Synchronous complex baseband waveforms for SASL algorithm',
            SigMFFile.FREQUENCY_KEY: 5787500000,  # Center frequency in Hz
            SigMFFile.DATETIME_KEY: str(datetime.now(pytz.timezone('US/Eastern')))
        }
    )
    
    # Create a capture key at time index 0
    meta.add_capture(0, metadata={
        'gps:latitude': gps_lat,  # Add GPS latitude
        'gps:longitude': gps_lon,  # Add GPS longitude
        'gps:altitude': gps_alt,  # Add GPS altitude (in meters)
    })

    # Optional: Add annotations for regions of interest
    # meta.add_annotation(0, 1024, metadata={
    #    'comment': 'Entire dataset with GPS metadata.'
    # })
    
    # This means:

    # start=0: The annotation starts at sample index 0.
    # length=1024: The annotation spans 1024 samples.
    # metadata={'comment': 'Entire dataset with GPS metadata.'}:
        # Adds a comment describing the annotation as covering the entire dataset.


    # Write the metadata to a .sigmf-meta file
    meta.tofile(meta_file)
    print(f"SigMF files saved: {data_file}, {meta_file}")
    return

def main():
    # Prompt user for input (only the file name without extension)
    #file_name = input("Enter the name of the CSV file (without extension, e.g., 'example'): ")

    # Add the ".csv" extension to the file name
    
    #csv_file = file_name + ".csv"

    # Get GPS coordinates from user
    #gps_lat = float(input("Enter the GPS latitude (e.g., 37.7749): "))
    #gps_lon = float(input("Enter the GPS longitude (e.g., -122.4194): "))
    #gps_alt = float(input("Enter the GPS altitude (in meters): "))
    gps_lat = 0;
    gps_lon = 0;
    gps_alt = 1.2192 # meters, primary
    
    # Loop through all files in the current directory
    directory = "."
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)  
        
        if os.path.isfile(file_path) and file_path.endswith('.csv'):
            #print(file_path)
            process_file_with_SigMF(file_path,gps_lat,gps_lon,gps_alt)  
                # Only use process_file_with_SigMF with current directory
        



if __name__ == "__main__":
    main()

