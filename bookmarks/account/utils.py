import csv
import os

# Get list of all administrator accounts
def get_admin_account():
    pass


def store_as_csv(data,filename,dir):

    filename = dir + os.path.sep + filename
    with open(filename, 'w', newline='') as f_handle:
        writer = csv.writer(f_handle)
        for row in data:
            writer.writerow(row)