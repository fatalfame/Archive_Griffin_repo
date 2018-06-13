# import datetime
# import numbers
# from dateutil.parser import parse

# This class is really just to format dates to fit the datetime2 format for SQL Server
class DataFormatter:

# If it can't format the data as a date, it is not a date and the data is sent back untouched.
    def format_date_for_load(self,unformatted_date):
        try:
            unformatted_date = unformatted_date.replace('+0000','')
            formatted_date = datetime.datetime.strptime(unformatted_date, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')
            return formatted_date
        except:
            return unformatted_date

    def format_data(self,unformatted_data):
        final_data2 = []
        complete_data = []
        final_dict = {}
        for i in range(len(unformatted_data)):
            data = unformatted_data[i]
            for key, value in data.items():
                final_dict[key] = self.format_date_for_load(value)
            final_data2 = dict(final_dict.items())
            complete_data.append(final_data2)
        return complete_data
