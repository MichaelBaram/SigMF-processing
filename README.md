# SigMF-processing
A repository of python scripts to create and process SigMF files.


To create a SigMF archive, please follow the instructions below.

1.  Clone this directory, unzip it and paste a csv file correponding to one "capture" to the folder named "SigMF and csv files". Then run the script "create_sigmf_recording.py" and enter the file information (name of the csv file and the coordinates of the sensor). This script creates a pair of SigMF data and meta (which is called a SigMF recording) with the same name as the csv file. Repeat this process every time a new csv file is generated. Please note that other information such as the carrier frequency, current time and the sample rate are also saved in the created SigMF recording.
2.  Run the python script called "create_archive.py". This python script will create an archive named "Compressed SigMF files" containing all the SigMF files in the "SigMF and csv files" folder.

To process a SigMF archive,

3. Please first ensure that an archive called "Compressed SigMF files" lies in the current directory, then run the script named "process_archive.py". This script decompresses the archive to a new folder called "Decompressed SigMF files", loops through all the SigMF recordings in it and displays the data and meta data associated with each of them.
