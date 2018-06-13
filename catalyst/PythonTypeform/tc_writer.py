import csv
import sys
import logging
import os
import traceback

logging.basicConfig(filename='C:\SourceFiles\Typeform\logs\Typeform.log',level=logging.INFO)

# Class used to write data out to a file.  It parses through the JSON to get the key value pairs and writes the headers
# and the data to the file as a CSV.
class Writer:

    def write_to_file(self,result,filename):
        try:
            # converts all of the keys in the result object into a list
            keys = list(set().union(*(d.keys() for d in result)))


        except:
            logging.info("Error on keys: " + str(sys.exc_info()[0]))
            print traceback.print_exc()

        with open(filename, 'ab') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            if os.stat(filename).st_size == 0:
                dict_writer.writeheader()
            dict_writer.writerows(result)

        logging.info('Wrote to file: ' + filename)
