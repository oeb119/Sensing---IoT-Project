import pandas as pd
import matplotlib.pyplot as plt
import pull_thingspeak_data as pu

def plot_save_name(day, field):

    df = pu.get_prices('2363580', field, 'I0TX348P2XLD2V55')
    dfl = pu.get_prices('2367228', field, '5DMSQSY2KYNGH5ZD')

    field_name = "field{}".format(field)

    # Extract timestamps and field3 values TRAINS
    timestamps = [entry['created_at'] for entry in df]
    prices_tr = [entry[field_name] for entry in df]

    # Extract timestamps and field3 values PLANES
    timestamps_fl = [entry['created_at'] for entry in dfl]
    prices_fl = [entry[field_name] for entry in dfl]

    # Make plot
    plt.figure(figsize=(10, 6))
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
        name = 'plot_dec_{}'.format(day)
        return str(name) + '.png'
    
    plt.savefig(get_plot_name(day))

    # Show the plot
    # plt.show()

    return print(get_plot_name(day))

# plot_save_name(24, 5)