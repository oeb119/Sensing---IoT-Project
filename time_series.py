import pandas as pd
import matplotlib.pyplot as plt
import pull_thingspeak_data as pu
import requests
import pandas as pd
import matplotlib.pyplot as plt

### Initializing credentials ###

eu_file = 'trains_13'
fl_file = 'flights_13'
pe_file = 'performance_13'

### Function to get dataframe of ticket prices and times found for requested day ###
### This will be used to make graphs of the data ###

def get_prices(file, field):

    # Specify the path to your CSV file
    path = "./feeds/{}.csv".format(file)
    # Read CSV data into a DataFrame
    df = pd.read_csv(path)

    field_name = "field{}".format(field)

    # Filter out entries where field1 is null
    df = df[df[field_name].notna() & (df[field_name] != '[]')]
    # df = [entry for entry in df["feeds"] if entry.get(field_name) is not None]

    # Convert 'created_at' to datetime format
    def convert_columns(entry):
        entry['created_at'] = pd.to_datetime(entry['created_at'], errors='coerce')
        entry[field_name] = pd.to_numeric(entry[field_name], errors='coerce')
        return entry

    # Apply the conversion function to each row in the DataFrame
    df = df.apply(convert_columns, axis=1)

    return df

def plot_save_name(day, field):

    df = get_prices(eu_file, field)
    dfl = get_prices(fl_file, field)

    field_name = "field{}".format(field)

    # Extract timestamps and field3 values TRAINS
    timestamps = pd.to_datetime(df['created_at'])
    prices_tr = pd.to_numeric(df[field_name], errors='coerce')

    timestamps_fl = pd.to_datetime(dfl['created_at'])
    prices_fl = pd.to_numeric(dfl[field_name], errors='coerce')

    # Make plot
    plt.figure(figsize=(15, 3))
    plt.plot(timestamps, prices_tr, label='Trains', marker='o', linestyle='-', color='b')
    plt.plot(timestamps_fl, prices_fl, label='Planes', marker='o', linestyle='-', color='r')
    
    # # Shading the region when line1 is lower than line2
    # plt.fill_between(timestamps, prices_tr, prices_fl, where=(prices_fl < prices_tr), color='gray', alpha=0.3, label='Shaded Region')

    plt.xlabel('Timestamp')
    plt.ylabel('Price (£)')
    plt.title('Prices in £ Over Time on Dec {}'.format(day))
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    def get_plot_name(day):
        name = './feeds/time_series_dec_{}'.format(day)
        return str(name) + '.png'
    
    plt.savefig(get_plot_name(day))

    # Show the plot
    # plt.show()

    return print(get_plot_name(day))

plot_save_name(20, 1)
plot_save_name(21, 2)
plot_save_name(22, 3)
plot_save_name(23, 4)
plot_save_name(24, 5)
plot_save_name(25, 6)
plot_save_name(26, 7)
plot_save_name(27, 8)

def performance_graph(field, y):

    df = get_prices(pe_file, field)

    field_name = "field{}".format(field)

    # Extract timestamps and field3 values TRAINS
    timestamps = pd.to_datetime(df['created_at'])
    values = pd.to_numeric(df[field_name], errors='coerce')

    # Make plot
    plt.figure(figsize=(15, 3))
    plt.plot(timestamps, values, marker='o', linestyle='-', color='b')
    
    # # Shading the region when line1 is lower than line2
    # plt.fill_between(timestamps, prices_tr, prices_fl, where=(prices_fl < prices_tr), color='gray', alpha=0.3, label='Shaded Region')

    plt.xlabel('Timestamp')
    plt.ylabel(str(y))
    plt.title(str(str(y) + ' Over Time'))
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    def get_plot_name(y):
        name = './feeds/dec_13_{}'.format(y)
        return str(name) + '.png'
    
    plt.savefig(get_plot_name(y))

    # Show the plot
    # plt.show()

    return print(get_plot_name(y))

performance_graph(1, 'Time Mac')
performance_graph(2, 'CPU Pi')
performance_graph(3, 'Internet Download Speed')
performance_graph(4, 'Internet Upload Speed')
performance_graph(5, 'CPU Mac')
performance_graph(6, 'Time Pi')