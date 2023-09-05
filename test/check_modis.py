from pyhdf import SD

# Open the HDF4 file
file_path = 'data\MOD11A2\MOD11A2.A2023169.h27v06.061.2023178033326.hdf'
hdf_file = SD.SD(file_path)

# Access the temperature dataset
temperature_dataset_name = 'Emis_31'
temperature_dataset = hdf_file.select(temperature_dataset_name)

# Read the temperature data into a variable
temperature_data = temperature_dataset.get()

# Close the HDF4 file
hdf_file.end()

# Print the temperature data
print(temperature_data)
