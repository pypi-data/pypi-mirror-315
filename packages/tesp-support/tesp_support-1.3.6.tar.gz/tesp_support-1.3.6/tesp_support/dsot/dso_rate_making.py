# Copyright (C) 2021-2024 Battelle Memorial Institute
# See LICENSE file at https://github.com/pnnl/tesp
# file: DSO_rate_making.py
"""
@author: reev057
"""
import json
import os
import sys
from os.path import dirname, abspath

import numpy as np
import pandas as pd

# sys.path.insert(0, dirname(abspath(__file__)))

from .plots import load_da_retail_price, customer_meta_data, load_json, load_agent_data, \
    load_system_data, get_date, tic, toc, load_retail_data, load_ames_data, load_gen_data, load_indust_data


def read_meters(metadata, dir_path, folder_prefix, dso_num,
                day_range, SF, dso_data_path, rate_scenario=None):
    """ Determines the total energy consumed and max power consumption for all meters within a
    DSO for a series of days. Also collects information on day ahead and real time quantities
    consumed by transactive customers. Creates summation of these statistics by customer class.
    Args:
        metadata (dict): metadata structure for the DSO to be analyzed
        dir_path (str): directory path for the case to be analyzed
        folder_prefix (str): prefix of GLD folder name (e.g. '\TE_base_s')
        dso_num (str): number of the DSO folder to be opened
        day_range (list): range of days to be summed (for example a month).
        SF (float): Scaling factor to scale GLD results to TSO scale (e.g. 1743)
        dso_data_path (str): A str specifying the directory in which the time-of-use rate
        rate_scenario (str): A str specifying the rate scenario under investigation (e.g.
        flat, time-of-use or TOU, subscription, or transactive), defaults to None.
    Returns:
        meter_df: dataframe of energy consumption and max 15 minute power consumption for each month and total
        energysum_df: dataframe of energy consumption summations by customer class (residential, commercial, and industrial)
        saves the two dataframe above to an h5 file in the dir_path
        """

    # Load in bulk industrial loads
    case_config = load_json(dir_path, 'generate_case_config.json')
    industrial_file = os.path.join("../" + dso_data_path, case_config['indLoad'][5].split('/')[-1])
    indust_df = load_indust_data(industrial_file, day_range)

    # Load in necessary data for the defined rate scenario
    if (rate_scenario in ["time-of-use", "TOU"]):
        # Load time-of-use rate parameters
        tou_params = load_json(os.path.join("../" + dso_data_path), "time_of_use_parameters.json")

        # Create a mapping between month number and month abbreviation
        month_num_to_abbrev = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec",
        }

        # Identify the month name
        month_name = month_num_to_abbrev[
            get_date(dir_path, dso_num, day_range[0]).month
        ]

    # Create empty dataframe structure for all meters.
    meter = []
    variable = []
    month = []

    fixed_variable_list = ['kw-hr', 'max_kw', 'avg_load', 'load_factor']
    for each in metadata['billingmeters']:
        for var in fixed_variable_list:
            meter.append(each)
            variable.append(var)
            month.append(0)

        # Add consumption during time-of-use periods, if applicable
        if rate_scenario in ["time-of-use", "TOU"]:
            for k in tou_params["DSO_" + dso_num][month_name]["periods"].keys():
                meter.append(each)
                variable.append(k + "_kwh")
                month.append(0)

    meter_df = pd.DataFrame(month,
                            index=[meter, variable],
                            columns=['sum'])

    # Create dataframe for transactive customer data.
    trans = []
    variable = []
    month = []

    dynamic_variable_list = ['DA_Q', 'DA_cost', 'RT_Q', 'RT_cost', 'Congestion_Q', 'Congestion_cost']
    if rate_scenario == "transactive":
        dynamic_variable_list.append("DA_capacity_charge")
        dynamic_variable_list.append("RT_capacity_charge")
    for each in metadata['billingmeters']:
        # if metadata['billingmeters'][each]['cust_participating']:
        for var in dynamic_variable_list:
            trans.append(each)
            variable.append(var)
            month.append(0)
    for var in dynamic_variable_list:
        trans.append('Industrial')
        variable.append(var)
        month.append(0)

    trans_df = pd.DataFrame(month,
                            index=[trans, variable],
                            columns=['sum'])

    # Create empty dataframe structure for total energy summation
    month = []
    variable = []
    loads = []
    loadtype = ['residential', 'commercial', 'industrial', 'total']
    load_list = ['kw-hr', 'demand_quantity', 'da_q', 'rt_q', 'congest_$', 'congest_q']

    for each in loadtype:
        for var in load_list:
            loads.append(each)
            variable.append(var)
            month.append(0)
        if each == 'total':
            loads.append(each)
            variable.append('dist_loss_$')
            month.append(0)
            loads.append(each)
            variable.append('dist_loss_q')
            month.append(0)
        
        # Add consumtpion during time-of-use periods, if applicable
        if rate_scenario in ["time-of-use", "TOU"]:
            for k in tou_params["DSO_" + dso_num][month_name]["periods"].keys():
                loads.append(each)
                variable.append(k + "_kwh")
                month.append(0)

    energysum_df = pd.DataFrame(month,
                                index=[loads, variable],
                                columns=['sum'])

    # load meter data for each day
    for day in day_range:
        # Label columns of data frame by actual calendar date (not simulation day)
        date = get_date(dir_path, dso_num, str(day))
        day_name = date.strftime("%m-%d")
        meter_df[day_name] = [0] * len(meter_df)
        trans_df[day_name] = [0] * len(trans_df)
        energysum_df[day_name] = [0] * len(energysum_df)

        # Load in transactive customer Q data, real-time price data, and DA cleared price
        filename = dir_path + '/DSO_' + dso_num + '/Retail_Quantities.h5'
        cust_trans_df = pd.read_hdf(filename, key='/index' + str(day), mode='r')
        # DSO agent retail values are used for congestion and AMES price LMPs used for quantity billing.
        RT_price_df = load_ames_data(dir_path, range(int(day), int(day) + 1))
        RT_retail_df, RT_bid_df = load_agent_data(dir_path, '/DSO_', dso_num, str(day), 'retail_market')
        RT_retail_df = RT_retail_df.droplevel(level=1)
        DA_price_df = load_gen_data(dir_path, 'da_lmp', range(int(day), int(day) + 1))
        DA_price_df = DA_price_df.unstack(level=1)
        DA_price_df.columns = DA_price_df.columns.droplevel()
        DA_retail_df = load_da_retail_price(dir_path, '/DSO_', dso_num, str(day))
        # Load meter data
        substation_meta_df, substation_data_df = load_system_data(dir_path, folder_prefix, dso_num, str(day), 'substation')
        substation_data_df = substation_data_df.set_index(['time'])

        meter_meta_df, meter_data_df = load_system_data(dir_path, folder_prefix, dso_num, str(day), 'billing_meter')
        meter_data_df['date'] = meter_data_df['date'].str.replace('CDT', '', regex=True)
        meter_data_df['date'] = meter_data_df['date'].str.replace('CST', '', regex=True)
        meter_data_df['date'] = pd.to_datetime(meter_data_df['date'])  #, infer_datetime_format=True)
        meter_data_df = meter_data_df.set_index(['time', 'name'])
        RThourprice = RT_price_df[' LMP' + dso_num].resample('h').mean() / 1000
        RThourcongestionprice = RT_retail_df['congestion_surcharge_RT'].resample('h').mean() / 1000
        RThourcleartype = RT_retail_df['clear_type_rt'].resample('h').mean() / 1000
        for each in metadata['billingmeters']:
            # Calculate standard customer energy consumption metrics used for all customers (including baseline)
            # temp = meter_data_df[meter_data_df['name'].str.contains(each)]
            temp = meter_data_df.xs(each, level=1)[['real_power_avg', 'date']]
            meter_df.loc[(each, 'kw-hr'), day_name] = temp.loc[:, 'real_power_avg'].sum() / 1000 / 12
            meter_df.loc[(each, 'avg_load'), day_name] = temp.loc[:, 'real_power_avg'].mean() / 1000
            # TODO: changed from fixed window to moving window.  Need to check if this is OK.
            # find average max power over a 15 minute moving window (=3 * 5 minute intervals).
            windowsize = 3
            max_kw = temp['real_power_avg'].rolling(window=windowsize).mean().max() / 1000
            meter_df.loc[(each, 'max_kw'), day_name] = max(meter_df.loc[(each, 'max_kw'), day_name], max_kw)
            if meter_df.loc[(each, 'max_kw'), day_name] != 0:
                meter_df.loc[(each, 'load_factor'), day_name] = meter_df.loc[(each, 'avg_load'), day_name] / \
                                                                meter_df.loc[(each, 'max_kw'), day_name]
            else:
                meter_df.loc[(each, 'load_factor'), day_name] = 0
            
            # Calculate each consumer's time-of-use-related consumption metrics, if applicable
            if rate_scenario in ["time-of-use", "TOU"]:
                for k in tou_params["DSO_" + dso_num][month_name]["periods"].keys():
                    for t in range(len(tou_params["DSO_" + dso_num][month_name]["periods"][k]["hour_start"])):
                        meter_df.loc[(each, k + "_kwh"), day_name] += (
                            temp.loc[
                                (300 * 12 * (24 * (day - 1)
                                        + tou_params["DSO_" + dso_num][month_name]["periods"][k]["hour_start"][t]
                                    )):
                                (300 * 12 * (24 * (day - 1)
                                        + tou_params["DSO_" + dso_num][month_name]["periods"][k]["hour_end"][t]
                                    ) - 1),
                                "real_power_avg",
                            ].sum()
                            / 1000
                            / 12
                        )
                        if tou_params["DSO_" + dso_num][month_name]["periods"][k]["hour_start"][t] == 0:
                            meter_df.loc[(each, k + "_kwh"), day_name] += (
                                temp.loc[300 * 12 * 24 * day, "real_power_avg"]
                                / 1000
                                / 12
                            )

            # Calculate transactive customer energy consumption metrics
            temp2 = cust_trans_df[cust_trans_df.meter == each]
            trans_df.loc[(each, 'DA_Q'), day_name] = temp2.loc[:, 'total_cleared_quantity'].sum()
            trans_df.loc[(each, 'RT_Q'), day_name] = meter_df.loc[(each, 'kw-hr'), day_name] - \
                                                     trans_df.loc[(each, 'DA_Q'), day_name]
            # TODO:  Need to interpolate day ahead Q to make RT summation every
            #  5 minutes rather than one hour average
            RTonehour = temp.set_index('date').resample('h').mean() / 1000
            trans_df.loc[(each, 'DA_cost'), day_name] = (temp2['total_cleared_quantity'] *
                                                         DA_price_df['da_lmp' + dso_num] / 1000).sum()
            Real_time_purchase = (RTonehour['real_power_avg'] - temp2['total_cleared_quantity']) * RThourprice
            trans_df.loc[(each, 'RT_cost'), day_name] = Real_time_purchase.sum()
            #  Calculate Congestion Quantities and costs for each customer
            trans_df.loc[(each, 'Congestion_cost'), day_name] = (temp2['total_cleared_quantity'] *
                                                                 DA_retail_df['congestion_surcharge_DA']).sum() + \
                                                                ((RTonehour['real_power_avg'] - temp2[
                                                                    'total_cleared_quantity']) * RThourcongestionprice).sum()
            # TODO: Need to check or verify that clear_type is never 2 or 3 (inefficient or failure)...
            trans_df.loc[(each, 'Congestion_Q'), day_name] = (temp2['total_cleared_quantity'] *
                                                              DA_retail_df['clear_type_da']).sum() + \
                                                             ((RTonehour['real_power_avg'] - temp2[
                                                                 'total_cleared_quantity']) * RThourcleartype).sum()

            # Calculate the transactive capacity charge components, if applicable
            # TODO: Incorporate dynamic capital costs, likely following a similar 
            # format to that implemented for the DA and RT energy charges
            """
            if rate_scenario == "transactive":
                trans_df.loc[(each, "DA_capacity_charge"), day_name] = 0
                trans_df.loc[(each, "RT_capacity_charge"), day_name] = 0
            """

        # Calculate total energy consumption for each customer class (aka load type)
        for each in metadata['billingmeters']:
            for load in loadtype:
                if metadata['billingmeters'][each]['tariff_class'] == load:
                    energysum_df.loc[(load, 'kw-hr'), day_name] += meter_df.loc[(each, 'kw-hr'), day_name] * SF
                    if metadata['billingmeters'][each]['cust_participating']:
                        energysum_df.loc[(load, 'da_q'), day_name] += trans_df.loc[(each, 'DA_Q'), day_name] * SF
                        energysum_df.loc[(load, 'rt_q'), day_name] += trans_df.loc[(each, 'RT_Q'), day_name] * SF
                        energysum_df.loc[(load, 'congest_$'), day_name] += trans_df.loc[
                                                                               (each, 'Congestion_Q'), day_name] * SF
                        energysum_df.loc[(load, 'congest_q'), day_name] += trans_df.loc[
                                                                               (each, 'Congestion_cost'), day_name] * SF
                    else:
                        energysum_df.loc[(load, 'demand_quantity'), day_name] += meter_df.loc[
                                                                                     (each, 'max_kw'), day_name] * SF
                    
                    # Calculate the time-of-use-related metrics, if applicable
                    if rate_scenario in ["time-of-use", "TOU"]:
                        for k in tou_params["DSO_" + dso_num][month_name]["periods"].keys():
                            energysum_df.loc[(load, k + "_kwh"), day_name] += (
                                meter_df.loc[(each, k + "_kwh"), day_name] * SF
                            )

        # Break the streetlights out into a separate category for reporting and verification purposes
        # energysum_df.loc[('street_lights', 'kw-hr'), :] = energysum_df.loc[('industrial', 'kw-hr'), :]
        # energysum_df.loc[('street_lights', 'max_kw'), :] = energysum_df.loc[('industrial', 'max_kw'), :]

        # Load in bulk industrial load for day in question:
        start_time = (day - 1) * 300 * 288
        end_time = start_time + 300 * 287
        # TODO: Need to verify MW-kW conversion?
        energysum_df.loc[('industrial', 'kw-hr'), day_name] += \
            indust_df.loc[start_time:end_time, 'Bus' + dso_num].sum() / 12 * 1000
        energysum_df.loc[('industrial', 'demand_quantity'), day_name] += \
            indust_df.loc[start_time:end_time, 'Bus' + dso_num].rolling(window=windowsize).mean().max() * 1000
        dso_losses = (substation_data_df['real_power_avg'] - meter_data_df['real_power_avg'].
                      groupby(level=0).sum()) / 1000 / 12 * SF
        energysum_df.loc[('total', 'dist_loss_$'), day_name] += (
                    dso_losses * RT_price_df[' LMP' + dso_num].values / 1000).sum()
        energysum_df.loc[('total', 'dist_loss_q'), day_name] += dso_losses.sum()

        # Calculate the time-of-use-related metrics, if applicable
        if rate_scenario in ["time-of-use", "TOU"]:
            for k in tou_params["DSO_" + dso_num][month_name]["periods"].keys():
                num_hours = 0
                for i in range(
                        len(tou_params["DSO_" + dso_num][month_name]["periods"][k]["hour_start"])):
                    num_hours += (
                        tou_params["DSO_" + dso_num][month_name]["periods"][k]["hour_end"][i]
                        - tou_params["DSO_" + dso_num][month_name]["periods"][k]["hour_start"][i]
                    )
                energysum_df.loc[("industrial", k + "_kwh"), day_name] += (
                    indust_df.loc[start_time:end_time, "Bus" + dso_num].sum()
                    / 12 * 1000 * num_hours / 24
                )

    # Create totals for energy metrics
    energysum_metrics = ['kw-hr', 'demand_quantity', 'da_q', 'rt_q', 'congest_$', 'congest_q']
    if rate_scenario in ["time-of-use", "TOU"]:
        for k in tou_params["DSO_" + dso_num][month_name]["periods"].keys():
            energysum_metrics.append(k + "_kwh")
    for item in energysum_metrics:
        for load in ['residential', 'commercial', 'industrial']:
            energysum_df.loc[('total', item), :] += energysum_df.loc[(load, item), :]

    # Sum the total power consumption for all days
    meter_df.loc[(slice(None), 'kw-hr'), ['sum']] = \
        meter_df.loc[(slice(None), 'kw-hr'), meter_df.columns[~meter_df.columns.isin(['sum'])]].sum(axis=1)
    meter_df.loc[(slice(None), 'max_kw'), ['sum']] = \
        meter_df.loc[(slice(None), 'max_kw'), meter_df.columns[~meter_df.columns.isin(['sum'])]].max(axis=1)
    meter_df.loc[(slice(None), 'avg_load'), ['sum']] = \
        meter_df.loc[(slice(None), 'avg_load'), meter_df.columns[~meter_df.columns.isin(['sum'])]].mean(axis=1)

    for each in metadata['billingmeters']:
        if meter_df.loc[(each, 'max_kw'), 'sum'] != 0:
            meter_df.loc[(each, 'load_factor'), 'sum'] = meter_df.loc[(each, 'avg_load'), 'sum'] / \
                                                         meter_df.loc[(each, 'max_kw'), 'sum']
        else:
            meter_df.loc[(each, 'load_factor'), 'sum'] = 0
    
    if rate_scenario in ["time-of-use", "TOU"]:
        for k in tou_params["DSO_" + dso_num][month_name]["periods"].keys():
            meter_df.loc[(slice(None), k + "_kwh"), ["sum"]] = meter_df.loc[
                (slice(None), k + "_kwh"),
                meter_df.columns[~meter_df.columns.isin(["sum"])],
            ].sum(axis=1)

    trans_df.loc[:, ['sum']] = \
        trans_df.loc[:, trans_df.columns[~trans_df.columns.str.contains('sum')]].sum(axis=1)

    # Sum all days to create total for the month.
    energysum_df['sum'] = \
        energysum_df.loc[:, meter_df.columns[~meter_df.columns.str.contains('sum')]].sum(axis=1)
    # Need to correct demand quantity to be the max for the month and not the sum of each day of the month.
    energysum_df.loc[(slice(None), 'demand_quantity'), ['sum']] = \
        energysum_df.loc[(slice(None), 'demand_quantity'),
                         energysum_df.columns[~energysum_df.columns.str.contains('sum')]].max(axis=1)
    # Save summary data to h5 file in folder where meter data came from (dir_path)
    # os.chdir(dir_path + folder_prefix + dso_num)
    save_path = dir_path + folder_prefix + dso_num
    meter_df.to_hdf(save_path + '/energy_metrics_data.h5', key='energy_data')
    energysum_df.to_hdf(save_path + '/energy_metrics_data.h5', key='energy_sums')
    trans_df.to_hdf(save_path + '/transactive_metrics_data.h5', key='trans_data')

    return meter_df, energysum_df


def annual_energy(month_list, folder_prefix, dso_num, metadata):
    """ Creates a dataframe of monthly energy consumption values and annual sum based on monthly h5 files.
    Args:
        month_list (list): list of lists.  Each sub list has month name (str), directory path (str)
        folder_prefix (str): prefix of GLD folder name (e.g. '/TE_base_s')
        dso_num (str): number of the DSO folder to be opened
        metadata (dict): metadata of GridLAB-D model entities
    Returns:
        year_meter_df: dataframe of energy consumption and max 15 minute power consumption for each month and total
        year_energysum_df: dataframe of energy consumption summations by customer class (res., commercial, and indust)
        """

    for i in range(len(month_list)):
        filename = (month_list[i][1] + folder_prefix + dso_num + '/energy_metrics_data.h5')
        trans_file = (month_list[i][1] + folder_prefix + dso_num + '/transactive_metrics_data.h5')
        meter_df = pd.read_hdf(filename, key='energy_data', mode='r')
        energysum_df = pd.read_hdf(filename, key='energy_sums', mode='r')
        trans_df = pd.read_hdf(trans_file, key='trans_data', mode='r')

        if i == 0:
            year_meter_df = meter_df[['sum']]
            year_meter_df = year_meter_df.rename(columns={'sum': month_list[i][0]})
            year_energysum_df = energysum_df[['sum']]
            year_energysum_df = year_energysum_df.rename(columns={'sum': month_list[i][0]})
            year_trans_sum_df = trans_df[['sum']]
            year_trans_sum_df = year_trans_sum_df.rename(columns={'sum': month_list[i][0]})
        else:
            year_meter_df[month_list[i][0]] = meter_df[['sum']]
            year_energysum_df[month_list[i][0]] = energysum_df[['sum']]
            year_trans_sum_df[month_list[i][0]] = trans_df[['sum']]

    year_meter_df['sum'] = year_meter_df.sum(axis=1)
    year_energysum_df['sum'] = year_energysum_df.sum(axis=1)
    year_trans_sum_df['sum'] = year_trans_sum_df.sum(axis=1)

    year_meter_df.loc[(slice(None), 'max_kw'), ['sum']] = \
        year_meter_df.loc[(slice(None), 'max_kw'),
                          year_meter_df.columns[~year_meter_df.columns.str.contains('sum')]].max(axis=1)
    year_meter_df.loc[(slice(None), 'avg_load'), ['sum']] = \
        year_meter_df.loc[(slice(None), 'avg_load'),
                          year_meter_df.columns[~year_meter_df.columns.str.contains('sum')]].mean(axis=1)
    for each in metadata['billingmeters']:
        if year_meter_df.loc[(each, 'max_kw'), 'sum'] != 0:
            year_meter_df.loc[(each, 'load_factor'), 'sum'] = \
                year_meter_df.loc[(each, 'avg_load'), 'sum'] / year_meter_df.loc[(each, 'max_kw'), 'sum']
        else:
            year_meter_df.loc[(each, 'load_factor'), 'sum'] = 0

    return year_meter_df, year_energysum_df, year_trans_sum_df


def create_demand_profiles_for_each_meter(
    dir_path,
    dso_num,
    day_range,
    save=False,
):
    """Creates a pandas DataFrame that contains hourly time-series data for each meter 
    in a DSO. The resultant DataFrame can be saved to a .h5 file if desired.
    Arguments:
        dir_path (str): Contains file path of daily power and voltage information for 
        each meter in five-minute time steps.
        dso_num (int): The number of a valid substation in the system model.
        day_range (list): List of day numbers in a month to be considered.
        save (bool): Indicates whether the output data should be saved in a .h5
        file. If True, data is saved to the same location as what is provided in 
        'dir_path'.
    Returns:
        demand_df (pandas.DataFrame): Monthly hourly demand data for each meter.
    """
    # Iterate through the days to access the demand data
    demand_dict = {}
    for day in day_range:
        # Load the meter data from the specified day
        _, meter_data_df = load_system_data(
            dir_path, "/Substation_", str(dso_num), str(day), "billing_meter"
        )
        meter_data_df["date"] = meter_data_df["date"].str.replace("CST", "", regex=True)
        meter_data_df["date"] = meter_data_df["date"].str.replace("CDT", "", regex=True)
        meter_data_df["date"] = pd.to_datetime(meter_data_df["date"])
        meter_data_df = meter_data_df.set_index(["time", "name"])

        # Identify the start and end indices, for use in the DataFrame
        if day == day_range[0]:
            start_index = meter_data_df["date"].iloc[0].date()
        if day == day_range[-1]:
            end_index = meter_data_df["date"].iloc[-1].date()

        # Distribute demand data from meter_data_df to demand_df
        for meter in meter_data_df.index.get_level_values("name").unique():
            if day == day_range[0]:
                demand_dict[meter] = list(
                    meter_data_df.loc[
                        meter_data_df.index.get_level_values("name") == meter,
                        "real_power_avg",
                    ].values
                )
            else:
                demand_dict[meter].extend(
                    list(
                        meter_data_df.loc[
                            meter_data_df.index.get_level_values("name") == meter,
                            "real_power_avg",
                        ].values
                    )
                )

    # Identify the timestamp index that will be used in the time-series demand DataFrame
    index = pd.date_range(
        start=start_index,
        end=end_index,
        freq="5min",
        inclusive="left",
    )
    # For some reason had another day in November
    if not (len(index) == len(demand_dict[meter])):
        index = pd.date_range(
            start=start_index,
            end=(end_index + pd.Timedelta(days=1)),
            freq="5min",
            inclusive="left",
        )

    # for debug
    # print(f"dso_num {dso_num}, index {len(index)}, demand_dict {len(demand_dict[meter])}", flush=True)
    # print(f"dso_num {dso_num}, start-> {start_index}, end-> {end_index}", flush=True)
    # for key, value in demand_dict.items():
    #     print(f"dso_num {dso_num}, {key} {len(value)}", flush=True)

    # Create DataFrame from demand_dict
    demand_df = pd.DataFrame.from_dict(demand_dict)
    demand_df.set_index(index, inplace=True)

    # Convert to an hourly profile
    demand_df = demand_df.resample("h").sum().div(1000).div(12)

    # Save the demand data, if specified
    if save:
        demand_df.to_hdf(
            os.path.join(
                dir_path,
                "Substation_" + str(dso_num),
                "Substation_" + str(dso_num) + "_demand_by_meter.h5",
            ),
            key="demand",
            mode="w",
        )

    # Return the monthly hourly demand data for each meter
    return demand_df


def create_baseline_demand_profiles_for_each_meter(
    demand_df,
    dso_num,
    type_of_baseline,
    save=False,
    save_path=None,
):
    """Creates a pandas DataFrame that contains hourly time-series data for each meter 
    in a DSO. The data in this DataFrame is configured to be a baseline demand profile, 
    determined according to a specified metric. The resultant DataFrame can be saved to 
    a .h5 file if desired.
    Arguments:
        demand_df (pandas.DataFrame): Monthly hourly demand data for each meter.
        dso_num (int): The number of a valid substation in the system model.
        type_of_baseline (str): The type of baseline demand that should be considered. 
        There are four types of baselines supported by this function: 'daily',
        'day_of_week', 'weekdays_and_weekends', and 'monthly'.
        save (bool): Indicates whether the output data should be saved in a .h5
        file. If True, data is saved to the location specified by 'save_path'.
        save_path (str): File path that indicates where the resultant baseline demand 
        profile should be saved, if allowed by 'save'.
    Returns:
        bl_demand_df (pandas.DataFrame): Monthly hourly baseline demand data for each 
        meter.
    """

    # Establish the day range
    day_range = list(range(demand_df.index[0].day, demand_df.index[-1].day + 1))

    # Establish the month
    month = demand_df.index[0].month

    # Establish the year
    year = demand_df.index[0].year

    # Determine the type of demand baseline to create based on type_of_baseline
    type_of_baseline = type_of_baseline.lower()
    if type_of_baseline == "daily":
        # Establish the baseline to be the demand profile for each meter
        bl_demand_df = demand_df.copy(deep=True)
    elif type_of_baseline == "days_of_week":
        # Find the average demand for each meter by day of the week and hour
        demand_data_by_weekday_and_hour = demand_df.groupby(
            [demand_df.index.dayofweek, demand_df.index.hour]
        ).mean()

        # Identify the days of the week for the first and last days of the month
        first_day_of_month = pd.to_datetime(
            str(month) + "/" + str(day_range[0]) + "/" + str(year)
        ).dayofweek
        last_day_of_month = pd.to_datetime(
            str(month) + "/" + str(day_range[-1]) + "/" + str(year)
        ).dayofweek

        # Identify the number of full weeks, Monday through Sunday
        num_full_weeks = int(
            (len(day_range) - (7 - first_day_of_month) - (1 + last_day_of_month)) / 7
        )

        # Create the baseline demand data profile
        bl_demand_data = demand_data_by_weekday_and_hour.loc[
            first_day_of_month:6
        ].values.tolist()
        for w in range(num_full_weeks):
            bl_demand_data.extend(demand_data_by_weekday_and_hour.values.tolist())
        bl_demand_data.extend(
            demand_data_by_weekday_and_hour.loc[0:last_day_of_month].values.tolist()
        )

        # Create the baseline demand DataFrame
        bl_demand_df = pd.DataFrame(
            data=bl_demand_data,
            columns=demand_data_by_weekday_and_hour.columns.tolist(),
        )
        bl_demand_df.set_index(demand_df.index, inplace=True)
    elif type_of_baseline == "weekdays_and_weekends":
        # Find the average demand for each meter by weekday/weekend and hour
        demand_data_by_weekday_and_hour = demand_df.groupby(
            [
                np.where(demand_df.index.dayofweek < 5, 0, 1),
                demand_df.index.hour,
            ]
        ).mean()

        # Identify the days of the week for the first and last days of the month
        first_day_of_month = pd.to_datetime(
            str(month) + "/" + str(day_range[0]) + "/" + str(year)
        ).dayofweek
        last_day_of_month = pd.to_datetime(
            str(month) + "/" + str(day_range[-1]) + "/" + str(year)
        ).dayofweek

        # Identify the number of full weeks, Monday through Sunday
        num_full_weeks = int(
            (len(day_range) - (7 - first_day_of_month) - (1 + last_day_of_month)) / 7
        )

        # Create the baseline demand data profile
        bl_demand_data = []
        if (7 - first_day_of_month) > 2:
            for d in range(7 - first_day_of_month - 2):
                bl_demand_data.extend(
                    demand_data_by_weekday_and_hour.loc[0].values.tolist()
                )
            for d in range(2):
                bl_demand_data.extend(
                    demand_data_by_weekday_and_hour.loc[1].values.tolist()
                )
        else:
            for d in range(7 - first_day_of_month):
                bl_demand_data.extend(
                    demand_data_by_weekday_and_hour.loc[1].values.tolist()
                )
        for w in range(num_full_weeks):
            for d in range(5):
                bl_demand_data.extend(
                    demand_data_by_weekday_and_hour.loc[0].values.tolist()
                )
            for d in range(2):
                bl_demand_data.extend(
                    demand_data_by_weekday_and_hour.loc[1].values.tolist()
                )
        if last_day_of_month < 5:
            for d in range(last_day_of_month + 1):
                bl_demand_data.extend(
                    demand_data_by_weekday_and_hour.loc[0].values.tolist()
                )
        else:
            for d in range(5):
                bl_demand_data.extend(
                    demand_data_by_weekday_and_hour.loc[0].values.tolist()
                )
            for d in range(last_day_of_month - 4):
                bl_demand_data.extend(
                    demand_data_by_weekday_and_hour.loc[1].values.tolist()
                )

        # Create the baseline demand DataFrame
        bl_demand_df = pd.DataFrame(
            data=bl_demand_data,
            columns=demand_data_by_weekday_and_hour.columns.tolist(),
        )
        bl_demand_df.set_index(demand_df.index, inplace=True)
    elif type_of_baseline == "monthly":
        # Find the average demand for each meter by hour
        demand_data_by_hour = demand_df.groupby([demand_df.index.hour]).mean()

        # Create the baseline demand data profile
        bl_demand_data = []
        for d in range(len(day_range)):
            bl_demand_data.extend(demand_data_by_hour.values.tolist())

        # Create the baseline demand DataFrame
        bl_demand_df = pd.DataFrame(
            data=bl_demand_data,
            columns=demand_data_by_hour.columns.tolist(),
        )
        bl_demand_df.set_index(demand_df.index, inplace=True)
    else:
        raise ValueError(
            "The provided baseline type is not valid. The allowed types are 'daily', "
            + "'day_of_week', 'weekdays_and_weekends', and 'monthly'. Please try again."
        )

    # Save the demand data, if specified
    if save and (save_path is not None):
        bl_demand_df.to_hdf(
            os.path.join(
                save_path,
                "Substation_" + str(dso_num),
                "Substation_" + str(dso_num) + "_baseline_demand_by_meter.h5",
            ),
            key="demand",
            mode="w",
        )

    # Return the monthly five-minute baseline demand data for each meter
    return bl_demand_df


def calc_cust_bill(metadata, meter_df, trans_df, energy_sum_df, tariff, dso_num, SF, ind_cust):
    """ Calculate the customer bill using summary meter data and fixed tariff structure.
    Args:
        metadata (dict): metadata structure for the DSO to be analyzed
        meter_df (dataframe): monthly and total energy consumption and peak power by house (meter)
        trans_df:
        energy_sum_df:
        tariff (dict): dictionary of fixed tariff structure
        dso_num:
        SF (float): Scaling factor to scale GLD results to TSO scale (e.g. 1743)
        ind_cust (int): number of industrial customers
    Returns:
        bill_df : dataframe of monthly and total bill for each house broken out by each element (energy, demand,
        connection, and total bill)
        """

    # Create empty dataframe structure for all bills for first month.
    meter = []
    variable = []
    month = []

    for each in metadata['billingmeters']:
        meter.append(each)
        variable.append('fix_energy')
        month.append(0)
        meter.append(each)
        variable.append('demand')
        month.append(0)
        meter.append(each)
        variable.append('fix_connect')
        month.append(0)
        meter.append(each)
        variable.append('fix_total')
        month.append(0)
        meter.append(each)
        variable.append('DA_energy')
        month.append(0)
        meter.append(each)
        variable.append('RT_energy')
        month.append(0)
        meter.append(each)
        variable.append('trans_connect')
        month.append(0)
        meter.append(each)
        variable.append('distribution')
        month.append(0)
        meter.append(each)
        variable.append('trans_total')
        month.append(0)
        meter.append(each)
        variable.append('quantity_purchased')
        month.append(0)
        meter.append(each)
        variable.append('blended_rate')
        month.append(0)

    bill_df = pd.DataFrame(month,
                           index=[meter, variable],
                           columns=['sum'])

    month = []
    variable = []
    loads = []
    loadtype = ['residential', 'commercial', 'industrial', 'total']

    for each in loadtype:
        loads.append(each)
        variable.append('fix_energy')
        month.append(0)
        loads.append(each)
        variable.append('demand')
        month.append(0)
        loads.append(each)
        variable.append('fix_connect')
        month.append(0)
        loads.append(each)
        variable.append('fix_total')
        month.append(0)
        loads.append(each)
        variable.append('fix_blended_rate')
        month.append(0)
        loads.append(each)
        variable.append('DA_energy')
        month.append(0)
        loads.append(each)
        variable.append('RT_energy')
        month.append(0)
        loads.append(each)
        variable.append('trans_connect')
        month.append(0)
        loads.append(each)
        variable.append('distribution')
        month.append(0)
        loads.append(each)
        variable.append('trans_total')
        month.append(0)
        loads.append(each)
        variable.append('trans_blended_rate')
        month.append(0)
        loads.append(each)
        variable.append('da_blended_rate')
        month.append(0)
        loads.append(each)
        variable.append('rt_blended_rate')
        month.append(0)

    billsum_df = pd.DataFrame(month,
                              index=[loads, variable],
                              columns=['sum'])

    # Set up dynamic (transactive) tariff structure
    flat = tariff['DSO_' + dso_num]['flat_rate']
    connection = tariff['DSO_' + dso_num]['base_connection_charge']
    trans_dist_rate = tariff['DSO_' + dso_num]['transactive_dist_rate']
    trans_connection = tariff['DSO_' + dso_num]['transactive_connection_charge']
    trans_retail_scale = tariff['DSO_' + dso_num]['transactive_LMP_multiplier']

    # Cycle through each month for which there is energy data and calculate customer bill
    months = list(meter_df.columns[~meter_df.columns.str.contains('sum')])

    for m in months:
        bill_df[m] = [0] * len(bill_df)
        billsum_df[m] = [0] * len(billsum_df)
        if energy_sum_df.loc[('total', 'da_q'), m] + energy_sum_df.loc[('total', 'rt_q'), m] == 0:
            congestion_rebate = 0
        else:
            congestion_rebate = energy_sum_df.loc[('total', 'congest_$'), m] / (
                    energy_sum_df.loc[('total', 'da_q'), m] + energy_sum_df.loc[('total', 'rt_q'), m])

        for each in metadata['billingmeters']:
            kw_hrs = meter_df.loc[(each, 'kw-hr'), m]
            max_kw = meter_df.loc[(each, 'max_kw'), m]

            if metadata['billingmeters'][each]['cust_participating']:
                # Calculate bill for transactive customer
                bill_df.loc[(each, 'DA_energy'), m] = trans_df.loc[(each, 'DA_cost'), m] * trans_retail_scale
                bill_df.loc[(each, 'RT_energy'), m] = trans_df.loc[(each, 'RT_cost'), m] * trans_retail_scale
                bill_df.loc[(each, 'trans_connect'), m] = trans_connection
                bill_df.loc[(each, 'distribution'), m] = \
                    meter_df.loc[(each, 'kw-hr'), m] * trans_dist_rate - congestion_rebate
                bill_df.loc[(each, 'trans_total'), m] = \
                    bill_df.loc[(each, 'DA_energy'), m] + bill_df.loc[(each, 'RT_energy'), m] + \
                    bill_df.loc[(each, 'trans_connect'), m] + bill_df.loc[(each, 'distribution'), m]
            else:
                # Calculate bill for baseline (non-participating) customer on fixed tariff structure
                tier2 = 0
                tier3 = 0
                tariff_class = metadata['billingmeters'][each]['tariff_class']
                T1P = tariff['DSO_' + dso_num][tariff_class]['tier_1']['price']
                T1Q = tariff['DSO_' + dso_num][tariff_class]['tier_1']['max_quantity']
                T2P = tariff['DSO_' + dso_num][tariff_class]['tier_2']['price']
                T2Q = tariff['DSO_' + dso_num][tariff_class]['tier_2']['max_quantity']
                demand = tariff['DSO_' + dso_num][tariff_class]['demand_charge']

                if kw_hrs >= T1Q:
                    tier2 = 1
                if kw_hrs >= T2Q:
                    tier3 = 1
                bill_df.loc[(each, 'fix_energy'), m] = \
                    flat * kw_hrs + T1P * tier2 * (kw_hrs - T1Q) + T2P * tier3 * (kw_hrs - T2Q)
                bill_df.loc[(each, 'demand'), m] = demand * max_kw
                # TODO: Need to fix connection charge for street lights (gets too expensive given how many there are).
                bill_df.loc[(each, 'fix_connect'), m] = connection
                bill_df.loc[(each, 'fix_total'), m] = \
                    bill_df.loc[(each, 'fix_energy'), m] + \
                    bill_df.loc[(each, 'demand'), m] + \
                    bill_df.loc[(each, 'fix_connect'), m]

            #  Calculated average electricity price (blended rate) for each customer
            if kw_hrs == 0:
                bill_df.loc[(each, 'blended_rate'), m] = 0
            else:
                bill_df.loc[(each, 'blended_rate'), m] = (bill_df.loc[(each, 'fix_total'), m] +
                                                          bill_df.loc[(each, 'trans_total'), m]) / kw_hrs

            bill_df.loc[(each, 'quantity_purchased'), m] = kw_hrs

            # Calculate total revenue for each customer class (aka load type)
        for each in metadata['billingmeters']:
            for load in loadtype:
                if metadata['billingmeters'][each]['tariff_class'] == load:
                    # Sum transactive values
                    billsum_df.loc[(load, 'DA_energy'), m] += bill_df.loc[(each, 'DA_energy'), m] * SF
                    billsum_df.loc[(load, 'RT_energy'), m] += bill_df.loc[(each, 'RT_energy'), m] * SF
                    billsum_df.loc[(load, 'trans_connect'), m] += bill_df.loc[(each, 'trans_connect'), m] * SF
                    billsum_df.loc[(load, 'distribution'), m] += bill_df.loc[(each, 'distribution'), m] * SF
                    billsum_df.loc[(load, 'trans_total'), m] += bill_df.loc[(each, 'trans_total'), m] * SF
                    # Sum non-partipating / base-case values
                    billsum_df.loc[(load, 'fix_energy'), m] += bill_df.loc[(each, 'fix_energy'), m] * SF
                    billsum_df.loc[(load, 'demand'), m] += bill_df.loc[(each, 'demand'), m] * SF
                    billsum_df.loc[(load, 'fix_connect'), m] += bill_df.loc[(each, 'fix_connect'), m] * SF
                    billsum_df.loc[(load, 'fix_total'), m] += bill_df.loc[(each, 'fix_total'), m] * SF

    # Calculate industrial load bill.  This lumps all industrial loads as one entity and surplants any individual
    # industrial load bills calculated for individual GLD meters above.  This is OK as those meters are small zip loads
    # representing streetlights.
    for m in months:
        # Calculate bill for baseline (non-participating) customer on fixed tariff structure
        tier2 = 0
        tier3 = 0
        tariff_class = 'industrial'
        T1P = tariff['DSO_' + dso_num][tariff_class]['tier_1']['price']
        T1Q = tariff['DSO_' + dso_num][tariff_class]['tier_1']['max_quantity']
        T2P = tariff['DSO_' + dso_num][tariff_class]['tier_2']['price']
        T2Q = tariff['DSO_' + dso_num][tariff_class]['tier_2']['max_quantity']
        demand = tariff['DSO_' + dso_num][tariff_class]['demand_charge']

        kw_hrs = energy_sum_df.loc[('industrial', 'kw-hr'), m]
        max_kw = energy_sum_df.loc[('industrial', 'demand_quantity'), m]
        if kw_hrs >= T1Q:
            tier2 = 1
        if kw_hrs >= T2Q:
            tier3 = 1
        billsum_df.loc[('industrial', 'fix_energy'), m] = \
            flat * kw_hrs + T1P * tier2 * (kw_hrs - T1Q) + T2P * tier3 * (kw_hrs - T2Q)
        billsum_df.loc[('industrial', 'demand'), m] = demand * max_kw
        billsum_df.loc[('industrial', 'fix_connect'), m] = connection * ind_cust
        billsum_df.loc[('industrial', 'fix_total'), m] = \
            billsum_df.loc[('industrial', 'fix_energy'), m] + \
            billsum_df.loc[('industrial', 'demand'), m] + \
            billsum_df.loc[('industrial', 'fix_connect'), m]

    # Calculate total values across all customer classes.
    for item in ['DA_energy', 'RT_energy', 'trans_connect', 'distribution', 'trans_total', 'fix_energy', 'demand',
                 'fix_connect', 'fix_total']:
        for load in ['residential', 'commercial', 'industrial']:
            billsum_df.loc[('total', item), :] += billsum_df.loc[(load, item), :]

    # Calculate the annual sum.
    bill_df['sum'] = bill_df.loc[:, bill_df.columns[~bill_df.columns.str.contains('sum')]].sum(axis=1)
    for each in metadata['billingmeters']:
        bill_df.loc[(each, 'blended_rate'), 'sum'] = (bill_df.loc[(each, 'fix_total'), 'sum'] +
                                                      bill_df.loc[(each, 'trans_total'), 'sum']) / bill_df.loc[
                                                         (each, 'quantity_purchased'), 'sum']
    billsum_df['sum'] = billsum_df.loc[:, billsum_df.columns[~billsum_df.columns.str.contains('sum')]].sum(
        axis=1)

    #  Calculated average electricity price (blended rate) for each customer class and purchase type
    for load in ['residential', 'commercial', 'industrial', 'total']:
        fixed_energy_q = energy_sum_df.loc[(load, 'kw-hr')] - energy_sum_df.loc[(load, 'da_q')] \
                         - energy_sum_df.loc[(load, 'rt_q')]
        billsum_df.loc[(load, 'fix_blended_rate')] = billsum_df.loc[(load, 'fix_total')] / fixed_energy_q
        # Find fraction of day ahead energy to proportion distribution and connection costs.
        da_fraction = energy_sum_df.loc[(load, 'da_q')] / (
                    energy_sum_df.loc[(load, 'da_q')] + energy_sum_df.loc[(load, 'rt_q')])
        billsum_df.loc[(load, 'da_blended_rate')] = (billsum_df.loc[(load, 'DA_energy')] + da_fraction *
                                                     (billsum_df.loc[(load, 'trans_connect')] +
                                                      billsum_df.loc[(load, 'distribution')])) / energy_sum_df.loc[
                                                        (load, 'da_q')]
        billsum_df.loc[(load, 'rt_blended_rate')] = (billsum_df.loc[(load, 'RT_energy')] + (1 - da_fraction) *
                                                     (billsum_df.loc[(load, 'trans_connect')] +
                                                      billsum_df.loc[(load, 'distribution')])) / energy_sum_df.loc[
                                                        (load, 'rt_q')]
        billsum_df.loc[(load, 'trans_blended_rate')] = billsum_df.loc[(load, 'trans_total')] / \
                                                       (energy_sum_df.loc[(load, 'da_q')] + energy_sum_df.loc[
                                                           (load, 'rt_q')])

    return bill_df, billsum_df


def calculate_consumer_bills(
    case_path,
    base_path,
    metadata,
    meter_df,
    trans_df,
    energy_sum_df,
    tariff,
    dso_num,
    sf,
    num_ind_cust,
    rate_scenario,
):
    """Calculates the consumers' bills for the four different scenarios considered in 
    the Rates Analysis work.
    Args:
        case_path (str): A string specifying the directory path of the case being analyzed.
        base_path (str): A string specifying the directory path of the reference case (containing baseline demand).
        metadata (dict): A dictionary containing the metadata structure of the DSO.
        meter_df (pandas.DataFrame): DataFrame containing consumers' consumption information.
        trans_df (pandas.DataFrame): DataFrame containing consumers' transactive consumption
        information.
        energy_sum_df (pandas.DataFrame): DataFrame containing consumption information for 
        each consumer class.
        tariff (dict): A dictionary of pertinant tariff information. Includes information 
        for the volumetric rates (i.e., flat and time-of-use).
        dso_num (str): A string specifying the number of the DSo being considered.
        sf (float): Scaling factor to scale the GridLAB-D results to TSO scale.
        num_ind_cust (int): Number of industrial consumers.
        rate_scenario (str): A str specifying the rate scenario under investigation: flat,
        time-of-use, subscription, transactive, or dsot.
    Returns:
        bill_df (pandas.DataFrame): DataFrame containing bill information for each meter.
        billsum_df (pandas.DataFrame): DataFrame containing bill information for each 
        load sector.
    """

    # Load in necessary data for the defined rate scenario
    if rate_scenario in ["time-of-use", "subscription"]:
        tou_params = load_json(case_path, "time_of_use_parameters.json")

    # Specify the bill components that will be recorded
    bill_components = [
        "flat_energy_charge",
        "flat_demand_charge",
        "flat_fixed_charge",
        "flat_total_charge",
        "flat_energy_purchased",
        "flat_average_price",
    ]
    if rate_scenario == "time-of-use":
        bill_components.append("tou_energy_charge")
        bill_components.extend(
            [
                "tou_" + k + "_energy_charge"
                for k in tou_params["DSO_" + dso_num]["Jan"]["periods"].keys()
            ]
        )
        bill_components.append("tou_demand_charge")
        bill_components.append("tou_fixed_charge")
        bill_components.append("tou_total_charge")
        bill_components.extend(
            [
                "tou_" + k + "_energy_purchased"
                for k in tou_params["DSO_" + dso_num]["Jan"]["periods"].keys()
            ]
        )
        bill_components.append("tou_energy_purchased")
        bill_components.append("tou_average_price")
    elif rate_scenario == "subscription":
        bill_components.append("subscription_net_deviation_charge")
        bill_components.append("subscription_energy_charge")
        bill_components.extend(
            [
                "subscription_" + k + "_energy_charge"
                for k in tou_params["DSO_" + dso_num]["Jan"]["periods"].keys()
            ]
        )
        bill_components.append("subscription_demand_charge")
        bill_components.append("subscription_fixed_charge")
        bill_components.append("subscription_total_charge")
        bill_components.extend(
            [
                "subscription_" + k + "_energy_purchased"
                for k in tou_params["DSO_" + dso_num]["Jan"]["periods"].keys()
            ]
        )
        bill_components.append("subscription_energy_purchased")
        bill_components.append("subscription_average_price")
    elif rate_scenario == "transactive":
        bill_components.append("transactive_DA_energy_charge")
        bill_components.append("transactive_RT_energy_charge")
        #bill_components.append("transactive_DA_capacity_charge")
        #bill_components.append("transactive_RT_capacity_charge")
        bill_components.append("transactive_fixed_charge")
        bill_components.append("transactive_volumetric_charge")
        bill_components.append("transactive_total_charge")
        bill_components.append("transactive_energy_purchased")
        bill_components.append("transactive_average_price")
    elif rate_scenario == "dsot":
        bill_components.append("dsot_DA_energy_charge")
        bill_components.append("dsot_RT_energy_charge")
        bill_components.append("dsot_fixed_charge")
        bill_components.append("dsot_volumetric_charge")
        bill_components.append("dsot_total_charge")
        bill_components.append("dsot_energy_purchased")
        bill_components.append("dsot_average_price")

    # Create empty DataFrame for all consumer bills
    meters = []
    variable = []
    month = []
    for meter in metadata["billingmeters"]:
        for component in bill_components:
            meters.append(meter)
            variable.append(component)
            month.append(0)
    bill_df = pd.DataFrame(month, index=[meters, variable], columns=["sum"])

    # Create empty DataFrame for sectoral aggregations of consumers' bills
    loads = []
    variable = []
    month = []
    for load in ["residential", "commercial", "industrial", "total"]:
        for component in bill_components:
            loads.append(load)
            variable.append(component)
            month.append(0)
    billsum_df = pd.DataFrame(month, index=[loads, variable], columns=["sum"])

    # Specify price components that do not vary in time or by consumer type
    flat_rate = tariff["DSO_" + dso_num]["flat_rate"]
    fixed_charge = tariff["DSO_" + dso_num]["base_connection_charge"]
    trans_vol_charge = tariff["DSO_" + dso_num]["transactive_dist_rate"]
    trans_fixed_charge = tariff["DSO_" + dso_num]["transactive_connection_charge"]
    trans_retail_scale = tariff["DSO_" + dso_num]["transactive_LMP_multiplier"]
    
    # Cycle through each month for which there is energy data and calculate customer bill
    months = list(meter_df.columns[~meter_df.columns.str.contains("sum")])
    for m in months:
        # Initialize the DataFrames for each month
        bill_df[m] = [0] * len(bill_df)
        billsum_df[m] = [0] * len(billsum_df)

        if rate_scenario == "subscription":
            # Create a mapping between month name and month number
            month_map = {
                "Jan": "01",
                "Feb": "02",
                "Mar": "03",
                "Apr": "04",
                "May": "05",
                "Jun": "06",
                "Jul": "07",
                "Aug": "08",
                "Sep": "09",
                "Oct": "10",
                "Nov": "11",
                "Dec": "12",
            }

            # For the subscription rate, load the month's hourly baseline demand
            # profile and the month's hourly demand profile
            bl_demand_df = pd.read_hdf(
                os.path.join(
                    base_path,
                    [
                        p
                        for p in os.listdir(case_path)
                        if len(p) > 10
                        if p[7:9] == month_map[m]
                    ][0],
                    "Substation_" + dso_num,
                    "Substation_" + dso_num + "_baseline_demand_by_meter.h5",
                ),
                key="demand",
                mode="r",
            )
            demand_df = pd.read_hdf(
                os.path.join(
                    case_path,
                    [
                        p
                        for p in os.listdir(case_path)
                        if len(p) > 10
                        if p[7:9] == month_map[m]
                    ][0],
                    "Substation_" + dso_num,
                    "Substation_" + dso_num + "_demand_by_meter.h5",
                ),
                key="demand",
                mode="r",
            )

            # For the subscription rate, load in the annual DA LMP data and convert to 
            # $/kWh
            da_lmp_stats = (
                pd.read_csv(
                    os.path.join(case_path, "Annual_DA_LMP_Load_data.csv"), index_col=0
                )
                / 1000
            )

        # Iterate through each consumer
        for each in metadata["billingmeters"]:
            # Specify the demand charge based on the consumer's sector type
            demand_charge = tariff["DSO_" + dso_num][
                metadata["billingmeters"][each]["tariff_class"]
            ]["demand_charge"]
            
            # Determine bills for participating vs. non-participating consumers
            if metadata["billingmeters"][each]["cust_participating"]:
                if rate_scenario == "time-of-use":
                    # Calculate the consumer's energy charge under the time-of-use tariff
                    bill_df.loc[(each, "tou_energy_charge"), m] = sum(
                        tou_params["DSO_" + dso_num][m]["price"]
                        * tou_params["DSO_" + dso_num][m]["periods"][k]["ratio"]
                        * meter_df.loc[(each, k + "_kwh"), m]
                        for k in tou_params["DSO_" + dso_num][m]["periods"].keys()
                    )

                    # Calculate the consumer's tier credit (due to the declining block)
                    # rate, if the consumer is eligible
                    if metadata["billingmeters"][each]["tariff_class"] in [
                        "residential",
                        "commercial",
                        "industrial",
                    ]:
                        bill_df.loc[
                            (each, "tou_energy_charge"), m
                        ] += calculate_tier_credit(
                            dso_num,
                            metadata["billingmeters"][each]["tariff_class"],
                            tariff,
                            meter_df.loc[(each, "kw-hr"), m],
                        )

                    # Calculate the consumer's energy charge for each time-of-use period
                    for k in tou_params["DSO_" + dso_num][m]["periods"].keys():
                        bill_df.loc[(each, "tou_" + k + "_energy_charge"), m] = (
                            tou_params["DSO_" + dso_num][m]["price"]
                            * tou_params["DSO_" + dso_num][m]["periods"][k]["ratio"]
                            * meter_df.loc[(each, k + "_kwh"), m]
                        )

                    # Calculate the consumer's demand charge under the time-of-use tariff
                    bill_df.loc[(each, "tou_demand_charge"), m] = (
                        demand_charge * meter_df.loc[(each, "max_kw"), m]
                    )

                    # Calculate the consumer's fixed charge under the time-of-use tariff
                    bill_df.loc[(each, "tou_fixed_charge"), m] = fixed_charge

                    # Calculate the consumer's total bill under the time-of-use tariff
                    bill_df.loc[(each, "tou_total_charge"), m] = (
                        bill_df.loc[(each, "tou_energy_charge"), m]
                        + bill_df.loc[(each, "tou_demand_charge"), m]
                        + bill_df.loc[(each, "tou_fixed_charge"), m]
                    )

                    # Store the total energy purchased under the time-of-use tariff
                    bill_df.loc[(each, "tou_energy_purchased"), m] = meter_df.loc[
                        (each, "kw-hr"), m
                    ]

                    # Store the total energy purchased during each time-of-use period
                    for k in tou_params["DSO_" + dso_num][m]["periods"].keys():
                        bill_df.loc[
                            (each, "tou_" + k + "_energy_purchased"), m
                        ] = meter_df.loc[(each, k + "_kwh"), m]

                    # Calculate the average price under the time-of-use tariff
                    if meter_df.loc[(each, "kw-hr"), m] == 0:
                        bill_df.loc[(each, "tou_average_price"), m] = 0
                    else:
                        bill_df.loc[(each, "tou_average_price"), m] = (
                            bill_df.loc[(each, "tou_total_charge"), m]
                            / meter_df.loc[(each, "kw-hr"), m]
                        )
                elif rate_scenario == "subscription":
                    # Calculate the consumer's net deviation charge under the
                    # subscription rate
                    bill_df.loc[(each, "subscription_net_deviation_charge"), m] = sum(
                        da_lmp_stats.loc[str(t), "da_lmp" + dso_num]
                        * (demand_df.loc[t, each] - bl_demand_df.loc[t, each])
                        for t in demand_df.index
                    )

                    # Calculate the consumer's energy charge under the time-of-use rate
                    # associated with the subscription rate
                    bill_df.loc[(each, "subscription_energy_charge"), m] = sum(
                        tou_params["DSO_" + dso_num][m]["price"]
                        * tou_params["DSO_" + dso_num][m]["periods"][k]["ratio"]
                        * sum(
                            bl_demand_df.loc[:, each]
                            .between_time(
                                str(
                                    tou_params["DSO_" + dso_num][m]["periods"][k][
                                        "hour_start"
                                    ][h]
                                )
                                + ":00",
                                str(
                                    tou_params["DSO_" + dso_num][m]["periods"][k][
                                        "hour_end"
                                    ][h]
                                )
                                + ":00"
                                if tou_params["DSO_" + dso_num][m]["periods"][k][
                                    "hour_end"
                                ][h]
                                != 24
                                else "0:00",
                                inclusive="left",
                            )
                            .sum()
                            for h in range(
                                len(
                                    tou_params["DSO_" + dso_num][m]["periods"][k][
                                        "hour_start"
                                    ]
                                )
                            )
                        )
                        for k in tou_params["DSO_" + dso_num][m]["periods"].keys()
                    ) + calculate_tier_credit(
                        dso_num,
                        metadata["billingmeters"][each]["tariff_class"],
                        tariff,
                        bl_demand_df.loc[:, each].sum(),
                    )

                    # Calculate the consumer's energy charge for each time-of-use period
                    for k in tou_params["DSO_" + dso_num][m]["periods"].keys():
                        bill_df.loc[(each, "subscription_" + k + "_energy_charge"), m] = (
                            tou_params["DSO_" + dso_num][m]["price"]
                            * tou_params["DSO_" + dso_num][m]["periods"][k]["ratio"]
                            * sum(
                                bl_demand_df.loc[:, each]
                                .between_time(
                                    str(
                                        tou_params["DSO_" + dso_num][m]["periods"][k][
                                            "hour_start"
                                        ][h]
                                    )
                                    + ":00",
                                    str(
                                        tou_params["DSO_" + dso_num][m]["periods"][k][
                                            "hour_end"
                                        ][h]
                                    )
                                    + ":00"
                                    if tou_params["DSO_" + dso_num][m]["periods"][k][
                                        "hour_end"
                                    ][h]
                                    != 24
                                    else "0:00",
                                    inclusive="left",
                                )
                                .sum()
                                for h in range(
                                    len(
                                        tou_params["DSO_" + dso_num][m]["periods"][k][
                                            "hour_start"
                                        ]
                                    )
                                )
                            )
                        )

                    # Calculate the consumer's demand charge under the subscription tariff
                    bill_df.loc[(each, "subscription_demand_charge"), m] = (
                        demand_charge * bl_demand_df.loc[:, each].max()
                    )

                    # Calculate the consumer's fixed charge under the subscription tariff
                    bill_df.loc[(each, "subscription_fixed_charge"), m] = fixed_charge

                    # Calculate the consumer's total bill under the subscription tariff
                    bill_df.loc[(each, "subscription_total_charge"), m] = (
                        bill_df.loc[(each, "subscription_net_deviation_charge"), m]
                        + bill_df.loc[(each, "subscription_energy_charge"), m]
                        + bill_df.loc[(each, "subscription_demand_charge"), m]
                        + bill_df.loc[(each, "subscription_fixed_charge"), m]
                    )

                    # Store the total energy purchased under the subscription tariff
                    bill_df.loc[
                        (each, "subscription_energy_purchased"), m
                    ] = bl_demand_df.loc[:, each].sum()

                    # Store the total energy purchased during each time-of-use period
                    for k in tou_params["DSO_" + dso_num][m]["periods"].keys():
                        bill_df.loc[
                            (each, "subscription_" + k + "_energy_purchased"), m
                        ] = sum(
                            bl_demand_df.loc[:, each]
                            .between_time(
                                str(
                                    tou_params["DSO_" + dso_num][m]["periods"][k][
                                        "hour_start"
                                    ][h]
                                )
                                + ":00",
                                str(
                                    tou_params["DSO_" + dso_num][m]["periods"][k][
                                        "hour_end"
                                    ][h]
                                )
                                + ":00"
                                if tou_params["DSO_" + dso_num][m]["periods"][k][
                                    "hour_end"
                                ][h]
                                != 24
                                else "0:00",
                                inclusive="left",
                            )
                            .sum()
                            for h in range(
                                len(
                                    tou_params["DSO_" + dso_num][m]["periods"][k][
                                        "hour_start"
                                    ]
                                )
                            )
                        )

                    # Calculate the average price under the subscription tariff
                    if bl_demand_df.loc[:, each].sum() == 0:
                        bill_df.loc[(each, "subscription_average_price"), m] = 0
                    else:
                        bill_df.loc[(each, "subscription_average_price"), m] = (
                            bill_df.loc[(each, "subscription_total_charge"), m]
                            / bl_demand_df.loc[:, each].sum()
                        )
                elif rate_scenario == "transactive":
                    # Calculate the consumer's market-related charges under the 
                    # transactive tariff
                    bill_df.loc[(each, "transactive_DA_energy_charge"), m] = (
                        trans_df.loc[(each, "DA_cost"), m] * trans_retail_scale
                    )
                    bill_df.loc[(each, "transactive_RT_energy_charge"), m] = (
                        trans_df.loc[(each, "RT_cost"), m] * trans_retail_scale
                    )

                    # Calculate the consumer's fixed charge under the transactive tariff
                    bill_df.loc[
                        (each, "transactive_fixed_charge"), m
                    ] = trans_fixed_charge

                    # Calculate the consumer's volumetric energy charge under the
                    # transactive tariff
                    bill_df.loc[(each, "transactive_volumetric_charge"), m] = (
                        meter_df.loc[(each, "kw-hr"), m] * trans_vol_charge
                    )

                    # Calculate the consumer's total bill under the transactive tariff
                    bill_df.loc[(each, "transactive_total_charge"), m] = (
                        bill_df.loc[(each, "transactive_DA_energy_charge"), m]
                        + bill_df.loc[(each, "transactive_RT_energy_charge"), m]
                        #+ bill_df.loc[(each, "transactive_DA_capacity_charge"), m]
                        #+ bill_df.loc[(each, "transactive_RT_capacity_charge"), m]
                        + bill_df.loc[(each, "transactive_fixed_charge"), m]
                        + bill_df.loc[(each, "transactive_volumetric_charge"), m]
                    )

                    # Store the total energy purchased under the transactive tariff
                    bill_df.loc[
                        (each, "transactive_energy_purchased"), m
                    ] = meter_df.loc[(each, "kw-hr"), m]

                    # Calculate the average price under the transactive rate
                    if meter_df.loc[(each, "kw-hr"), m] == 0:
                        bill_df.loc[(each, "transactive_average_price"), m] = 0
                    else:
                        bill_df.loc[(each, "transactive_average_price"), m] = (
                            bill_df.loc[(each, "transactive_total_charge"), m]
                            / meter_df.loc[(each, "kw-hr"), m]
                        )
                elif rate_scenario == "dsot":
                    # Calculate the consumer's market-related charges under the DSO+T 
                    # tariff
                    bill_df.loc[(each, "dsot_DA_energy_charge"), m] = (
                        trans_df.loc[(each, "DA_cost"), m] * trans_retail_scale
                    )
                    bill_df.loc[(each, "dsot_RT_energy_charge"), m] = (
                        trans_df.loc[(each, "RT_cost"), m] * trans_retail_scale
                    )

                    # Calculate the consumer's fixed charge under the DSO+T tariff
                    bill_df.loc[(each, "dsot_fixed_charge"), m] = trans_fixed_charge

                    # Calculate the consumer's volumetric energy charge under the DSO+T
                    # tariff
                    bill_df.loc[(each, "dsot_volumetric_charge"), m] = (
                        meter_df.loc[(each, "kw-hr"), m] * trans_vol_charge
                    )

                    # Calculate the consumer's total bill under the DSO+T tariff
                    bill_df.loc[(each, "dsot_total_charge"), m] = (
                        bill_df.loc[(each, "dsot_DA_energy_charge"), m]
                        + bill_df.loc[(each, "dsot_RT_energy_charge"), m]
                        + bill_df.loc[(each, "dsot_fixed_charge"), m]
                        + bill_df.loc[(each, "dsot_volumetric_charge"), m]
                    )

                    # Store the total energy purchased under the DSO+T tariff
                    bill_df.loc[(each, "dsot_energy_purchased"), m] = meter_df.loc[
                        (each, "kw-hr"), m
                    ]

                    # Calculate the average price under the DSO+T rate
                    if meter_df.loc[(each, "kw-hr"), m] == 0:
                        bill_df.loc[(each, "dsot_average_price"), m] = 0
                    else:
                        bill_df.loc[(each, "dsot_average_price"), m] = (
                            bill_df.loc[(each, "dsot_total_charge"), m]
                            / meter_df.loc[(each, "kw-hr"), m]
                        )
            else:
                # Calculate the consumer's energy charge under the flat rate tariff
                bill_df.loc[(each, "flat_energy_charge"), m] = flat_rate * meter_df.loc[
                    (each, "kw-hr"), m
                ]

                # Calculate the consumer's tier credit (due to the declining block)
                # rate, if the consumer is eligible
                if metadata["billingmeters"][each]["tariff_class"] in [
                    "residential",
                    "commercial",
                    "industrial",
                ]:
                    bill_df.loc[
                        (each, "flat_energy_charge"), m
                    ] += calculate_tier_credit(
                        dso_num,
                        metadata["billingmeters"][each]["tariff_class"],
                        tariff,
                        meter_df.loc[(each, "kw-hr"), m],
                    )

                # Calculate the consumer's demand charge under the flat rate tariff
                bill_df.loc[(each, "flat_demand_charge"), m] = (
                    demand_charge * meter_df.loc[(each, "max_kw"), m]
                )

                # Calculate the consumer's fixed charge under the flat rate tariff
                bill_df.loc[(each, "flat_fixed_charge"), m] = fixed_charge

                # Calculate the consumer's total bill under the flat rate tariff
                bill_df.loc[(each, "flat_total_charge"), m] = (
                    bill_df.loc[(each, "flat_energy_charge"), m]
                    + bill_df.loc[(each, "flat_demand_charge"), m]
                    + bill_df.loc[(each, "flat_fixed_charge"), m]
                )

                # Store the total energy purchased under the flat tariff
                bill_df.loc[(each, "flat_energy_purchased"), m] = meter_df.loc[
                    (each, "kw-hr"), m
                ]

                # Calculate the average price under the flat tariff
                if meter_df.loc[(each, "kw-hr"), m] == 0:
                    bill_df.loc[(each, "flat_average_price"), m] = 0
                else:
                    bill_df.loc[(each, "flat_average_price"), m] = (
                        bill_df.loc[(each, "flat_total_charge"), m]
                        / meter_df.loc[(each, "kw-hr"), m]
                    )

            # Calculate the totals for each consumer class except for industrial
            # consumers, which are calculated separately below
            if metadata["billingmeters"][each]["tariff_class"] in [
                "residential",
                "commercial",
            ]:
                for component in bill_components:
                    if "average_price" not in component:
                        billsum_df.loc[
                            (
                                metadata["billingmeters"][each]["tariff_class"],
                                component,
                            ),
                            m,
                        ] += (
                            bill_df.loc[(each, component), m] * sf
                        )

        # Calculate totals for the industrial loads. As was done in DSO+T, all
        # industrial loads are lumped into one entity that includes the individual-
        # metered industrial loads considered above (generally small and representing
        # street lights) and bulk industrial loads that are large and flat.
        billsum_df.loc[
            ("industrial", "flat_energy_charge"), m
        ] = flat_rate * energy_sum_df.loc[
            ("industrial", "kw-hr"), m
        ] + calculate_tier_credit(
            dso_num,
            "industrial",
            tariff,
            energy_sum_df.loc[("industrial", "kw-hr"), m],
        )
        billsum_df.loc[("industrial", "flat_demand_charge"), m] = (
            tariff["DSO_" + dso_num]["industrial"]["demand_charge"]
            * energy_sum_df.loc[("industrial", "demand_quantity"), m]
        )
        billsum_df.loc[("industrial", "flat_fixed_charge"), m] = (
            fixed_charge * num_ind_cust
        )
        billsum_df.loc[("industrial", "flat_total_charge"), m] = (
            billsum_df.loc[("industrial", "flat_energy_charge"), m]
            + billsum_df.loc[("industrial", "flat_demand_charge"), m]
            + billsum_df.loc[("industrial", "flat_fixed_charge"), m]
        )
        billsum_df.loc[("industrial", "flat_energy_purchased"), m] = energy_sum_df.loc[
            ("industrial", "kw-hr"), m
        ]

    # Calculate the totals across all consumer classes
    for component in bill_components:
        if "average_price" not in component:
            for load in ["residential", "commercial", "industrial"]:
                billsum_df.loc[("total", component), :] += billsum_df.loc[
                    (load, component), :
                ]

    # Calculate the annual sums
    bill_df["sum"] = bill_df.loc[
        :, bill_df.columns[~bill_df.columns.str.contains("sum")]
    ].sum(axis=1)
    billsum_df["sum"] = billsum_df.loc[
        :, billsum_df.columns[~billsum_df.columns.str.contains("sum")]
    ].sum(axis=1)

    # Calculate the average prices at the meter level
    for each in metadata["billingmeters"]:
        bill_df.loc[(each, "flat_average_price"), "sum"] = (
            bill_df.loc[(each, "flat_total_charge"), "sum"]
            / bill_df.loc[(each, "flat_energy_purchased"), "sum"]
        )
        if rate_scenario == "time-of-use":
            bill_df.loc[(each, "tou_average_price"), "sum"] = (
                bill_df.loc[(each, "tou_total_charge"), "sum"]
                / bill_df.loc[(each, "tou_energy_purchased"), "sum"]
            )
        elif rate_scenario == "subscription":
            bill_df.loc[(each, "subscription_average_price"), "sum"] = (
                bill_df.loc[(each, "subscription_total_charge"), "sum"]
                / bill_df.loc[(each, "subscription_energy_purchased"), "sum"]
            )
        elif rate_scenario == "transactive":
            bill_df.loc[(each, "transactive_average_price"), "sum"] = (
                bill_df.loc[(each, "transactive_total_charge"), "sum"]
                / bill_df.loc[(each, "transactive_energy_purchased"), "sum"]
            )
        elif rate_scenario == "dsot":
            bill_df.loc[(each, "dsot_average_price"), "sum"] = (
                bill_df.loc[(each, "dsot_total_charge"), "sum"]
                / bill_df.loc[(each, "dsot_energy_purchased"), "sum"]
            )
        
    # Calculate the average prices at the sector level
    for load in ["residential", "commercial", "industrial", "total"]:
        billsum_df.loc[(load, "flat_average_price")] = (
            billsum_df.loc[(load, "flat_total_charge")]
            / billsum_df.loc[(load, "flat_energy_purchased")]
        )
        if rate_scenario == "time-of-use":
            billsum_df.loc[(load, "tou_average_price")] = (
                billsum_df.loc[(load, "tou_total_charge")]
                / billsum_df.loc[(load, "tou_energy_purchased")]
            )
        elif rate_scenario == "subscription":
            billsum_df.loc[(load, "subscription_average_price")] = (
                billsum_df.loc[(load, "subscription_total_charge")]
                / billsum_df.loc[(load, "subscription_energy_purchased")]
            )
        elif rate_scenario == "transactive":
            billsum_df.loc[(load, "transactive_average_price")] = (
                billsum_df.loc[(load, "transactive_total_charge")]
                / billsum_df.loc[(load, "transactive_energy_purchased")]
            )
        elif rate_scenario == "dsot":
            billsum_df.loc[(load, "dsot_average_price")] = (
                billsum_df.loc[(load, "dsot_total_charge")]
                / billsum_df.loc[(load, "dsot_energy_purchased")]
            )

    # Return the bill DataFrames
    return bill_df, billsum_df


def calculate_tier_credit(dso_num, tariff_class, tariff, total_energy):
    """Calculate the tier credit added to the consumers' bills from the declining-block 
    rate.
    Args:
        dso_num (str): A string specifying the number of the DSO being considered.
        tariff_class (str): Indicates the type of consumer that is under consideration.
        tariff (dict): A dictionary of pertinant tariff information. Includes information 
        for the volumetric rates (i.e., flat and time-of-use).
        total_energy (float): Consumer's total energy consumption for the month.
    Returns:
        tier_credit (float): The tier credit that will be applied to the energy portion 
        of the consumer's bill.
    """

    # Specify the parameters of the declining-block tiers of the tiered rate
    tier_info = {
        1: {
            "price": 0,
            "threshold": tariff["DSO_" + dso_num][tariff_class]["tier_1"]["max_quantity"],
        },
        2: {
            "price": tariff["DSO_" + dso_num][tariff_class]["tier_1"]["price"],
            "threshold": tariff["DSO_" + dso_num][tariff_class]["tier_2"]["max_quantity"],
        },
        3: {
            "price": sum(
                tariff["DSO_" + dso_num][tariff_class]["tier_" + str(i)]["price"]
                for i in range(1, 3)
            ),
            "threshold": tariff["DSO_" + dso_num][tariff_class]["tier_3"]["max_quantity"],
        },
    }

    # Calculate the tier credit
    tier_credit = 0
    for b in tier_info:
        if b == 1:
            prev_threshold = 0
        else:
            prev_threshold = tier_info[b - 1]["threshold"]
        tier_credit += tier_info[b]["price"] * max(
            min(
                total_energy - prev_threshold,
                tier_info[b]["threshold"] - prev_threshold,
            ),
            0,
        )

    # Return the tier credit
    return tier_credit


def calculate_tariff_prices(
    case_path,
    base_case_path,
    metadata,
    meter_df,
    trans_df,
    energy_sum_df,
    tariff,
    dso_num,
    sf,
    num_ind_cust,
    industrial_file,
    rate_scenario,
    trans_cost_balance_method=None,
):
    """Determines the prices that ensure enough revenue is collected to recover the 
    DSO's expenses.
    Args:
        case_path (str): A string specifying the directory path of the case being analyzed.
        base_case_path (str): A string specifying the directory path of the base_case being used as a reference.
        metadata (dict): A dictionary containing the metadata structure of the DSO.
        meter_df (pandas.DataFrame): DataFrame containing consumers' consumption information.
        trans_df (pandas.DataFrame): DataFrame containing consumers' transactive consumption
        information.
        energy_sum_df (pandas.DataFrame): DataFrame containing consumption information for 
        each consumer class.
        tariff (dict): A dictionary of pertinant tariff information. Includes information 
        for the volumetric rates (i.e., flat and time-of-use).
        dso_num (str): A string specifying the number of the DSO being considered.
        sf (float): Scaling factor to scale the GridLAB-D results to TSO scale.
        num_ind_cust (int): Number of industrial consumers.
        industrial_file (str): File path to the bulk industrial loads.
        rate_scenario (str): A str specifying the rate scenario under investigation: flat,
        time-of-use, subscription, transactive, or dsot.
        trans_cost_balance_method (str): A str indicating the cost component of the 
        transactive rate that will be adjusted to recover all unmet costs.
    Returns:
        prices (dict): A dictionary containing the prices that need to be calculated for 
        each of the rates considered in the rate scenario.
    """

    # Determine the months under consideration
    months = list(meter_df.columns[~meter_df.columns.str.contains("sum")])
    # TODO: Remove column renaming once consistent month names are implemented earlier in rate-making code.
    monthsdict = {}

    for i in range(len(months)):
        monthsdict[months[i]] = months[i][:3]
        months[i] = months[i][:3]

    meter_df.rename(columns=monthsdict, inplace=True)
    energy_sum_df.rename(columns=monthsdict, inplace=True)
    trans_df.rename(columns=monthsdict, inplace=True)

    # Specify price components that do not vary in time or by consumer type
    fixed_charge = tariff["DSO_" + dso_num]["base_connection_charge"]
    trans_retail_scale = tariff["DSO_" + dso_num]["transactive_LMP_multiplier"]

    # Initialize the prices dictionary
    prices = {}

    # Determine the prices that ensure enough revenue is collected to recover the DSO's
    # expenses for each rate considered in the respective Rate Scenario
    if rate_scenario == "flat":
        # Obtain the DSO expenses (e.g., operational expenditures, capital expenditures)
        dso_expenses = get_total_dso_costs(case_path, dso_num, rate_scenario)

        # Initialize some of the closed-form solution components
        total_consumption_rc = 0
        rev_demand_charge_rc = 0
        rev_fixed_charge_rc = 0
        total_tier_credit_rc = 0

        # Iterate through each consumer to find certain components
        for each in metadata["billingmeters"]:
            # Calculate the necessary rate components for residential and commercial
            # consumers
            if metadata["billingmeters"][each]["tariff_class"] in [
                "residential",
                "commercial",
            ]:
                # Update total consumption
                total_consumption_rc += meter_df.loc[(each, "kw-hr"), "sum"]

                # Specify the demand charge based on the consumer's sector type
                demand_charge = tariff["DSO_" + dso_num][
                    metadata["billingmeters"][each]["tariff_class"]
                ]["demand_charge"]

                # Update total revenue from demand charges
                rev_demand_charge_rc += demand_charge * sum(
                    meter_df.loc[(each, "max_kw"), m] for m in months
                )

                # Update total revenue from fixed charges
                rev_fixed_charge_rc += fixed_charge * len(months)

                # Update the total tier credit, if the consumer qualifies
                if metadata["billingmeters"][each]["tariff_class"] in [
                    "residential",
                    "commercial",
                ]:
                    total_tier_credit_rc += sum(
                        calculate_tier_credit(
                            dso_num,
                            metadata["billingmeters"][each]["tariff_class"],
                            tariff,
                            meter_df.loc[(each, "kw-hr"), m],
                        )
                        for m in months
                    )

        # Calculate the necessary rate components for industrial consumers
        total_consumption_i = energy_sum_df.loc[("industrial", "kw-hr"), "sum"]
        rev_demand_charge_i = tariff["DSO_" + dso_num]["industrial"][
            "demand_charge"
        ] * sum(energy_sum_df.loc[("industrial", "demand_quantity"), m] for m in months)
        rev_fixed_charge_i = fixed_charge * len(months) * num_ind_cust
        total_tier_credit_i = sum(
            calculate_tier_credit(
                dso_num,
                "industrial",
                tariff,
                energy_sum_df.loc[("industrial", "kw-hr"), m],
            )
            for m in months
        )
        
        # Find the energy price for the flat rate
        prices["flat_rate"] = (
            dso_expenses
            - sf * (rev_demand_charge_rc + rev_fixed_charge_rc + total_tier_credit_rc)
            - rev_demand_charge_i
            - rev_fixed_charge_i
            - total_tier_credit_i
        ) / (sf * total_consumption_rc + total_consumption_i)
    elif rate_scenario == "time-of-use":
        # Load in necessary data for the time-of-use rate
        tou_params = load_json(case_path, "time_of_use_parameters.json")

        # Determine the seasons under consideration in the time-of-use rate
        seasons_dict = {}
        for m in months:
            if tou_params["DSO_" + dso_num][m]["season"] in seasons_dict:
                seasons_dict[tou_params["DSO_" + dso_num][m]["season"]].append(m)
            else:
                seasons_dict[tou_params["DSO_" + dso_num][m]["season"]] = [m]

        # Obtain the DSO expenses (e.g., operational expenditures, capital expenditures)
        dso_expenses = get_total_dso_costs(
            case_path, dso_num, rate_scenario, seasons_dict
        )

        # Initialize some of the closed-form solution components
        total_weighted_consumption_tou_rc = {s: 0 for s in seasons_dict}
        total_weighted_consumption_tou_i = {s: 0 for s in seasons_dict}
        rev_demand_charge_tou_rc = {s: 0 for s in seasons_dict}
        rev_demand_charge_tou_i = {s: 0 for s in seasons_dict}
        rev_fixed_charge_tou_rc = {s: 0 for s in seasons_dict}
        rev_fixed_charge_tou_i = {s: 0 for s in seasons_dict}
        total_tier_credit_tou_rc = {s: 0 for s in seasons_dict}
        total_tier_credit_tou_i = {s: 0 for s in seasons_dict}

        # Iterate through each consumer as if they are all participating under 
        # the time-of-use rate
        for s in seasons_dict:
            for each in metadata["billingmeters"]:
                # Calculate the necessary rate components for residential and commercial
                # consumers
                if metadata["billingmeters"][each]["tariff_class"] in [
                    "residential",
                    "commercial",
                ]:
                    # Update the total consumption for each consumer during each season
                    total_weighted_consumption_tou_rc[s] += sum(
                        sum(
                            tou_params["DSO_" + dso_num][m]["periods"][k]["ratio"]
                            * meter_df.loc[(each, k + "_kwh"), m]
                            for m in seasons_dict[s]
                        )
                        for k in tou_params["DSO_" + dso_num][m]["periods"].keys()
                    )

                    # Specify the demand charge based on the consumer's sector type
                    demand_charge = tariff["DSO_" + dso_num][
                        metadata["billingmeters"][each]["tariff_class"]
                    ]["demand_charge"]

                    # Update total revenue from demand charges for each consumer during 
                    # each season
                    rev_demand_charge_tou_rc[s] += demand_charge * sum(
                        meter_df.loc[(each, "max_kw"), m] for m in seasons_dict[s]
                    )

                    # Update total revenue from fixed charges for each consumer during 
                    # each season
                    rev_fixed_charge_tou_rc[s] += fixed_charge * len(seasons_dict[s])

                    # Update the total tier credit for each consumer during each season, 
                    # if the consumer qualifies
                    if metadata["billingmeters"][each]["tariff_class"] in [
                        "residential",
                        "commercial",
                    ]:
                        total_tier_credit_tou_rc[s] += sum(
                            calculate_tier_credit(
                                dso_num,
                                metadata["billingmeters"][each]["tariff_class"],
                                tariff,
                                meter_df.loc[(each, "kw-hr"), m],
                            )
                            for m in seasons_dict[s]
                        )

            # Calculate the necessary rate components for industrial consumers
            total_weighted_consumption_tou_i[s] += sum(
                sum(
                    tou_params["DSO_" + dso_num][m]["periods"][k]["ratio"]
                    * energy_sum_df.loc[("industrial", k + "_kwh"), m]
                    for m in seasons_dict[s]
                )
                for k in tou_params["DSO_" + dso_num][m]["periods"].keys()
            )
            rev_demand_charge_tou_i[s] = tariff["DSO_" + dso_num]["industrial"][
                "demand_charge"
            ] * sum(
                energy_sum_df.loc[("industrial", "demand_quantity"), m]
                for m in seasons_dict[s]
            )
            rev_fixed_charge_tou_i[s] = (
                fixed_charge * len(seasons_dict[s]) * num_ind_cust
            )
            total_tier_credit_tou_i[s] = sum(
                calculate_tier_credit(
                    dso_num,
                    "industrial",
                    tariff,
                    energy_sum_df.loc[("industrial", "kw-hr"), m],
                )
                for m in seasons_dict[s]
            )

            # Find the off-peak energy price for each season for the time-of-use rate,
            # assuming that each consumer is taking service under the time-of-use rate
            prices["tou_rate_" + s] = (
                dso_expenses[s]
                - sf
                * (
                    rev_demand_charge_tou_rc[s]
                    + rev_fixed_charge_tou_rc[s]
                    + total_tier_credit_tou_rc[s]
                )
                - rev_demand_charge_tou_i[s]
                - rev_fixed_charge_tou_i[s]
                - total_tier_credit_tou_i[s]
            ) / (
                sf * total_weighted_consumption_tou_rc[s]
                + total_weighted_consumption_tou_i[s]
            )

        # Initialize some of the closed-form solution components
        total_consumption_flat_rc = 0
        rev_energy_charge_tou = {s: 0 for s in seasons_dict}
        rev_demand_charge_flat_rc = 0
        rev_demand_charge_tou = {s: 0 for s in seasons_dict}
        rev_fixed_charge_flat_rc = 0
        rev_fixed_charge_tou = {s: 0 for s in seasons_dict}
        total_tier_credit_flat_rc = 0

        # Iterate through each consumer to allocate costs according to the tariff under 
        # which they take service
        for each in metadata["billingmeters"]:
            # Calculate the necessary rate components for residential and commercial
            # consumers
            if metadata["billingmeters"][each]["tariff_class"] in [
                "residential",
                "commercial",
            ]:
                if metadata["billingmeters"][each]["cust_participating"]:
                    for s in seasons_dict:
                        # Update the total revenue from energy charges for time-of-use
                        # consumers during each season
                        rev_energy_charge_tou[s] += sum(
                            sum(
                                prices["tou_rate_" + s]
                                * tou_params["DSO_" + dso_num][m]["periods"][k]["ratio"]
                                * meter_df.loc[(each, k + "_kwh"), m]
                                for m in seasons_dict[s]
                            )
                            for k in tou_params["DSO_" + dso_num][m]["periods"].keys()
                        )

                        # Calculate the consumer's tier credit (due to the declining 
                        # block rate), if the consumer is eligible
                        if metadata["billingmeters"][each]["tariff_class"] in [
                            "residential",
                            "commercial",
                        ]:
                            rev_energy_charge_tou[s] += sum(
                                calculate_tier_credit(
                                    dso_num,
                                    metadata["billingmeters"][each]["tariff_class"],
                                    tariff,
                                    meter_df.loc[(each, "kw-hr"), m],
                                )
                                for m in seasons_dict[s]
                            )

                        # Specify the demand charge based on the consumer's sector type
                        demand_charge = tariff["DSO_" + dso_num][
                            metadata["billingmeters"][each]["tariff_class"]
                        ]["demand_charge"]

                        # Update total revenue from demand charges for time-of-use 
                        # consumers during each season
                        rev_demand_charge_tou[s] += demand_charge * sum(
                            meter_df.loc[(each, "max_kw"), m] for m in seasons_dict[s]
                        )

                        # Update total revenue from fixed charges for time-of-use 
                        # consumers during each season
                        rev_fixed_charge_tou[s] += fixed_charge * len(seasons_dict[s])
                else:
                    # Update total consumption for the flat rate consumers
                    total_consumption_flat_rc += meter_df.loc[(each, "kw-hr"), "sum"]

                    # Specify the demand charge based on the consumer's sector type
                    demand_charge = tariff["DSO_" + dso_num][
                        metadata["billingmeters"][each]["tariff_class"]
                    ]["demand_charge"]

                    # Update total revenue from demand charges for the flat rate 
                    # consumers
                    rev_demand_charge_flat_rc += demand_charge * sum(
                        meter_df.loc[(each, "max_kw"), m] for m in months
                    )

                    # Update total revenue from fixed charges for the flat rate 
                    # consumers
                    rev_fixed_charge_flat_rc += fixed_charge * len(months)

                    # Update the total tier credit for the flat rate consumers, if the 
                    # consumer qualifies
                    if metadata["billingmeters"][each]["tariff_class"] in [
                        "residential",
                        "commercial",
                    ]:
                        total_tier_credit_flat_rc += sum(
                            calculate_tier_credit(
                                dso_num,
                                metadata["billingmeters"][each]["tariff_class"],
                                tariff,
                                meter_df.loc[(each, "kw-hr"), m],
                            )
                            for m in months
                        )

        # Calculate the necessary rate components for industrial consumers
        total_consumption_flat_i = energy_sum_df.loc[("industrial", "kw-hr"), "sum"]
        rev_demand_charge_flat_i = tariff["DSO_" + dso_num]["industrial"][
            "demand_charge"
        ] * sum(energy_sum_df.loc[("industrial", "demand_quantity"), m] for m in months)
        rev_fixed_charge_flat_i = fixed_charge * len(months) * num_ind_cust
        total_tier_credit_flat_i = sum(
            calculate_tier_credit(
                dso_num,
                "industrial",
                tariff,
                energy_sum_df.loc[("industrial", "kw-hr"), m],
            )
            for m in months
        )

        # Calculate the total revenue obtained from consumers taking service under the 
        # time-of-use rate
        rev_total_tou = sum(
            rev_energy_charge_tou[s]
            + rev_demand_charge_tou[s]
            + rev_fixed_charge_tou[s]
            for s in seasons_dict
        )
            
        # Find the energy price for the flat rate
        prices["flat_rate"] = (
            sum(dso_expenses[s] for s in seasons_dict)
            - sf
            * (
                rev_total_tou
                + rev_demand_charge_flat_rc
                + rev_fixed_charge_flat_rc
                + total_tier_credit_flat_rc
            )
            - rev_demand_charge_flat_i
            - rev_fixed_charge_flat_i
            - total_tier_credit_flat_i
        ) / (sf * total_consumption_flat_rc + total_consumption_flat_i)
    elif rate_scenario == "subscription":
        # Load in necessary data for the time-of-use rate
        tou_params = load_json(case_path, "time_of_use_parameters.json")

        # Create a mapping between month name and month number
        month_map = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12",
        }

        # Determine the seasons under consideration in the time-of-use rate
        seasons_dict = {}
        for m in months:
            if tou_params["DSO_" + dso_num][m]["season"] in seasons_dict:
                seasons_dict[tou_params["DSO_" + dso_num][m]["season"]].append(m)
            else:
                seasons_dict[tou_params["DSO_" + dso_num][m]["season"]] = [m]

        # Obtain the DSO expenses (e.g., operational expenditures, capital expenditures)
        dso_expenses = get_total_dso_costs(
            case_path, dso_num, rate_scenario, seasons_dict
        )

        # Load in the market data and convert to $/kWh
        da_lmp_stats = (
            pd.read_csv(
                os.path.join(case_path, "Annual_DA_LMP_Load_data.csv"), index_col=0
            )
            / 1000
        )

        # Initialize the demand and baseline demand profiles for their seasonal 
        # aggregation
        demand_df = {s: 0 for s in seasons_dict}
        bl_demand_df = {s: 0 for s in seasons_dict}

        # Initialize some of the closed-form solution components
        total_weighted_consumption_sub_rc = {s: 0 for s in seasons_dict}
        total_weighted_consumption_sub_i = {s: 0 for s in seasons_dict}
        total_unweighted_consumption_sub_i = {
            s: {m: 0 for m in seasons_dict[s]} for s in seasons_dict
        }
        rev_net_deviation_charge_sub_rc = {s: 0 for s in seasons_dict}
        rev_net_deviation_charge_sub_i = {s: 0 for s in seasons_dict}
        rev_demand_charge_sub_rc = {s: 0 for s in seasons_dict}
        rev_demand_charge_sub_i = {s: 0 for s in seasons_dict}
        rev_fixed_charge_sub_rc = {s: 0 for s in seasons_dict}
        rev_fixed_charge_sub_i = {s: 0 for s in seasons_dict}
        total_tier_credit_sub_rc = {s: 0 for s in seasons_dict}
        total_tier_credit_sub_i = {s: 0 for s in seasons_dict}

        # Iterate through each seasons that makes up separate TOU rates for the base subscription
        for s in seasons_dict:
            # Load in and combine the hourly baseline demand profiles and the hourly 
            # demand profiles for each month in the season being considered
            for m in seasons_dict[s]:
                if m == seasons_dict[s][0]:
                    bl_demand_df[s] = pd.read_hdf(
                        os.path.join(
                            base_case_path,
                            [
                                p
                                for p in os.listdir(case_path)
                                if len(p)>10
                                    if p[7:9] == month_map[m]
                            ][0],
                            "Substation_" + dso_num,
                            "Substation_" + dso_num + "_baseline_demand_by_meter.h5",
                        ),
                        key="demand",
                        mode="r",
                        # format="table",
                    )
                    demand_df[s] = pd.read_hdf(
                        os.path.join(
                            case_path,
                            [
                                p
                                for p in os.listdir(case_path)
                                if len(p)>10
                                    if p[7:9] == month_map[m]
                            ][0],
                            "Substation_" + dso_num,
                            "Substation_" + dso_num + "_demand_by_meter.h5",
                        ),
                        key="demand",
                        mode="r",
                    )
                else:
                    bl_demand_df[s] = pd.concat(
                        [
                            bl_demand_df[s],
                            pd.read_hdf(
                                os.path.join(
                                    base_case_path,
                                    [
                                        p
                                        for p in os.listdir(case_path)
                                        if len(p) > 10
                                            if p[7:9] == month_map[m]
                                    ][0],
                                    "Substation_" + dso_num,
                                    "Substation_"
                                    + dso_num
                                    + "_baseline_demand_by_meter.h5",
                                ),
                                key="demand",
                                mode="r",
                            ),
                        ]
                    )
                    demand_df[s] = pd.concat(
                        [
                            demand_df[s],
                            pd.read_hdf(
                                os.path.join(
                                    case_path,
                                    [
                                        p
                                        for p in os.listdir(case_path)
                                        if len(p) > 10
                                            if p[7:9] == month_map[m]
                                    ][0],
                                    "Substation_" + dso_num,
                                    "Substation_" + dso_num + "_demand_by_meter.h5",
                                ),
                                key="demand",
                                mode="r",
                            ),
                        ]
                    )

            # For each customer calculate the necessary rate components for the metered consumers
            for each in metadata["billingmeters"]:
                if metadata["billingmeters"][each]["tariff_class"] in [
                    "residential",
                    "commercial",
                ]:
                    # Update the total weighted consumption for each residential and
                    # commercial consumer during each season
                    total_weighted_consumption_sub_rc[s] += sum(
                        tou_params["DSO_" + dso_num][seasons_dict[s][0]]["periods"][k][
                            "ratio"
                        ]
                        * sum(
                            bl_demand_df[s]
                            .loc[:, each]
                            .between_time(
                                str(
                                    tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                        "periods"
                                    ][k]["hour_start"][h]
                                )
                                + ":00",
                                str(
                                    tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                        "periods"
                                    ][k]["hour_end"][h]
                                )
                                + ":00"
                                if tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                    "periods"
                                ][k]["hour_end"][h]
                                != 24
                                else "0:00",
                                inclusive="left",
                            )
                            .sum()
                            for h in range(
                                len(
                                    tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                        "periods"
                                    ][k]["hour_start"]
                                )
                            )
                        )
                        for k in tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                            "periods"
                        ].keys()
                    )

                    # Update the total revenue from demand charges for each residential
                    # and commercial consumer during each season
                    rev_demand_charge_sub_rc[s] += tariff["DSO_" + dso_num][
                        "industrial"
                    ]["demand_charge"] * sum(
                        bl_demand_df[s][
                            bl_demand_df[s].index.month == int(month_map[m])
                        ]
                        .loc[:, each]
                        .max()
                        for m in seasons_dict[s]
                    )

                    # Update total revenue from fixed charges for each residential and 
                    # commercial consumer during each season
                    rev_fixed_charge_sub_rc[s] += fixed_charge * len(seasons_dict[s])

                    # Update the total revenue from the net deviation charges for each
                    # residential and commercial consumer during each season
                    # TODO: Incorporate dynamic capital cost recovery price
                    rev_net_deviation_charge_sub_rc[s] += sum(
                        da_lmp_stats.loc[str(t), "da_lmp" + dso_num]
                        * (demand_df[s].loc[t, each] - bl_demand_df[s].loc[t, each])
                        for t in demand_df[s].index
                    )

                    # Update the total tier credit for each consumer during each season,
                    # if the consumer qualifies
                    if metadata["billingmeters"][each]["tariff_class"] in [
                        "residential",
                        "commercial",
                    ]:
                        total_tier_credit_sub_rc[s] += sum(
                            calculate_tier_credit(
                                dso_num,
                                metadata["billingmeters"][each]["tariff_class"],
                                tariff,
                                bl_demand_df[s][
                                    bl_demand_df[s].index.month == int(month_map[m])
                                ]
                                .loc[:, each]
                                .sum(),
                            )
                            for m in seasons_dict[s]
                        )
                elif metadata["billingmeters"][each]["tariff_class"] == "industrial":
                    # Update the total weighted consumption for each industrial consumer
                    # during each season
                    total_weighted_consumption_sub_i[s] += sum(
                        tou_params["DSO_" + dso_num][seasons_dict[s][0]]["periods"][k][
                            "ratio"
                        ]
                        * sum(
                            bl_demand_df[s]
                            .loc[:, each]
                            .between_time(
                                str(
                                    tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                        "periods"
                                    ][k]["hour_start"][h]
                                )
                                + ":00",
                                str(
                                    tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                        "periods"
                                    ][k]["hour_end"][h]
                                )
                                + ":00"
                                if tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                    "periods"
                                ][k]["hour_end"][h]
                                != 24
                                else "0:00",
                                inclusive="left",
                            )
                            .sum()
                            for h in range(
                                len(
                                    tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                        "periods"
                                    ][k]["hour_start"]
                                )
                            )
                        )
                        for k in tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                            "periods"
                        ].keys()
                    )

                    # Specify the demand charge based on the consumer's sector type
                    demand_charge = tariff["DSO_" + dso_num][
                        metadata["billingmeters"][each]["tariff_class"]
                    ]["demand_charge"]

                    # Update the total revenue from demand charges for each industrial
                    # consumer during each season
                    rev_demand_charge_sub_i[s] += demand_charge * sum(
                        bl_demand_df[s][bl_demand_df[s].index.month == int(month_map[m])]
                        .loc[:, each]
                        .max()
                        for m in seasons_dict[s]
                    )

                    # Update the total revenue from the net deviation charges for each
                    # industrial consumer during each season
                    # TODO: Incorporate dynamic capital cost recovery price
                    rev_net_deviation_charge_sub_i[s] += sum(
                        da_lmp_stats.loc[str(t), "da_lmp" + dso_num]
                        * (demand_df[s].loc[t, each] - bl_demand_df[s].loc[t, each])
                        for t in demand_df[s].index
                    )

                    # Update the total unweighted consumption for each industrial
                    # consumer during each month of each season
                    for m in seasons_dict[s]:
                        total_unweighted_consumption_sub_i[s][m] += (
                            bl_demand_df[s][bl_demand_df[s].index.month == int(month_map[m])]
                            .loc[:, each]
                            .sum()
                        )

            # Calculate the necessary rate components for industrial consumers
            indust_df = load_indust_data(industrial_file, range(1, 2)) * 1000
            for k in tou_params["DSO_" + dso_num][seasons_dict[s][0]]["periods"].keys():
                num_hours = 0
                for i in range(len(tou_params["DSO_" + dso_num][seasons_dict[s][0]]["periods"][k]["hour_start"])):
                    num_hours += (
                        tou_params["DSO_" + dso_num][seasons_dict[s][0]]["periods"][k]["hour_end"][i]
                        - tou_params["DSO_" + dso_num][seasons_dict[s][0]]["periods"][k]["hour_start"][i]
                    )
                total_weighted_consumption_sub_i[s] += (
                    tou_params["DSO_" + dso_num][seasons_dict[s][0]]["periods"][k]["ratio"]
                    * indust_df.loc[0, "Bus" + dso_num]
                    * bl_demand_df[s].shape[0]
                    * num_hours / 24
                )
            rev_demand_charge_sub_i[s] += (
                tariff["DSO_" + dso_num]["industrial"]["demand_charge"]
                * len(seasons_dict[s])
                * indust_df.loc[0, "Bus" + dso_num]
            )
            rev_fixed_charge_sub_i[s] = fixed_charge * len(seasons_dict) * num_ind_cust
            total_tier_credit_sub_i[s] = sum(
                calculate_tier_credit(
                    dso_num,
                    "industrial",
                    tariff,
                    total_unweighted_consumption_sub_i[s][m]
                    + bl_demand_df[s][
                        bl_demand_df[s].index.month == int(month_map[m])
                    ].shape[0]
                    * indust_df.loc[0, "Bus" + dso_num],
                )
                for m in seasons_dict[s]
            )


            # Find the off-peak energy price for each season for the time-of-use rate,
            # assuming that each consumer is taking service under the subscription rate
            prices["subscription_rate_" + s] = (
                dso_expenses[s]
                - sf
                * (
                    rev_net_deviation_charge_sub_rc[s]
                    + rev_demand_charge_sub_rc[s]
                    + rev_fixed_charge_sub_rc[s]
                    + total_tier_credit_sub_rc[s])
                -(
                    rev_net_deviation_charge_sub_i[s]
                    + rev_demand_charge_sub_i[s]
                    + rev_fixed_charge_sub_i[s]
                    + total_tier_credit_sub_i[s]
                )
            ) / (
                sf
                * total_weighted_consumption_sub_rc[s]
                    + total_weighted_consumption_sub_i[s]
            )

        # Initialize some of the closed-form solution components
        total_consumption_flat_rc = 0
        rev_energy_charge_sub = {s: 0 for s in seasons_dict}
        rev_demand_charge_flat_rc = 0
        rev_demand_charge_sub = {s: 0 for s in seasons_dict}
        rev_fixed_charge_flat_rc = 0
        rev_fixed_charge_sub = {s: 0 for s in seasons_dict}
        total_tier_credit_flat_rc = 0
        rev_net_deviation_charge_sub = {s: 0 for s in seasons_dict}

        # Iterate through each consumer to allocate costs according to the tariff under 
        # which they take service
        for each in metadata["billingmeters"]:
            # Calculate the necessary rate components for residential and commercial 
            # consumers
            if metadata["billingmeters"][each]["tariff_class"] in [
                "residential",
                "commercial",
            ]:
                if metadata["billingmeters"][each]["cust_participating"]:
                    for s in seasons_dict:
                        # Update the total revenue from the net deviation charges for 
                        # subscription consumers during each season
                        rev_net_deviation_charge_sub[s] += sum(
                            da_lmp_stats.loc[str(t), "da_lmp" + dso_num]
                            * (demand_df[s].loc[t, each] - bl_demand_df[s].loc[t, each])
                            for t in demand_df[s].index
                        )

                        # Update the total revenue from energy charges for subscription
                        # consumers durng each season
                        rev_energy_charge_sub[s] += sum(
                            prices["subscription_rate_" + s]
                            * tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                "periods"
                            ][k]["ratio"]
                            * sum(
                                bl_demand_df[s]
                                .loc[:, each]
                                .between_time(
                                    str(
                                        tou_params["DSO_" + dso_num][
                                            seasons_dict[s][0]
                                        ]["periods"][k]["hour_start"][h]
                                    )
                                    + ":00",
                                    str(
                                        tou_params["DSO_" + dso_num][
                                            seasons_dict[s][0]
                                        ]["periods"][k]["hour_end"][h]
                                    )
                                    + ":00"
                                    if tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                        "periods"
                                    ][k]["hour_end"][h]
                                    != 24
                                    else "0:00",
                                    inclusive="left",
                                )
                                .sum()
                                for h in range(
                                    len(
                                        tou_params["DSO_" + dso_num][
                                            seasons_dict[s][0]
                                        ]["periods"][k]["hour_start"]
                                    )
                                )
                            )
                            for k in tou_params["DSO_" + dso_num][seasons_dict[s][0]][
                                "periods"
                            ].keys()
                        )

                        # Calculate the consumer's tier credit (due to the declining 
                        # block rate), if the consumer is eligible
                        if metadata["billingmeters"][each]["tariff_class"] in [
                            "residential",
                            "commercial",
                        ]:
                            rev_energy_charge_sub[s] += sum(
                                calculate_tier_credit(
                                    dso_num,
                                    metadata["billingmeters"][each]["tariff_class"],
                                    tariff,
                                    bl_demand_df[s][
                                        bl_demand_df[s].index.month == int(month_map[m])
                                    ]
                                    .loc[:, each]
                                    .sum(),
                                )
                                for m in seasons_dict[s]
                            )

                        # Specify the demand charge based on the consumer's sector type
                        demand_charge = tariff["DSO_" + dso_num][
                            metadata["billingmeters"][each]["tariff_class"]
                        ]["demand_charge"]

                        # Update the total revenue from demand charges for subscription
                        # consumers during each season
                        rev_demand_charge_sub[s] += demand_charge * sum(
                            bl_demand_df[s][
                                bl_demand_df[s].index.month == int(month_map[m])
                            ]
                            .loc[:, each]
                            .max()
                            for m in seasons_dict[s]
                        )

                        # Update total revenue from fixed charges for subscription 
                        # consumers during each season
                        rev_fixed_charge_sub[s] += fixed_charge * len(seasons_dict[s])
                else:
                     # Update total consumption for the flat rate consumers
                    total_consumption_flat_rc += meter_df.loc[(each, "kw-hr"), "sum"]

                    # Specify the demand charge based on the consumer's sector type
                    demand_charge = tariff["DSO_" + dso_num][
                        metadata["billingmeters"][each]["tariff_class"]
                    ]["demand_charge"]

                    # Update total revenue from demand charges for the flat rate 
                    # consumers
                    rev_demand_charge_flat_rc += demand_charge * sum(
                        meter_df.loc[(each, "max_kw"), m] for m in months
                    )

                    # Update total revenue from fixed charges for the flat rate 
                    # consumers
                    rev_fixed_charge_flat_rc += fixed_charge * len(months)

                    # Update the total tier credit for the flat rate consumers, if the 
                    # consumer qualifies
                    if metadata["billingmeters"][each]["tariff_class"] in [
                        "residential",
                        "commercial",
                    ]:
                        total_tier_credit_flat_rc += sum(
                            calculate_tier_credit(
                                dso_num,
                                metadata["billingmeters"][each]["tariff_class"],
                                tariff,
                                meter_df.loc[(each, "kw-hr"), m],
                            )
                            for m in months
                        )

        # Calculate the necessary rate components for industrial consumers
        total_consumption_flat_i = energy_sum_df.loc[("industrial", "kw-hr"), "sum"]
        rev_demand_charge_flat_i = tariff["DSO_" + dso_num]["industrial"][
            "demand_charge"
        ] * sum(energy_sum_df.loc[("industrial", "demand_quantity"), m] for m in months)
        rev_fixed_charge_flat_i = fixed_charge * len(months) * num_ind_cust
        total_tier_credit_flat_i = sum(
            calculate_tier_credit(
                dso_num,
                "industrial",
                tariff,
                energy_sum_df.loc[("industrial", "kw-hr"), m],
            )
            for m in months
        )

        # Calculate the total revenue obtained from consumers taking service under the 
        # subscription rate
        rev_total_sub = sum(
            rev_net_deviation_charge_sub[s]
            + rev_energy_charge_sub[s]
            + rev_demand_charge_sub[s]
            + rev_fixed_charge_sub[s]
            for s in seasons_dict
        )

        # Find the energy price for the flat rate
        prices["flat_rate"] = (
            sum(dso_expenses[s] for s in seasons_dict)
            - sf
            * (
                rev_total_sub
                + rev_demand_charge_flat_rc
                + rev_fixed_charge_flat_rc
                + total_tier_credit_flat_rc
            )
            - rev_demand_charge_flat_i
            - rev_fixed_charge_flat_i
            - total_tier_credit_flat_i
        ) / (sf * total_consumption_flat_rc + total_consumption_flat_i)
    elif rate_scenario == "transactive":
        # Load in necessary data for the transactive rate
        if trans_cost_balance_method in [None, "volumetric"]:
            trans_fixed_charge = tariff["DSO_" + dso_num]["transactive_connection_charge"]
        elif trans_cost_balance_method == "fixed":
            trans_vol_charge = tariff["DSO_" + dso_num]["transactive_dist_rate"]

        # Obtain the DSO expenses (e.g., operational expenditures, capital expenditures)
        dso_expenses = get_total_dso_costs(case_path, dso_num, rate_scenario)

        # Initialize some of the closed-form solution components
        total_consumption_trans_rc = 0
        total_consumption_trans_i = 0
        total_consumers_trans_rc = 0
        total_consumers_trans_i = 0
        rev_DA_energy_charge_trans_rc = 0
        rev_DA_energy_charge_trans_i = 0
        rev_RT_energy_charge_trans_rc = 0
        rev_RT_energy_charge_trans_i = 0
        rev_volumetric_charge_trans_rc = 0
        rev_volumetric_charge_trans_i = 0
        rev_fixed_charge_trans_rc = 0
        rev_fixed_charge_trans_i = 0

        # Iterate through each consumer to find certain components
        for each in metadata["billingmeters"]:
            # Calculate the necessary rate components for residential and commercial 
            # consumers
            if metadata["billingmeters"][each]["tariff_class"] in ["residential", "commercial"]:
                if trans_cost_balance_method in [None, "volumetric"]:
                    # Update the total consumption
                    total_consumption_trans_rc += meter_df.loc[(each, "kw-hr"), "sum"]

                    # Update the total revenue from fixed charges
                    rev_fixed_charge_trans_rc += trans_fixed_charge * len(months)
                elif trans_cost_balance_method == "fixed":
                    # Update the total number of consumers
                    total_consumers_trans_rc += 1

                    # Update the total revenue from volumetric charges
                    rev_volumetric_charge_trans_rc += (
                        meter_df.loc[(each, "kw-hr"), "sum"] * trans_vol_charge
                    )

                # Update the total revenue from DA energy charges
                rev_DA_energy_charge_trans_rc += (
                    trans_df.loc[(each, "DA_cost"), "sum"] * trans_retail_scale
                )

                # Update the total revenue from RT energy charges
                rev_RT_energy_charge_trans_rc += (
                    trans_df.loc[(each, "RT_cost"), "sum"] * trans_retail_scale
                )
            elif metadata["billingmeters"][each]["tariff_class"] == "industrial":
                # Update the total revenue from DA energy charges
                rev_DA_energy_charge_trans_i += (
                    trans_df.loc[(each, "DA_cost"), "sum"] * trans_retail_scale
                )

                # Update the total revenue from RT energy charges
                rev_RT_energy_charge_trans_i += (
                    trans_df.loc[(each, "RT_cost"), "sum"] * trans_retail_scale
                )

        # Calculate the necessary rate components for industrial consumers
        if trans_cost_balance_method in [None, "volumetric"]:
            total_consumption_trans_i = energy_sum_df.loc[("industrial", "kw-hr"), "sum"]
            rev_fixed_charge_trans_i = trans_fixed_charge * len(months) * num_ind_cust
        elif trans_cost_balance_method == "fixed":
            total_consumers_trans_i = num_ind_cust
            rev_volumetric_charge_trans_i = (
                energy_sum_df.loc[("industrial", "kw-hr"), "sum"] * trans_vol_charge
            )
        da_lmp_stats = (
            pd.read_csv(
                os.path.join(case_path, "Annual_DA_LMP_Load_data.csv"), index_col=0
            )
            / 1000
        )
        indust_df = load_indust_data(industrial_file, range(1, 2)) * 1000
        rev_DA_energy_charge_trans_i += (
            indust_df.loc[0, "Bus" + dso_num]
            * da_lmp_stats.loc[:, "da_lmp" + dso_num].sum()
        )

        # Find the volumetric price or the fixed charge for the transactive rate,
        # assuming that each consumer is taking service under the transactive rate
        if trans_cost_balance_method in [None, "volumetric"]:
            prices["transactive_volumetric_rate"] = (
                dso_expenses
                - sf
                * (
                    rev_DA_energy_charge_trans_rc
                    + rev_RT_energy_charge_trans_rc
                    + rev_fixed_charge_trans_rc
                )
                - (
                    rev_fixed_charge_trans_i
                  + rev_DA_energy_charge_trans_i
                  + rev_RT_energy_charge_trans_i
                )
            ) / (sf * total_consumption_trans_rc + total_consumption_trans_i)
        elif trans_cost_balance_method == "fixed":
            prices["transactive_fixed_charge"] = (
                dso_expenses
                - sf
                * (
                    rev_DA_energy_charge_trans_rc
                    + rev_RT_energy_charge_trans_rc
                    + rev_volumetric_charge_trans_rc
                    + rev_DA_energy_charge_trans_i
                    + rev_RT_energy_charge_trans_i
                )
                - rev_volumetric_charge_trans_i
            ) / (12 * (sf * total_consumers_trans_rc + total_consumers_trans_i))

        # Initialize some of the closed-form solution components
        total_consumption_flat_rc = 0
        rev_demand_charge_flat_rc = 0
        rev_fixed_charge_flat_rc = 0
        total_tier_credit_flat_rc = 0
        rev_DA_energy_charge_trans = 0
        rev_RT_energy_charge_trans = 0
        rev_volumetric_charge_trans = 0
        rev_fixed_charge_trans = 0

        # Iterate through each consumer to allocate costs according to the tariff under 
        # which they take service
        for each in metadata["billingmeters"]:
            # Calculate the necessary rate components for residential and commercial
            # consumers
            if metadata["billingmeters"][each]["tariff_class"] in [
                "residential",
                "commercial",
            ]:
                if metadata["billingmeters"][each]["cust_participating"]:
                    # Calculate the consumer's market-related charges under the 
                    # transactive tariff
                    rev_DA_energy_charge_trans += (
                        trans_df.loc[(each, "DA_cost"), "sum"] * trans_retail_scale
                    )
                    rev_RT_energy_charge_trans += (
                        trans_df.loc[(each, "RT_cost"), "sum"] * trans_retail_scale
                    )

                    # Calculate the consumer's volumetric charge and fixed charge under
                    # the transactive tariff depending on the cost balance method
                    if trans_cost_balance_method in [None, "volumetric"]:
                        rev_volumetric_charge_trans += (
                            meter_df.loc[(each, "kw-hr"), "sum"]
                            * prices["transactive_volumetric_rate"]
                        )
                        rev_fixed_charge_trans += trans_fixed_charge * len(months)
                    elif trans_cost_balance_method == "fixed":
                        rev_volumetric_charge_trans += (
                            meter_df.loc[(each, "kw-hr"), "sum"] * trans_vol_charge
                        )
                        rev_fixed_charge_trans += prices["transactive_fixed_charge"]
                else:
                    # Update total consumption for the flat rate consumers
                    total_consumption_flat_rc += meter_df.loc[(each, "kw-hr"), "sum"]

                    # Specify the demand charge based on the consumer's sector type
                    demand_charge = tariff["DSO_" + dso_num][
                        metadata["billingmeters"][each]["tariff_class"]
                    ]["demand_charge"]

                    # Update total revenue from demand charges for the flat rate 
                    # consumers
                    rev_demand_charge_flat_rc += demand_charge * sum(
                        meter_df.loc[(each, "max_kw"), m] for m in months
                    )

                    # Update total revenue from fixed charges for the flat rate 
                    # consumers
                    rev_fixed_charge_flat_rc += fixed_charge * len(months)

                    # Update the total tier credit for the flat rate consumers, if the 
                    # consumer qualifies
                    if metadata["billingmeters"][each]["tariff_class"] in [
                        "residential",
                        "commercial",
                    ]:
                        total_tier_credit_flat_rc += sum(
                            calculate_tier_credit(
                                dso_num,
                                metadata["billingmeters"][each]["tariff_class"],
                                tariff,
                                meter_df.loc[(each, "kw-hr"), m],
                            )
                            for m in months
                        )

        # Calculate the necessary rate components for industrial consumers
        total_consumption_flat_i = energy_sum_df.loc[("industrial", "kw-hr"), "sum"]
        rev_demand_charge_flat_i = tariff["DSO_" + dso_num]["industrial"][
            "demand_charge"
        ] * sum(energy_sum_df.loc[("industrial", "demand_quantity"), m] for m in months)
        rev_fixed_charge_flat_i = fixed_charge * len(months) * num_ind_cust
        total_tier_credit_flat_i = sum(
            calculate_tier_credit(
                dso_num,
                "industrial",
                tariff,
                energy_sum_df.loc[("industrial", "kw-hr"), m],
            )
            for m in months
        )

        # Calculate the total revenue obtained from consumers taking service under the 
        # transactive rate
        rev_total_trans = (
            rev_DA_energy_charge_trans
            + rev_RT_energy_charge_trans
            + rev_volumetric_charge_trans
            + rev_fixed_charge_trans
        )
            
        # Find the energy price for the flat rate
        prices["flat_rate"] = (
            dso_expenses
            - sf
            * (
                rev_total_trans
                + rev_demand_charge_flat_rc
                + rev_fixed_charge_flat_rc
                + total_tier_credit_flat_rc
            )
            - rev_demand_charge_flat_i
            - rev_fixed_charge_flat_i
            - total_tier_credit_flat_i
        ) / (sf * total_consumption_flat_rc + total_consumption_flat_i)
    elif rate_scenario == "dsot":
        # Load in necessary data for the DSO+T rate
        trans_fixed_charge = tariff["DSO_" + dso_num]["transactive_connection_charge"]

        # Obtain the DSO expenses (e.g., operational expenditures, capital expenditures)
        dso_expenses = get_total_dso_costs(case_path, dso_num, rate_scenario)

        # Initialize some of the closed-form solution components
        total_consumption_dsot_rc = 0
        rev_DA_energy_charge_dsot_rc = 0
        rev_DA_energy_charge_dsot_i = 0
        rev_RT_energy_charge_dsot_rc = 0
        rev_RT_energy_charge_dsot_i = 0
        rev_fixed_charge_dsot_rc = 0

        # Iterate through each consumer to find certain components
        for each in metadata["billingmeters"]:
            # Calculate the necessary rate components for residential and commercial 
            # consumers
            if metadata["billingmeters"][each]["tariff_class"] in [
                "residential",
                "commercial",
            ]:
                # Update the total consumption
                total_consumption_dsot_rc += meter_df.loc[(each, "kw-hr"), "sum"]

                # Update the total revenue from fixed charges
                rev_fixed_charge_dsot_rc += trans_fixed_charge * len(months)

                # Update the total revenue from DA energy charges
                rev_DA_energy_charge_dsot_rc += (
                    trans_df.loc[(each, "DA_cost"), "sum"] * trans_retail_scale
                )

                # Update the total revenue from RT energy charges
                rev_RT_energy_charge_dsot_rc += (
                    trans_df.loc[(each, "RT_cost"), "sum"] * trans_retail_scale
                )
            elif metadata["billingmeters"][each]["tariff_class"] == "industrial":
                # Update the total revenue from DA energy charges
                rev_DA_energy_charge_dsot_i += (
                    trans_df.loc[(each, "DA_cost"), "sum"] * trans_retail_scale
                )

                # Update the total revenue from RT energy charges
                rev_RT_energy_charge_dsot_i += (
                    trans_df.loc[(each, "RT_cost"), "sum"] * trans_retail_scale
                )

        # Calculate the necessary rate components for industrial consumers
        total_consumption_dsot_i = energy_sum_df.loc[("industrial", "kw-hr"), "sum"]
        rev_fixed_charge_dsot_i = trans_fixed_charge * len(months) * num_ind_cust
        da_lmp_stats = (
            pd.read_csv(
                os.path.join(case_path, "Annual_DA_LMP_Load_data.csv"), index_col=0
            )
            / 1000
        )
        indust_df = load_indust_data(industrial_file, range(1, 2)) * 1000
        rev_DA_energy_charge_dsot_i += (
            indust_df.loc[0, "Bus" + dso_num]
            * da_lmp_stats.loc[:, "da_lmp" + dso_num].sum()
        )

        # Find the volumetric price for the DSO+T rate, assuming that each consumer is 
        # taking service under the DSO+T rate
        prices["dsot_volumetric_rate"] = (
            dso_expenses
            - sf
            * (
                rev_DA_energy_charge_dsot_rc
                + rev_RT_energy_charge_dsot_rc
                + rev_fixed_charge_dsot_rc
            )
            - (
                rev_fixed_charge_dsot_i
                + rev_DA_energy_charge_dsot_i
                + rev_RT_energy_charge_dsot_i
                )
        ) / (sf * total_consumption_dsot_rc + total_consumption_dsot_i)

        # Initialize some of the closed-form solution components
        total_consumption_flat_rc = 0
        rev_demand_charge_flat_rc = 0
        rev_fixed_charge_flat_rc = 0
        total_tier_credit_flat_rc = 0
        rev_DA_energy_charge_dsot = 0
        rev_RT_energy_charge_dsot = 0
        rev_volumetric_charge_dsot = 0
        rev_fixed_charge_dsot = 0

        # Iterate through each consumer to allocate costs according to the tariff under 
        # which they take service
        for each in metadata["billingmeters"]:
            # Calculate the necessary rate components for residential and commercial
            # consumers
            if metadata["billingmeters"][each]["tariff_class"] in [
                "residential",
                "commercial",
            ]:
                if metadata["billingmeters"][each]["cust_participating"]:
                    # Calculate the consumer's market-related charges under the DSO+T 
                    # tariff
                    rev_DA_energy_charge_dsot += (
                        trans_df.loc[(each, "DA_cost"), "sum"] * trans_retail_scale
                    )
                    rev_RT_energy_charge_dsot += (
                        trans_df.loc[(each, "RT_cost"), "sum"] * trans_retail_scale
                    )

                    # Calculate the consumer's volumetric charge under the DSO+T tariff
                    rev_volumetric_charge_dsot += (
                        meter_df.loc[(each, "kw-hr"), "sum"]
                        * prices["dsot_volumetric_rate"]
                    )

                    #Calculate the consumer's fixed charge under the DSO+T tariff
                    rev_fixed_charge_dsot += trans_fixed_charge * len(months)
                else:
                    # Update total consumption for the flat rate consumers
                    total_consumption_flat_rc += meter_df.loc[(each, "kw-hr"), "sum"]

                    # Specify the demand charge based on the consumer's sector type
                    demand_charge = tariff["DSO_" + dso_num][
                        metadata["billingmeters"][each]["tariff_class"]
                    ]["demand_charge"]

                    # Update total revenue from demand charges for the flat rate 
                    # consumers
                    rev_demand_charge_flat_rc += demand_charge * sum(
                        meter_df.loc[(each, "max_kw"), m] for m in months
                    )

                    # Update total revenue from fixed charges for the flat rate 
                    # consumers
                    rev_fixed_charge_flat_rc += fixed_charge * len(months)

                    # Update the total tier credit for the flat rate consumers, if the 
                    # consumer qualifies
                    if metadata["billingmeters"][each]["tariff_class"] in [
                        "residential",
                        "commercial",
                    ]:
                        total_tier_credit_flat_rc += sum(
                            calculate_tier_credit(
                                dso_num,
                                metadata["billingmeters"][each]["tariff_class"],
                                tariff,
                                meter_df.loc[(each, "kw-hr"), m],
                            )
                            for m in months
                        )

        # Calculate the necessary rate components for industrial consumers
        total_consumption_flat_i = energy_sum_df.loc[("industrial", "kw-hr"), "sum"]
        rev_demand_charge_flat_i = tariff["DSO_" + dso_num]["industrial"][
            "demand_charge"
        ] * sum(energy_sum_df.loc[("industrial", "demand_quantity"), m] for m in months)
        rev_fixed_charge_flat_i = fixed_charge * len(months) * num_ind_cust
        total_tier_credit_flat_i = sum(
            calculate_tier_credit(
                dso_num,
                "industrial",
                tariff,
                energy_sum_df.loc[("industrial", "kw-hr"), m],
            )
            for m in months
        )

        # Calculate the total revenue obtained from consumers taking service under the 
        # DSO+T rate
        rev_total_dsot = (
            rev_DA_energy_charge_dsot
            + rev_RT_energy_charge_dsot
            + rev_volumetric_charge_dsot
            + rev_fixed_charge_dsot
        )
            
        # Find the energy price for the flat rate
        prices["flat_rate"] = (
            dso_expenses
            - sf
            * (
                rev_total_dsot
                + rev_demand_charge_flat_rc
                + rev_fixed_charge_flat_rc
                + total_tier_credit_flat_rc
            )
            - rev_demand_charge_flat_i
            - rev_fixed_charge_flat_i
            - total_tier_credit_flat_i
        ) / (sf * total_consumption_flat_rc + total_consumption_flat_i)
    
    # Return the prices dictionary
    return prices


def get_total_dso_costs(case_path, dso_num, rate_scenario, seasons_dict=None):
    """Sets the DSO's expenses according to the rate scenario being considered. Uses an
    arbitrarily selected large value (that attempts to still be a similar order of 
    magnitude as the DSO's expected expenses) if the DSO CFS results have not been 
    calculated and stored.
    Args:
        case_path (str): A string specifying the directory path of the case being analyzed.
        dso_num (str):  A string specifying the number of the DSo being considered.
        rate_scenario (str): A str specifying the rate scenario under investigation: flat,
        time-of-use, subscription, or transactive.
        seasons_dict (dict): A dict specifying the seasons being considered and their 
        constituent months. Defaults to None.
    Returns:
        dso_expenses (float/dict): The DSO's total expenses, provided as a float, or the 
        seasonal expenses, provided as a dict.
    """

    # Try to read in the DSO CFS summary data
    try:
        dso_df = pd.read_csv(
            os.path.join(case_path, "DSO_CFS_Summary.csv"), index_col=0
        )
    except FileNotFoundError:
        print(
            "The DSO CFS summary data is not available. Will default to an arbitrarily "
            + "selected large value."
        )
        dso_df = None

    # Assign capital and operating expenses based on the rates being considered
    if rate_scenario == "flat":
        if dso_df is None:
            dso_expenses = 1e10
        else:
            dso_expenses = 1000 * (
                float(dso_df.loc["CapitalExpenses", "DSO_" + dso_num])
                + float(dso_df.loc["OperatingExpenses", "DSO_" + dso_num])
            )
    elif rate_scenario == "time-of-use":
        dso_expenses = {}
        num_seasons = len(seasons_dict)
        for s in seasons_dict:
            if dso_df is None:
                dso_expenses[s] = 1e10 / num_seasons
            else:
                dso_expenses[s] = 1000 * sum(
                    float(dso_df.loc["CapitalExpenses_" + m, "DSO_" + dso_num])
                    + float(dso_df.loc["OperatingExpenses_" + m, "DSO_" + dso_num])
                    for m in seasons_dict[s]
                )
    elif rate_scenario == "subscription":
        # Note that this assumes the subscription price is based on a time-of-use rate
        dso_expenses = {}
        num_seasons = len(seasons_dict)
        for s in seasons_dict:
            if dso_df is None:
                dso_expenses[s] = 1e10 / num_seasons
            else:
                dso_expenses[s] = 1000 * sum(
                    float(dso_df.loc["CapitalExpenses_" + m, "DSO_" + dso_num])
                    + float(dso_df.loc["OperatingExpenses_" + m, "DSO_" + dso_num])
                    for m in seasons_dict[s]
                )
    elif rate_scenario == "transactive":
        if dso_df is None:
            dso_expenses = 1e10
        else:
            dso_expenses = 1000 * (
                float(dso_df.loc["CapitalExpenses", "DSO_" + dso_num])
                + float(dso_df.loc["OperatingExpenses", "DSO_" + dso_num])
            )
    elif rate_scenario == "dsot":
        if dso_df is None:
            dso_expenses = 1e10
        else:
            dso_expenses = 1000 * (
                float(dso_df.loc["CapitalExpenses", "DSO_" + dso_num])
                + float(dso_df.loc["OperatingExpenses", "DSO_" + dso_num])
            )

    # Return the DSO's expenses
    return dso_expenses


# def calc_te_bill(metadata, meter_df, tariff):
    # """ Calculate the customer bill using realtime meter and agent bid data and transactive tariff structure.
    # Args:
    #     metadata (dict): metadata structure for the DSO to be analyzed
    #     meter_df (dataframe): monthly and total energy consumption and peak power by house (meter)
    #     tariff (dict): dictionary of fixed tariff structure
    # Returns:
    #     bill_df : dataframe of monthly and total bill for each house broken out by each element (energy, demand,
    #     connection, and total bill)
    #     """
    # Customer participation:
    # Need to determine if a customer is participating in transactive program or not
    # If not then their bill is calculated using the baseline equations and tariffs (I assume that is not safe to assume
    # that I can just pull the baseline values.  Better to recalculate)
    # Need to recalculate change in flat tariff for fixed customers similiar to baseline case.

    # Need to calculate the DA and Realtime price structure
    # DA price structure is:
    # DAP = A_da + LMP_da / 1000 + DMP_da + D + Delta_D
    # A_da = day ahead multiplier from tariff dictionary
    # LMP_da is the cleared price determined at 10 am as found in the dso_market 86400 file?
    # DMP_da = Retail_rate_da - LMP_da
    # D comes from tariff (needs to be assumed and then calculated to true up revenue).
    # Delta_D = to be determined peanut buttering of DMP_da charges as rebate.  Over year sum of DMP and Delta_D
    # should offset.  Offset should only go to folks on the feeder/substation affected.

    # RT price structure is:
    # RTP = A_rt + LMP_rt / 1000 + DMP_rt + D + Delta_D +Risk
    # A_rt = day ahead multiplier from tariff dictionary
    # LMP_rt is the realtime price as found in the dso_market 300 file?
    # DMP_rt = Retail_rate_da - LMP_da
    # Retail_rate_rt comes from price in the retail_market 300 file??
    # D comes from tariff (needs to be assumed and then calculated to true up revenue).
    # Delta_D = to be determined peanut buttering of DMP_rt charges as rebate to transactive customers.
    #           Over year sum of DMP and Delta_D
    # should offset
    # Risk = ????? average flat risk premium [$/kWh] for customers not making binding bids in day-ahead market.
    #   Will be set in tariff dictionary.  Since it is flat it will not affect agent behavior.

    # Calculation of DA and RT energy consumption at each 5 minute interval:
    # Q_da = sum of each agents day ahead commitment at 10 am.  Where does this come from ???????????
    # ###^^^^^ are these values hourly or 5 minute?
    # Q_rt = Meter_rt - Q_da

    # Calculation of energy bill:
    # for each day (then summing each day per month)
    # RTC =  RTP * Q_rt (product sum for the day)
    # DAC = DAP * Q_da (product sum for the day)
    # Flat_Charge = Q_total * D
    # Connection charge
    # Flat rebate = rebate to all on substation of congestion charge (do rebate retroactively monthly)
    # bill = RTC + DAC + Flat_C + Connection - Rebate
    # bill_2 = bill corrected with new flat rate for all rate payers on DSO to square up revenue with expenses.

    # data structure:
    # Energy:
    # energy bought DA
    # energy bought RT
    # peak power consumption (15 minute) for comparison to baseline
    # bill:
    # DA energy cost
    # DA congestion charge
    # RT energy cost
    # RT congestion charge
    # rebate charge
    # Flat energy charge
    # Connection Charge


def DSO_rate_making(
        case,
        base_case,
        dso_num,
        metadata,
        dso_expenses,
        tariff_path,
        dso_scaling_factor,
        num_indust_cust,
        case_name="",
        iterate=False,
        rate_scenario=None,
        trans_cost_balance_method=None,
):
    """ Main function to call for calculating the customer energy consumption, monthly bills, and tariff adjustments to
    ensure revenue matches expenses.  Saves meter and bill dataframes to a hdf5 file.
    Args:
        case (str): directory path for the case to be analyzed
        base_case (str): directory path for the base case containing baseline demand values
        dso_num (str): number of the DSO folder to be opened
        metadata:
        dso_expenses (TBD): dso expenses that need to be matched by customer revenue
        tariff_path:
        dso_scaling_factor (float): multiplier on customer bills to reflect the total number of customers in the DSO
        num_indust_cust (int): number of industrial customers
        case_name (str): name of the case ('MR-BAU', 'MR-Batt', 'MR-Flex', 'MR-BAU', 'MR-Batt', 'MR-Flex')
        iterate (Boolean): If True will iterate once to square up revenue.
        rate_scenario (str): A str specifying the rate scenario under investigation: flat,
        time-of-use, subscription, or transactive. If None, this function defaults to DSO+T.
        trans_cost_balance_method (str): A str indicating the cost component of the transactive 
        rate that will be adjusted to recover all unmet costs.
    Returns:
        meter_df : dataframe of energy consumption and max 15 minute power consumption for each month and total
        bill_df : dataframe of monthly and total bill for each house broken out by each element (energy, demand,
        connection, and total bill)
        tariff: Updated dictionary of tariff structure with rates adjusted to ensure revenue meets expenses
        surplus: dollar value difference between dso revenue and expenses.  When converged should be tiny (e.g. 1e-12)
        """

    counter_factual = False

    # Specify the Tariff file name for DSO+T-related scenarios
    if counter_factual:
        if case_name in ['8-MR-BAU', '8-MR-Batt', '8-MR-Flex']:
            file_name = 'rate_case_values_8-MR-BAU.json'
        elif case_name in ['8-HR-BAU', '8-HR-Batt', '8-HR-Flex']:
            file_name = 'rate_case_values_8-HR-BAU.json'
        elif case_name in ['200-MR-BAU', '200-MR-Batt', '200-MR-Flex']:
            file_name = 'rate_case_values_200-MR-BAU.json'
        elif case_name in ['200-HR-BAU', '200-HR-Batt', '200-HR-Flex']:
            file_name = 'rate_case_values_200-HR-BAU.json'
        else:
            raise Exception("Tariff rate case does not exist for case " + case_name + '.')
    else:
        file_name = 'rate_case_values_' + case_name + '.json'
    
    # Specify the Tariff file name for scenarios related to the rates scenarios project
    if (rate_scenario is not None) and (case_name == ""):
        file_name = "rate_case_values_" + rate_scenario + ".json"

    # Load Tariff structure
    tariff = load_json(tariff_path, file_name)

    # Load in transactive A values from simulation settings to ensure consistency
    default_config = load_json(tariff_path, 'default_case_config.json')
    for DSO in tariff:
        tariff[DSO]['transactive_LMP_multiplier'] = default_config['MarketPrep']['DSO']['dso_retail_scaling']

    energy_file = case + '/energy_dso_' + str(dso_num) + '_data.h5'
    trans_file = case + '/transactive_dso_' + str(dso_num) + '_data.h5'
    year_meter_df = pd.read_hdf(energy_file, key='energy_data', mode='r')
    year_energysum_df = pd.read_hdf(energy_file, key='energy_sums', mode='r')
    year_trans_df = pd.read_hdf(trans_file, key='trans_data', mode='r')

    if rate_scenario is None:
        if not counter_factual:
            if case_name not in ["8-MR-BAU", "8-HR-BAU", "200-MR-BAU", "200-HR-BAU"]:
                # Calculate the transactive volumetric rate as if all customers were participating:

                DA_Sales = (
                    year_trans_df.loc[(slice(None), "DA_cost"), "sum"].sum()
                    * dso_scaling_factor
                    * default_config["MarketPrep"]["DSO"]["dso_retail_scaling"]
                )
                RT_Sales = (
                    year_trans_df.loc[(slice(None), "RT_cost"), "sum"].sum()
                    * dso_scaling_factor
                    * default_config["MarketPrep"]["DSO"]["dso_retail_scaling"]
                )

                # Load in bulk industrial loads
                case_config = load_json(case, "generate_case_config.json")
                industrial_file = os.path.join(
                    tariff_path, case_config["indLoad"][5].split("/")[-1]
                )
                indust_df = load_indust_data(industrial_file, range(1, 2))
                da_lmp_stats = pd.read_csv(
                    case + "\\" + "Annual_DA_LMP_Load_data.csv", index_col=0
                )
                Indust_Sales = (
                    indust_df.loc[0, "Bus" + str(dso_num)]
                    * da_lmp_stats.loc[:, "da_lmp" + str(dso_num)].sum()
                )
                Customer_Count = 0
                for meter in metadata["billingmeters"]:
                    if metadata["billingmeters"][meter]["tariff_class"] in [
                        "residential",
                        "commercial",
                    ]:
                        Customer_Count += 1
                Connection_fees = tariff["DSO_" + str(dso_num)][
                    "base_connection_charge"
                ] * (num_indust_cust + dso_scaling_factor * Customer_Count)

                transactive_dist_rate = (
                    dso_expenses
                    - (DA_Sales + RT_Sales + Indust_Sales + Connection_fees)
                ) / year_energysum_df.loc[("total", "kw-hr"), "sum"]

                tariff["DSO_" + str(dso_num)][
                    "transactive_dist_rate"
                ] = transactive_dist_rate

                # Calculate the required revenue to be collected from non-participating customers.

                NP_Customer_Count = 0
                NP_DA_Sales = 0
                NP_RT_Sales = 0
                NP_Energy = 0
                for meter in metadata["billingmeters"]:
                    if (
                        metadata["billingmeters"][meter]["tariff_class"]
                        in ["residential", "commercial"]
                        and not metadata["billingmeters"][meter]["cust_participating"]
                    ):
                        NP_Customer_Count += 1
                        NP_DA_Sales += (
                            year_trans_df.loc[(meter, "DA_cost"), "sum"].sum()
                            * dso_scaling_factor
                            * default_config["MarketPrep"]["DSO"]["dso_retail_scaling"]
                        )
                        NP_RT_Sales += (
                            year_trans_df.loc[(meter, "RT_cost"), "sum"].sum()
                            * dso_scaling_factor
                            * default_config["MarketPrep"]["DSO"]["dso_retail_scaling"]
                        )
                        NP_Energy += (
                            year_meter_df.loc[(meter, "kw-hr"), "sum"].sum()
                            * dso_scaling_factor
                            * default_config["MarketPrep"]["DSO"]["dso_retail_scaling"]
                        )

                NP_Energy += (
                    indust_df.loc[0, "Bus" + str(dso_num)]
                    * 1000
                    * len(da_lmp_stats.loc[:, "da_lmp" + str(dso_num)])
                )
                NP_connection_fees = tariff["DSO_" + str(dso_num)][
                    "base_connection_charge"
                ] * (num_indust_cust + dso_scaling_factor * NP_Customer_Count)
                Non_participating_revenue_req = (
                    Indust_Sales
                    + NP_DA_Sales
                    + NP_RT_Sales
                    + NP_connection_fees
                    + NP_Energy * transactive_dist_rate
                )

        #  Calculate data frame of month customer bills
        #tic()
        # Legacy code used in DSO+T analysis
        cust_bill_df, billsum_df = calc_cust_bill(
            metadata,
            year_meter_df,
            year_trans_df,
            year_energysum_df,
            tariff,
            str(dso_num),
            dso_scaling_factor,
            num_indust_cust,
        )
        #toc()
    else:
        # Specify the file path of the bulk industrial loads
        case_config = load_json(case, "generate_case_config.json")
        industrial_file = os.path.join(tariff_path, case_config["indLoad"][5].split("/")[-1])

        # Check the value of the transactive cost balance method flag
        if trans_cost_balance_method not in [None, "volumetric", "fixed"]:
            raise ValueError(
                f"{trans_cost_balance_method} is not a supported cost balance method "
                + "for the transactive rate. Please try again."
            )

        # Calculate the prices the ensure enough revenue is collected to recover the  
        # DSO's expenses in the Rate Scenario analysis
        prices = calculate_tariff_prices(
            case,
            base_case,
            metadata,
            year_meter_df,
            year_trans_df,
            year_energysum_df,
            tariff,
            str(dso_num),
            dso_scaling_factor,
            num_indust_cust,
            industrial_file,
            rate_scenario,
            trans_cost_balance_method
        )

        # Update the price datasets accordingly
        if rate_scenario == "flat":
            # Update the variables
            tariff["DSO_" + str(dso_num)]["flat_rate"] = prices["flat_rate"]
        elif rate_scenario == "time-of-use":
            # Update the variables
            tariff["DSO_" + str(dso_num)]["flat_rate"] = prices["flat_rate"]
            tou_params = load_json(case, "time_of_use_parameters.json")
            for m in tou_params["DSO_" + str(dso_num)].keys():
                tou_params["DSO_" + str(dso_num)][m]["price"] = prices[
                    "tou_rate_" + tou_params["DSO_" + str(dso_num)][m]["season"]
                ]

            # Store the variables in the appropriate files, if not done later
            with open(os.path.join(case, "time_of_use_parameters.json"), "w") as fp:
                json.dump(tou_params, fp)
        elif rate_scenario == "subscription":
            # Update the variables
            tariff["DSO_" + str(dso_num)]["flat_rate"] = prices["flat_rate"]
            tou_params = load_json(case, "time_of_use_parameters.json")
            for m in tou_params["DSO_" + str(dso_num)].keys():
                tou_params["DSO_" + str(dso_num)][m]["price"] = prices[
                    "subscription_rate_" + tou_params["DSO_" + str(dso_num)][m]["season"]
                ]

            # Store the variables in the appropriate files, if not done later
            with open(os.path.join(case, "time_of_use_parameters.json"), "w") as fp:
                json.dump(tou_params, fp)
        elif rate_scenario == "transactive":
            # Update the variables
            tariff["DSO_" + str(dso_num)]["flat_rate"] = prices["flat_rate"]
            if trans_cost_balance_method in [None, "volumetric"]:
                tariff["DSO_" + str(dso_num)]["transactive_dist_rate"] = prices[
                    "transactive_volumetric_rate"
                ]
            elif trans_cost_balance_method == "fixed":
                tariff["DSO_" + str(dso_num)][
                    "transactive_connection_charge"
                ] = prices["transactive_fixed_charge"]
        elif rate_scenario == "dsot":
            # Update the variables
            tariff["DSO_" + str(dso_num)]["flat_rate"] = prices["flat_rate"]
            tariff["DSO_" + str(dso_num)]["transactive_dist_rate"] = prices[
                "dsot_volumetric_rate"
            ]
        
        # Calculate consumer bills in the Rate Scenario analysis
        cust_bill_df, billsum_df = calculate_consumer_bills(
            case,
            base_case,
            metadata,
            year_meter_df,
            year_trans_df,
            year_energysum_df,
            tariff,
            str(dso_num),
            dso_scaling_factor,
            num_indust_cust,
            rate_scenario
        )

    # Initialize surplus for export purposes when rate_scenario is not None
    surplus = 0 

    if rate_scenario is None:
        surplus = (
            billsum_df.loc[("total", "fix_total"), "sum"]
            + billsum_df.loc[("total", "trans_total"), "sum"]
        ) - dso_expenses
    
        if case_name in ['8-MR-BAU', '8-HR-BAU', '200-MR-BAU', '200-HR-BAU']:
            rebate = surplus / year_energysum_df.loc[('total', 'kw-hr'), 'sum']
        elif case_name in [
            '8-MR-Batt',
            '8-MR-Flex',
            '8-HR-Batt',
            '8-HR-Flex',
            '200-MR-Batt',
            '200-MR-Flex',
            '200-HR-Batt',
            '200-HR-Flex',
        ]:
            if counter_factual:
                rebate = surplus / (year_energysum_df.loc[('total', 'da_q'), 'sum'] + year_energysum_df.loc[
                    ('total', 'rt_q'), 'sum'])
            else:
                rebate = surplus / NP_Energy
        if iterate:
            if counter_factual:
                if case_name in ['8-MR-BAU', '8-HR-BAU', '200-MR-BAU', '200-HR-BAU', '200-MR-Batt', '200-MR-Flex',
                                 '200-HR-Batt', '200-HR-Flex']:
                    tariff['DSO_' + str(dso_num)]['flat_rate'] = tariff['DSO_' + str(dso_num)]['flat_rate'] - rebate
                elif case_name in ['8-MR-Batt', '8-MR-Flex', '8-HR-Batt', '8-HR-Flex']:
                    tariff['DSO_' + str(dso_num)]['transactive_dist_rate'] = tariff['DSO_' + str(dso_num)][
                                                                                 'transactive_dist_rate'] - rebate
            else:
                tariff['DSO_' + str(dso_num)]['flat_rate'] = tariff['DSO_' + str(dso_num)]['flat_rate'] - rebate

            cust_bill_df, billsum_df = calc_cust_bill(
                metadata,
                year_meter_df,
                year_trans_df,
                year_energysum_df,
                tariff,
                str(dso_num),
                dso_scaling_factor,
                num_indust_cust
            )

            surplus = (
                billsum_df.loc[('total', 'fix_total'), 'sum']
                + billsum_df.loc[('total', 'trans_total'), 'sum']
            ) - dso_expenses
            rebate = surplus / year_energysum_df.loc[('total', 'kw-hr'), 'sum']

    # Need to save files to hdf5 format.
    os.chdir(case)
    cust_bill_df.to_hdf('bill_dso_' + str(dso_num) + '_data.h5', key='cust_bill_data')
    billsum_df.to_hdf('bill_dso_' + str(dso_num) + '_data.h5', key='bill_sum_data')
    cust_bill_df.to_csv(path_or_buf=case + '/cust_bill_dso_' + str(dso_num) + '_data.csv')
    billsum_df.to_csv(path_or_buf=case + '/billsum_dso_' + str(dso_num) + '_data.csv')

    with open(os.path.join(tariff_path, file_name), "w") as out_file:
        json.dump(tariff, out_file, indent=2)

    if rate_scenario is None:
        # Calculate congestion averages and catch for zero values
        if year_energysum_df.loc[('residential', 'congest_q'), 'sum'] == 0:
            TransactiveCongestAvgPriceRes = 0
        else:
            TransactiveCongestAvgPriceRes = (year_energysum_df.loc[('residential', 'congest_$'), 'sum'] /
                                             year_energysum_df.loc[('residential', 'congest_q'), 'sum'])  # $/kW-hr
        if year_energysum_df.loc[('commercial', 'congest_q'), 'sum'] == 0:
            TransactiveCongestAvgPriceComm = 0
        else:
            TransactiveCongestAvgPriceComm = (
                        year_energysum_df.loc[('commercial', 'congest_$'), 'sum'] / year_energysum_df.loc[
                    ('commercial', 'congest_q'), 'sum'])  # $/kW-hr
        if year_energysum_df.loc[('industrial', 'congest_q'), 'sum'] == 0:
            TransactiveCongestAvgPriceInd = 0
        else:
            TransactiveCongestAvgPriceInd = (
                        year_energysum_df.loc[('industrial', 'congest_$'), 'sum'] / year_energysum_df.loc[
                    ('industrial', 'congest_q'), 'sum'])  # $/kW-hr

        DSO_Revenues_and_Energy_Sales = {
            'RetailSales': {
                'FixedSales': {
                    'ConnChargesFix': {
                        'ConnChargesFixRes': billsum_df.loc[('residential', 'fix_connect'), 'sum'] / 1000,  # $k
                        'ConnChargesFixComm': billsum_df.loc[('commercial', 'fix_connect'), 'sum'] / 1000,  # $k
                        'ConnChargesFixInd': billsum_df.loc[('industrial', 'fix_connect'), 'sum'] / 1000  # $k
                    },
                    'SalesFixRes': {
                        'EnergyFixPriceRes': year_energysum_df.loc[('residential', 'kw-hr'), 'sum'] / 1000,  # MW-hr/year
                        'EnergyFixRes': billsum_df.loc[('residential', 'fix_energy'), 'sum'] / 1000,  # $k
                        'DemandQuantityRes': year_energysum_df.loc[('residential', 'demand_quantity'), 'sum'] / 1000,  # MW
                        'DemandChargesRes': billsum_df.loc[('residential', 'demand'), 'sum'] / 1000,  # $k
                        'AvgPriceFixRes': billsum_df.loc[('residential', 'fix_blended_rate'), 'sum']  # $/kW-hr
                    },
                    'SalesFixComm': {
                        'EnergyFixPriceComm': year_energysum_df.loc[('commercial', 'kw-hr'), 'sum'] / 1000,  # MW-hr/year
                        'EnergyFixComm': billsum_df.loc[('commercial', 'fix_energy'), 'sum'] / 1000,  # $k
                        'DemandQuantityComm': year_energysum_df.loc[('commercial', 'demand_quantity'), 'sum'] / 1000,  # MW
                        'DemandChargesComm': billsum_df.loc[('commercial', 'demand'), 'sum'] / 1000,  # $k
                        'AvgPriceFixComm': billsum_df.loc[('commercial', 'fix_blended_rate'), 'sum']  # $/kW-hr
                    },
                    'SalesFixInd': {
                        'EnergyFixPriceInd': year_energysum_df.loc[('industrial', 'kw-hr'), 'sum'] / 1000,  # MW-hr/year
                        'EnergyFixInd': billsum_df.loc[('industrial', 'fix_energy'), 'sum'] / 1000,  # $k
                        'DemandQuantityInd': year_energysum_df.loc[('industrial', 'demand_quantity'), 'sum'] / 1000,  # MW
                        'DemandChargesInd': billsum_df.loc[('industrial', 'demand'), 'sum'] / 1000,  # $k
                        'AvgPriceFixInd': billsum_df.loc[('industrial', 'fix_blended_rate'), 'sum']  # $/kW-hr
                    }
                },
                'TransactiveSales': {
                    'ConnChargesDyn': {
                        'ConnChargesDynRes': billsum_df.loc[('residential', 'trans_connect'), 'sum'] / 1000,  # $k
                        'ConnChargesDynComm': billsum_df.loc[('commercial', 'trans_connect'), 'sum'] / 1000,  # $k
                        'ConnChargesDynInd': billsum_df.loc[('industrial', 'trans_connect'), 'sum'] / 1000  # $k
                    },
                    'DistCharges': {
                        'DistChargesRes': billsum_df.loc[('residential', 'distribution'), 'sum'] / 1000,  # $k
                        'DistChargesComm': billsum_df.loc[('commercial', 'distribution'), 'sum'] / 1000,  # $k
                        'DistChargesInd': billsum_df.loc[('industrial', 'distribution'), 'sum'] / 1000  # $k
                    },
                    'RetailDASales': {
                        'RetailDASalesRes': billsum_df.loc[('residential', 'DA_energy'), 'sum'] / 1000,  # $k
                        'RetailDASalesComm': billsum_df.loc[('commercial', 'DA_energy'), 'sum'] / 1000,  # $k
                        'RetailDASalesInd': billsum_df.loc[('industrial', 'DA_energy'), 'sum'] / 1000  # $k
                    },
                    'RetailDAEnergy': {
                        'RetailDAEnergyRes': year_energysum_df.loc[('residential', 'da_q'), 'sum'] / 1000,  # MW-hrs
                        'RetailDAEnergyComm': year_energysum_df.loc[('commercial', 'da_q'), 'sum'] / 1000,  # MW-hrs
                        'RetailDAEnergyInd': year_energysum_df.loc[('industrial', 'da_q'), 'sum'] / 1000  # MW-hrs
                    },
                    'RetailDAAvgPrice': {
                        'RetailDAAvgPriceRes': billsum_df.loc[('residential', 'da_blended_rate'), 'sum'],  # $/kW-hr
                        'RetailDAAvgPriceComm': billsum_df.loc[('commercial', 'da_blended_rate'), 'sum'],  # $/kW-hr
                        'RetailDAAvgPriceInd': billsum_df.loc[('industrial', 'da_blended_rate'), 'sum']  # $/kW-hr
                    },
                    'RetailRTSales': {
                        'RetailRTSalesRes': billsum_df.loc[('residential', 'RT_energy'), 'sum'] / 1000,  # $k
                        'RetailRTSalesComm': billsum_df.loc[('commercial', 'RT_energy'), 'sum'] / 1000,  # $k
                        'RetailRTSalesInd': billsum_df.loc[('industrial', 'RT_energy'), 'sum'] / 1000  # $k
                    },
                    'RetailRTEnergy': {
                        'RetailRTEnergyRes': year_energysum_df.loc[('residential', 'rt_q'), 'sum'] / 1000,  # MW-hrs
                        'RetailRTEnergyComm': year_energysum_df.loc[('commercial', 'rt_q'), 'sum'] / 1000,  # MW-hrs
                        'RetailRTEnergyInd': year_energysum_df.loc[('industrial', 'rt_q'), 'sum'] / 1000  # MW-hrs
                    },
                    'RetailRTAvgPrice': {
                        'RetailRTAvgPriceRes': billsum_df.loc[('residential', 'rt_blended_rate'), 'sum'],  # $/kW-hr
                        'RetailRTAvgPriceComm': billsum_df.loc[('commercial', 'rt_blended_rate'), 'sum'],  # $/kW-hr
                        'RetailRTAvgPriceInd': billsum_df.loc[('industrial', 'rt_blended_rate'), 'sum']  # $/kW-hr
                    },
                    'TransactiveAvgPrice': {
                        'TransactiveAvgPriceRes': billsum_df.loc[('residential', 'trans_blended_rate'), 'sum'],  # $/kW-hr
                        'TransactiveAvgPriceComm': billsum_df.loc[('commercial', 'trans_blended_rate'), 'sum'],  # $/kW-hr
                        'TransactiveAvgPriceInd': billsum_df.loc[('industrial', 'trans_blended_rate'), 'sum']  # $/kW-hr
                    },
                    'TransactiveCongestionEnergy': {
                        'TransactiveCongestEnergyRes': year_energysum_df.loc[('residential', 'congest_q'), 'sum'] / 1000,   # MW-hrs
                        'TransactiveCongestEnergyComm': year_energysum_df.loc[('commercial', 'congest_q'), 'sum'] / 1000,   # MW-hrs
                        'TransactiveCongestEnergyInd': year_energysum_df.loc[('industrial', 'congest_q'), 'sum'] / 1000   # MW-hrs
                    },
                    'TransactiveCongestionSales': {
                        'TransactiveCongestSalesRes': year_energysum_df.loc[('residential', 'congest_$'), 'sum'] / 1000,  # $k
                        'TransactiveCongestSalesComm': year_energysum_df.loc[('commercial', 'congest_$'), 'sum'] / 1000,  # $k
                        'TransactiveCongestSalesInd': year_energysum_df.loc[('industrial', 'congest_$'), 'sum'] / 1000  # $k
                    },
                    'TransactiveCongestionAvgPrice': {
                        'TransactiveCongestAvgPriceRes': TransactiveCongestAvgPriceRes,  # $/kW-hr
                        'TransactiveCongestAvgPriceComm': TransactiveCongestAvgPriceComm,  # $/kW-hr
                        'TransactiveCongestAvgPriceInd': TransactiveCongestAvgPriceInd  # $/kW-hr
                    }
                }
            },
            'EnergySold': year_energysum_df.loc[('total', 'kw-hr'), 'sum'] / 1000,  # Energy Sold in MW-hr
            'RequiredRevenue': (billsum_df.loc[('total', 'fix_total'), 'sum'] + billsum_df.loc[
                ('total', 'trans_total'), 'sum']) / 1000,  # Energy Charges in $k
            'EffectiveCostRetailEnergy': (billsum_df.loc[('total', 'fix_total'), 'sum'] +
                                          billsum_df.loc[('total', 'trans_total'), 'sum']) \
                                         / year_energysum_df.loc[('total', 'kw-hr'), 'sum'],  # $/kW-hr
            'DistLosses': {
                'DistLossesCost': year_energysum_df.loc[('total', 'dist_loss_$'), 'sum'] / 1000,  # DSO Losses in $k
                'DistLossesEnergy': year_energysum_df.loc[('total', 'dist_loss_q'), 'sum'] / 1000,  # DSO Losses in MW-hrs
            }
        }

        DSO_Cash_Flows = {
            'Revenues': {
                'RetailSales': {
                    'FixedSales': {
                        'FixedEnergyCharges': billsum_df.loc[('total', 'fix_energy'), 'sum'] / 1000,  # Energy Charges in $k
                        'DemandCharges': billsum_df.loc[('total', 'demand'), 'sum'] / 1000,  # Demand Charges in $k
                        'ConnectChargesFix': billsum_df.loc[('total', 'fix_connect'), 'sum'] / 1000
                        # Connection Charges in $k
                    },
                    'TransactiveSales': {
                        'RetailDACharges': billsum_df.loc[('total', 'DA_energy'), 'sum'] / 1000,  # DA Energy Charges in $k
                        'RetailRTCharges': billsum_df.loc[('total', 'RT_energy'), 'sum'] / 1000,  # RT Energy Charges in $k
                        'DistCharges': billsum_df.loc[('total', 'distribution'), 'sum'] / 1000,  # Distribution Charges in $k
                        'ConnectChargesDyn': billsum_df.loc[('total', 'trans_connect'), 'sum'] / 1000  # Connection Charges in $k
                    }
                },
            },
        }
    else:
        # Initialize the DSO_Revenues_and_Energy_Sales and DSO_Cash_Flows dicts
        DSO_Revenues_and_Energy_Sales = {
            "RetailSales": {
                "FlatSales": {
                    "FlatSalesRes": {
                        "FlatEnergySalesRes": billsum_df.loc[("residential", "flat_energy_purchased"), "sum"] / 1000, # MW-hr/year
                        "FlatEnergyChargesRes": billsum_df.loc[("residential", "flat_energy_charge"), "sum"] / 1000, # $k
                        "FlatDemandChargesRes": billsum_df.loc[("residential", "flat_demand_charge"), "sum"] / 1000, # $k
                        "FlatFixedChargesRes": billsum_df.loc[("residential", "flat_fixed_charge"), "sum"] / 1000, # $k
                        "FlatAveragePriceRes": billsum_df.loc[("residential", "flat_average_price"), "sum"], # $/kW-hr
                    },
                    "FlatSalesComm": {
                        "FlatEnergySalesComm": billsum_df.loc[("commercial", "flat_energy_purchased"), "sum"] / 1000, # MW-hr/year
                        "FlatEnergyChargesComm": billsum_df.loc[("commercial", "flat_energy_charge"), "sum"] / 1000, # $k
                        "FlatDemandChargesComm": billsum_df.loc[("commercial", "flat_demand_charge"), "sum"] / 1000, # $k
                        "FlatFixedChargesComm": billsum_df.loc[("commercial", "flat_fixed_charge"), "sum"] / 1000, # $k
                        "FlatAveragePriceComm": billsum_df.loc[("commercial", "flat_average_price"), "sum"], # $/kW-hr
                    },
                    "FlatSalesInd": {
                        "FlatEnergySalesInd": billsum_df.loc[("industrial", "flat_energy_purchased"), "sum"] / 1000, # MW-hr/year
                        "FlatEnergyChargesInd": billsum_df.loc[("industrial", "flat_energy_charge"), "sum"] / 1000, # $k
                        "FlatDemandChargesInd": billsum_df.loc[("industrial", "flat_demand_charge"), "sum"] / 1000, # $k
                        "FlatFixedChargesInd": billsum_df.loc[("industrial", "flat_fixed_charge"), "sum"] / 1000, # $k
                        "FlatAveragePriceInd": billsum_df.loc[("industrial", "flat_average_price"), "sum"], # $/kW-hr
                    },
                },
            },
            "EnergySold": billsum_df.loc[("total", "flat_energy_purchased"), "sum"] / 1000,  # Energy Sold in MW-hr
            "EnergySoldMonthly": {
                m: billsum_df.loc[("total", "flat_energy_purchased"), m] / 1000
                for m in billsum_df
                if m != "sum"
            }, # Energy Sold in MW-hr
            "RequiredRevenue": billsum_df.loc[("total", "flat_total_charge"), "sum"] / 1000, # Energy charges in $k
            "EffectiveCostRetailEnergy": billsum_df.loc[
                ("total", "flat_total_charge"), "sum"
            ]
            / billsum_df.loc[("total", "flat_energy_purchased"), "sum"],  # $/kW-hr
            "DistLosses": {
                "DistLossesCost": year_energysum_df.loc[("total", "dist_loss_$"), "sum"] / 1000,  # DSO Losses in $k
                "DistLossesEnergy": year_energysum_df.loc[("total", "dist_loss_q"), "sum"] / 1000,  # DSO Losses in MW-hrs
            },
        }
        DSO_Cash_Flows = {
            "Revenues": {
                "RetailSales": {
                    "FlatSales": {
                        "FlatEnergyCharges": billsum_df.loc[("total", "flat_energy_charge"), "sum"] / 1000, # $k
                        "FlatDemandCharges": billsum_df.loc[("total", "flat_demand_charge"), "sum"] / 1000, # $k
                        "FlatFixedCharges": billsum_df.loc[("total", "flat_fixed_charge"), "sum"] / 1000, # $k
                    },
                    "TOUSales": {
                        "TOUEnergyCharges": 0,  # $k
                        "TOUDemandCharges": 0,  # $k
                        "TOUFixedCharges": 0
                    },
                    "SubscriptionSales": {
                        "SubscriptionEnergyCharges": 0,  # $k
                        "SubscriptionDemandCharges": 0,  # $k
                        "SubscriptionFixedCharges": 0,
                        "SubscriptionNetDeviationCharges": 0
                    },
                    "TransactiveSales": {
                        "TransactiveDAEnergyCharges": 0,  # $k
                        "TransactiveRTEnergyCharges": 0,  # $k
                        "TransactiveFixedCharges": 0,
                        "TransactiveVolumetricCharges": 0
                    },
                    "DSOTSales": {
                        "DSOTDAEnergyCharges": 0,  # $k
                        "DSOTRTEnergyCharges": 0,  # $k
                        "DSOTFixedCharges": 0,
                        "DSOTVolumetricCharges": 0
                    },
                },
            },
        }

        # Assign additional information based on the rate scenario
        if rate_scenario == "time-of-use":
            DSO_Revenues_and_Energy_Sales["RetailSales"]["TOUSales"] = {
                "TOUSalesRes": {
                    "TOUEnergySalesRes": billsum_df.loc[("residential", "tou_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "TOUEnergyChargesRes": billsum_df.loc[("residential", "tou_energy_charge"), "sum"] / 1000, # $k
                    "TOUDemandChargesRes": billsum_df.loc[("residential", "tou_demand_charge"), "sum"] / 1000, # $k
                    "TOUFixedChargesRes": billsum_df.loc[("residential", "tou_fixed_charge"), "sum"] / 1000, # $k
                    "TOUAveragePriceRes": billsum_df.loc[("residential", "tou_average_price"), "sum"], # $/kW-hr
                },
                "TOUSalesComm": {
                    "TOUEnergySalesComm": billsum_df.loc[("commercial", "tou_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "TOUEnergyChargesComm": billsum_df.loc[("commercial", "tou_energy_charge"), "sum"] / 1000, # $k
                    "TOUDemandChargesComm": billsum_df.loc[("commercial", "tou_demand_charge"), "sum"] / 1000, # $k
                    "TOUFixedChargesComm": billsum_df.loc[("commercial", "tou_fixed_charge"), "sum"] / 1000, # $k
                    "TOUAveragePriceComm": billsum_df.loc[("commercial", "tou_average_price"), "sum"], # $/kW-hr
                },
                "TOUSalesInd": {
                    "TOUEnergySalesInd": billsum_df.loc[("industrial", "tou_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "TOUEnergyChargesInd": billsum_df.loc[("industrial", "tou_energy_charge"), "sum"] / 1000, # $k
                    "TOUDemandChargesInd": billsum_df.loc[("industrial", "tou_demand_charge"), "sum"] / 1000, # $k
                    "TOUFixedChargesInd": billsum_df.loc[("industrial", "tou_fixed_charge"), "sum"] / 1000, # $k
                    "TOUAveragePriceInd": billsum_df.loc[("industrial", "tou_average_price"), "sum"], # $/kW-hr
                },
            }
            DSO_Revenues_and_Energy_Sales["EnergySold"] += billsum_df.loc[("total", "tou_energy_purchased"), "sum"] / 1000 # Energy Sold in MW-hr
            for m in billsum_df:
                if m != "sum":
                    DSO_Revenues_and_Energy_Sales["EnergySoldMonthly"][m] += billsum_df.loc[("total", "tou_energy_purchased"), m] / 1000
            DSO_Revenues_and_Energy_Sales["RequiredRevenue"] += billsum_df.loc[("total", "tou_total_charge"), "sum"] / 1000 # Energy charges in $k
            DSO_Revenues_and_Energy_Sales["EffectiveCostRetailEnergy"] = (
                billsum_df.loc[("total", "flat_total_charge"), "sum"]
                + billsum_df.loc[("total", "tou_total_charge"), "sum"]
            ) / (
                billsum_df.loc[("total", "flat_energy_purchased"), "sum"]
                + billsum_df.loc[("total", "tou_energy_purchased"), "sum"]
            )
            DSO_Cash_Flows["Revenues"]["RetailSales"]["TOUSales"] = {
                "TOUEnergyCharges": billsum_df.loc[("total", "tou_energy_charge"), "sum"] / 1000, # $k
                "TOUDemandCharges": billsum_df.loc[("total", "tou_demand_charge"), "sum"] / 1000, # $k
                "TOUFixedCharges": billsum_df.loc[("total", "tou_fixed_charge"), "sum"] / 1000, # $k
            }
        elif rate_scenario == "subscription":
            DSO_Revenues_and_Energy_Sales["RetailSales"]["SubscriptionSales"] = {
                "SubscriptionSalesRes": {
                    "SubscriptionEnergySalesRes": billsum_df.loc[("residential", "subscription_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "SubscriptionEnergyChargesRes": billsum_df.loc[("residential", "subscription_energy_charge"), "sum"] / 1000, # $k
                    "SubscriptionDemandChargesRes": billsum_df.loc[("residential", "subscription_demand_charge"), "sum"] / 1000, # $k
                    "SubscriptionFixedChargesRes": billsum_df.loc[("residential", "subscription_fixed_charge"), "sum"] / 1000, # $k
                    "SubscriptionNetDeviationChargesRes": billsum_df.loc[("residential", "subscription_net_deviation_charge"), "sum"] / 1000, # $k
                    "SubscriptionAveragePriceRes": billsum_df.loc[("residential", "subscription_average_price"), "sum"], # $/kW-hr
                },
                "SubscriptionSalesComm": {
                    "SubscriptionEnergySalesComm": billsum_df.loc[("commercial", "subscription_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "SubscriptionEnergyChargesComm": billsum_df.loc[("commercial", "subscription_energy_charge"), "sum"] / 1000, # $k
                    "SubscriptionDemandChargesComm": billsum_df.loc[("commercial", "subscription_demand_charge"), "sum"] / 1000, # $k
                    "SubscriptionFixedChargesComm": billsum_df.loc[("commercial", "subscription_fixed_charge"), "sum"] / 1000, # $k
                    "SubscriptionNetDeviationChargesComm": billsum_df.loc[("commercial", "subscription_net_deviation_charge"), "sum"] / 1000, # $k
                    "SubscriptionAveragePriceComm": billsum_df.loc[("commercial", "subscription_average_price"), "sum"], # $/kW-hr
                },
                "SubscriptionSalesInd": {
                    "SubscriptionEnergySalesInd": billsum_df.loc[("industrial", "subscription_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "SubscriptionEnergyChargesInd": billsum_df.loc[("industrial", "subscription_energy_charge"), "sum"] / 1000, # $k
                    "SubscriptionDemandChargesInd": billsum_df.loc[("industrial", "subscription_demand_charge"), "sum"] / 1000, # $k
                    "SubscriptionFixedChargesInd": billsum_df.loc[("industrial", "subscription_fixed_charge"), "sum"] / 1000, # $k
                    "SubscriptionNetDeviationChargesInd": billsum_df.loc[("industrial", "subscription_net_deviation_charge"), "sum"] / 1000, # $k
                    "SubscriptionAveragePriceInd": billsum_df.loc[("industrial", "subscription_average_price"), "sum"], # $/kW-hr
                },
            }
            DSO_Revenues_and_Energy_Sales["EnergySold"] += billsum_df.loc[("total", "subscription_energy_purchased"), "sum"] / 1000 # Energy Sold in MW-hr
            for m in billsum_df:
                if m != "sum":
                    DSO_Revenues_and_Energy_Sales["EnergySoldMonthly"][m] += billsum_df.loc[("total", "subscription_energy_purchased"), m] / 1000
            DSO_Revenues_and_Energy_Sales["RequiredRevenue"] += billsum_df.loc[("total", "subscription_total_charge"), "sum"] / 1000 # Energy charges in $k
            DSO_Revenues_and_Energy_Sales["EffectiveCostRetailEnergy"] = (
                billsum_df.loc[("total", "flat_total_charge"), "sum"]
                + billsum_df.loc[("total", "subscription_total_charge"), "sum"]
            ) / (
                billsum_df.loc[("total", "flat_energy_purchased"), "sum"]
                + billsum_df.loc[("total", "subscription_energy_purchased"), "sum"]
            )
            DSO_Cash_Flows["Revenues"]["RetailSales"]["SubscriptionSales"] = {
                "SubscriptionEnergyCharges": billsum_df.loc[("total", "subscription_energy_charge"), "sum"] / 1000, # $k
                "SubscriptionDemandCharges": billsum_df.loc[("total", "subscription_demand_charge"), "sum"] / 1000, # $k
                "SubscriptionFixedCharges": billsum_df.loc[("total", "subscription_fixed_charge"), "sum"] / 1000, # $k
                "SubscriptionNetDeviationCharges": billsum_df.loc[("total", "subscription_net_deviation_charge"), "sum"] / 1000, # $k
            }
        elif rate_scenario == "transactive":
            DSO_Revenues_and_Energy_Sales["RetailSales"]["TransactiveSales"] = {
                "TransactiveSalesRes": {
                    "TransactiveEnergySalesRes": billsum_df.loc[("residential", "transactive_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "TransactiveDAEnergyChargesRes": billsum_df.loc[("residential", "transactive_DA_energy_charge"), "sum"] / 1000, # $k
                    "TransactiveRTEnergyChargesRes": billsum_df.loc[("residential", "transactive_RT_energy_charge"), "sum"] / 1000, # $k
                    "TransactiveFixedChargesRes": billsum_df.loc[("residential", "transactive_fixed_charge"), "sum"] / 1000, # $k
                    "TransactiveVolumetricChargeRes": billsum_df.loc[("residential", "transactive_volumetric_charge"), "sum"] / 1000, # $k
                    "TransactiveAveragePriceRes": billsum_df.loc[("residential", "transactive_average_price"), "sum"], # $/kW-hr
                },
                "TransactiveSalesComm": {
                    "TransactiveEnergySalesComm": billsum_df.loc[("commercial", "transactive_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "TransactiveDAEnergyChargesComm": billsum_df.loc[("commercial", "transactive_DA_energy_charge"), "sum"] / 1000, # $k
                    "TransactiveRTEnergyChargesComm": billsum_df.loc[("commercial", "transactive_RT_energy_charge"), "sum"] / 1000, # $k
                    "TransactiveFixedChargesComm": billsum_df.loc[("commercial", "transactive_fixed_charge"), "sum"] / 1000, # $k
                    "TransactiveVolumetricChargeComm": billsum_df.loc[("commercial", "transactive_volumetric_charge"), "sum"] / 1000, # $k
                    "TransactiveAveragePriceComm": billsum_df.loc[("commercial", "transactive_average_price"), "sum"], # $/kW-hr
                },
                "TransactiveSalesInd": {
                    "TransactiveEnergySalesInd": billsum_df.loc[("industrial", "transactive_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "TransactiveDAEnergyChargesInd": billsum_df.loc[("industrial", "transactive_DA_energy_charge"), "sum"] / 1000, # $k
                    "TransactiveRTEnergyChargesInd": billsum_df.loc[("industrial", "transactive_RT_energy_charge"), "sum"] / 1000, # $k
                    "TransactiveFixedChargesInd": billsum_df.loc[("industrial", "transactive_fixed_charge"), "sum"] / 1000, # $k
                    "TransactiveVolumetricChargeInd": billsum_df.loc[("industrial", "transactive_volumetric_charge"), "sum"] / 1000, # $k
                    "TransactiveAveragePriceInd": billsum_df.loc[("industrial", "transactive_average_price"), "sum"], # $/kW-hr
                },
            }
            DSO_Revenues_and_Energy_Sales["EnergySold"] += billsum_df.loc[("total", "transactive_energy_purchased"), "sum"] / 1000 # Energy Sold in MW-hr
            for m in billsum_df:
                if m != "sum":
                    DSO_Revenues_and_Energy_Sales["EnergySoldMonthly"][m] += billsum_df.loc[("total", "transactive_energy_purchased"), m] / 1000
            DSO_Revenues_and_Energy_Sales["RequiredRevenue"] += billsum_df.loc[("total", "transactive_total_charge"), "sum"] / 1000 # Energy charges in $k
            DSO_Revenues_and_Energy_Sales["EffectiveCostRetailEnergy"] = (
                billsum_df.loc[("total", "flat_total_charge"), "sum"]
                + billsum_df.loc[("total", "transactive_total_charge"), "sum"]
            ) / (
                billsum_df.loc[("total", "flat_energy_purchased"), "sum"]
                + billsum_df.loc[("total", "transactive_energy_purchased"), "sum"]
            )
            DSO_Cash_Flows["Revenues"]["RetailSales"]["TransactiveSales"] = {
                "TransactiveDAEnergyCharges": billsum_df.loc[("total", "transactive_DA_energy_charge"), "sum"] / 1000, # $k
                "TransactiveRTEnergyCharges": billsum_df.loc[("total", "transactive_RT_energy_charge"), "sum"] / 1000, # $k
                "TransactiveFixedCharges": billsum_df.loc[("total", "transactive_fixed_charge"), "sum"] / 1000, # $k
                "TransactiveVolumetricCharges": billsum_df.loc[("total", "transactive_volumetric_charge"), "sum"] / 1000, # $k
            }
        elif rate_scenario == "dsot":
            DSO_Revenues_and_Energy_Sales["RetailSales"]["DSOTSales"] = {
                "DSOTSalesRes": {
                    "DSOTEnergySalesRes": billsum_df.loc[("residential", "dsot_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "DSOTDAEnergyChargesRes": billsum_df.loc[("residential", "dsot_DA_energy_charge"), "sum"] / 1000, # $k
                    "DSOTRTEnergyChargesRes": billsum_df.loc[("residential", "dsot_RT_energy_charge"), "sum"] / 1000, # $k
                    "DSOTFixedChargesRes": billsum_df.loc[("residential", "dsot_fixed_charge"), "sum"] / 1000, # $k
                    "DSOTVolumetricChargeRes": billsum_df.loc[("residential", "dsot_volumetric_charge"), "sum"] / 1000, # $k
                    "DSOTAveragePriceRes": billsum_df.loc[("residential", "dsot_average_price"), "sum"], # $/kW-hr
                },
                "DSOTSalesComm": {
                    "DSOTEnergySalesComm": billsum_df.loc[("commercial", "dsot_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "DSOTDAEnergyChargesComm": billsum_df.loc[("commercial", "dsot_DA_energy_charge"), "sum"] / 1000, # $k
                    "DSOTRTEnergyChargesComm": billsum_df.loc[("commercial", "dsot_RT_energy_charge"), "sum"] / 1000, # $k
                    "DSOTFixedChargesComm": billsum_df.loc[("commercial", "dsot_fixed_charge"), "sum"] / 1000, # $k
                    "DSOTVolumetricChargeComm": billsum_df.loc[("commercial", "dsot_volumetric_charge"), "sum"] / 1000, # $k
                    "DSOTAveragePriceComm": billsum_df.loc[("commercial", "dsot_average_price"), "sum"], # $/kW-hr
                },
                "DSOTSalesInd": {
                    "DSOTEnergySalesInd": billsum_df.loc[("industrial", "dsot_energy_purchased"), "sum"] / 1000, # MW-hr/year
                    "DSOTDAEnergyChargesInd": billsum_df.loc[("industrial", "dsot_DA_energy_charge"), "sum"] / 1000, # $k
                    "DSOTRTEnergyChargesInd": billsum_df.loc[("industrial", "dsot_RT_energy_charge"), "sum"] / 1000, # $k
                    "DSOTFixedChargesInd": billsum_df.loc[("industrial", "dsot_fixed_charge"), "sum"] / 1000, # $k
                    "DSOTVolumetricChargeInd": billsum_df.loc[("industrial", "dsot_volumetric_charge"), "sum"] / 1000, # $k
                    "DSOTAveragePriceInd": billsum_df.loc[("industrial", "dsot_average_price"), "sum"], # $/kW-hr
                },
            }
            DSO_Revenues_and_Energy_Sales["EnergySold"] += billsum_df.loc[("total", "dsot_energy_purchased"), "sum"] / 1000 # Energy Sold in MW-hr
            for m in billsum_df:
                if m != "sum":
                    DSO_Revenues_and_Energy_Sales["EnergySoldMonthly"][m] += billsum_df.loc[("total", "dsot_energy_purchased"), m] / 1000
            DSO_Revenues_and_Energy_Sales["RequiredRevenue"] += billsum_df.loc[("total", "dsot_total_charge"), "sum"] / 1000 # Energy charges in $k
            DSO_Revenues_and_Energy_Sales["EffectiveCostRetailEnergy"] = (
                billsum_df.loc[("total", "flat_total_charge"), "sum"]
                + billsum_df.loc[("total", "dsot_total_charge"), "sum"]
            ) / (
                billsum_df.loc[("total", "flat_energy_purchased"), "sum"]
                + billsum_df.loc[("total", "dsot_energy_purchased"), "sum"]
            )
            DSO_Cash_Flows["Revenues"]["RetailSales"]["DSOTSales"] = {
                "DSOTDAEnergyCharges": billsum_df.loc[("total", "dsot_DA_energy_charge"), "sum"] / 1000, # $k
                "DSOTRTEnergyCharges": billsum_df.loc[("total", "dsot_RT_energy_charge"), "sum"] / 1000, # $k
                "DSOTFixedCharges": billsum_df.loc[("total", "dsot_fixed_charge"), "sum"] / 1000, # $k
                "DSOTVolumetricCharges": billsum_df.loc[("total", "dsot_volumetric_charge"), "sum"] / 1000, # $k
            }

    return DSO_Cash_Flows, DSO_Revenues_and_Energy_Sales, tariff, surplus

def get_cust_bill(cust, bill_df, bill_metadata, energy_df, rate_scenario):
    """ Populates dictionary of individual customer's annual bill.
    Args:
        cust (str): customer name (meter name from GLD dictionary)
        bill_df (dataframe): dataframe of annual and monthly customer bills
        bill_metadata (dict): dictionary of GLD metadata including tarrif and building type for each meter
        energy_df
        rate_scenario (str): A str specifying the rate scenario under investigation: flat,
        time-of-use, subscription, or transactive. If None, this function defaults to DSO+T.
    Returns:
        customer_annual_bill (dict): dictionary of customers annual energy bill
        """

    # TODO: Generalize this format - e.g. average rate - inclusion of transactive and subscription etc...

    customer_annual_bill = {
        'BillsFix': {
            'PurchasesFix': {
                'EnergyFix': bill_df.loc[(cust, 'flat_energy_charge'), 'sum'],
                'DemandCharges': bill_df.loc[(cust, 'flat_demand_charge'), 'sum']
            },
            'ConnChargesFix': bill_df.loc[(cust, 'flat_fixed_charge'), 'sum'],
            'TotalFix': bill_df.loc[(cust, 'flat_total_charge'), 'sum']
        },
        'EnergyQuantity': bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'],
        'MaxLoad': energy_df.loc[(cust, 'max_kw'), 'sum'],
        'LoadFactor': energy_df.loc[(cust, 'load_factor'), 'sum'],
        'BlendedRate': bill_df.loc[(cust, 'flat_average_price'), 'sum'],
        'RateDesign': rate_scenario,
        'CustomerType': {
            'BuildingType': bill_metadata['billingmeters'][cust]['building_type'],
            'TariffClass': bill_metadata['billingmeters'][cust]['tariff_class'],

        }
    }

    if rate_scenario == "time-of-use":
        customer_annual_bill.update({
            'BillsTOU': {
                'PurchasesTOU': {
                    'EnergyTotal': bill_df.loc[(cust, 'tou_energy_charge'), 'sum'],
                    'EnergyPeak': bill_df.loc[(cust, 'tou_peak_energy_charge'), 'sum'],
                    'EnergyOffPeak': bill_df.loc[(cust, 'tou_off-peak_energy_charge'), 'sum']
                },
                'DemandChargesTOU': bill_df.loc[(cust, 'tou_demand_charge'), 'sum'],
                'ConnChargesTOU': bill_df.loc[(cust, 'tou_fixed_charge'), 'sum'],
                'TotalTOU': bill_df.loc[(cust, 'tou_total_charge'), 'sum'],
            },
            'BlendedRate': (bill_df.loc[(cust, 'flat_average_price'), 'sum'] *
                           bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] +
                           bill_df.loc[(cust, 'tou_average_price'), 'sum'] *
                            bill_df.loc[(cust, 'tou_energy_purchased'), 'sum'])
                            / (bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] +
                              bill_df.loc[(cust, 'tou_energy_purchased'), 'sum']),
            'EnergyQuantity': bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] +
                              bill_df.loc[(cust, 'tou_energy_purchased'), 'sum']
        })

    elif rate_scenario == "subscription":
        customer_annual_bill.update({
            'BillsSubscription': {
                'PurchasesSub': {
                    'EnergySub': bill_df.loc[(cust, 'subscription_energy_charge'), 'sum'],
                    'EnergyDeviationSub': bill_df.loc[(cust, 'subscription_net_deviation_charge'), 'sum']
                },
                'DemandChargesSub': bill_df.loc[(cust, 'subscription_demand_charge'), 'sum'],
                'ConnChargesSub': bill_df.loc[(cust, 'subscription_fixed_charge'), 'sum'],
                'TotalSub': bill_df.loc[(cust, 'subscription_total_charge'), 'sum'],
            },
            'BlendedRate': (bill_df.loc[(cust, 'flat_average_price'), 'sum'] *
                           bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] +
                           bill_df.loc[(cust, 'subscription_average_price'), 'sum'] *
                            bill_df.loc[(cust, 'subscription_energy_purchased'), 'sum'])
                            / (bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] +
                              bill_df.loc[(cust, 'subscription_energy_purchased'), 'sum']),
            'EnergyQuantity': bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] + bill_df.loc[
                (cust, 'subscription_energy_purchased'), 'sum']
        })

    elif rate_scenario == "transactive":
        customer_annual_bill.update({
            'BillsTransactive': {
                'PurchasesDyn': {
                    'DAEnergy': bill_df.loc[(cust, 'transactive_DA_energy_charge'), 'sum'],
                    'RTEnergy': bill_df.loc[(cust, 'transactive_RT_energy_charge'), 'sum']
                },
                'DistCharges': bill_df.loc[(cust, 'transactive_volumetric_charge'), 'sum'],
                'ConnChargesDyn': bill_df.loc[(cust, 'transactive_fixed_charge'), 'sum'],
                'TotalDyn': bill_df.loc[(cust, 'transactive_total_charge'), 'sum'],
            },
            'BlendedRate': (bill_df.loc[(cust, 'flat_average_price'), 'sum'] *
                           bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] +
                           bill_df.loc[(cust, 'transactive_average_price'), 'sum'] *
                            bill_df.loc[(cust, 'transactive_energy_purchased'), 'sum'])
                            / (bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] +
                              bill_df.loc[(cust, 'transactive_energy_purchased'), 'sum']),
            'EnergyQuantity': bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] + bill_df.loc[
                (cust, 'transactive_energy_purchased'), 'sum']
        })

    elif rate_scenario == "dsot":
        customer_annual_bill.update({
            'BillsTransactive': {
                'PurchasesDyn': {
                    'DAEnergy': bill_df.loc[(cust, 'dsot_DA_energy_charge'), 'sum'],
                    'RTEnergy': bill_df.loc[(cust, 'dsot_RT_energy_charge'), 'sum']
                },
                'DistCharges': bill_df.loc[(cust, 'dsot_volumetric_charge'), 'sum'],
                'ConnChargesDyn': bill_df.loc[(cust, 'dsot_fixed_charge'), 'sum'],
                'TotalDyn': bill_df.loc[(cust, 'dsot_total_charge'), 'sum'],
            },
            'BlendedRate': (bill_df.loc[(cust, 'flat_average_price'), 'sum'] *
                           bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] +
                           bill_df.loc[(cust, 'dsot_average_price'), 'sum'] *
                            bill_df.loc[(cust, 'dsot_energy_purchased'), 'sum'])
                            / (bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] +
                              bill_df.loc[(cust, 'dsot_energy_purchased'), 'sum']),
            'EnergyQuantity': bill_df.loc[(cust, 'flat_energy_purchased'), 'sum'] + bill_df.loc[
                (cust, 'dsot_energy_purchased'), 'sum']
        })

    return customer_annual_bill

    # ----------------------   MAIN  ------------------------

def _testing():
    '''
    Example of creating energy statistics and bills for each customer (GLD meter) and by customer class.
    '''
    # ------------ Selection of DSO Range  ---------------------------------

    dso_range = range(4, 5)
    # ------------ Select folder locations for different cases ---------

    sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

    data_path = 'C:/Users/reev057\PycharmProjects/DSO+T/Data/Simdata/DER2/V1.1-1336-gb74f2d99/lean_8'
    base_case = 'C:/Users/reev057\PycharmProjects/DSO+T/Data/Simdata/DER2/V1.1-1336-gb74f2d99/lean_8'
    agent_prefix = '/DSO_'
    GLD_prefix = '/Substation_'
    tariff_path = 'C:/Users/reev057/PycharmProjects/TESP/src/examples/analysis/dsot/data'
    metadata_path = 'C:/Users/reev057/PycharmProjects/TESP/src/examples/analysis/dsot/data'

    # ------  For each DSO determine the scaling factor and update the metadata
    for dso_num in dso_range:
        # load DSO metadata
        file_name = 'Substation_' + str(dso_num) + '_glm_dict.json'
        agent_prefix = '/DSO_'
        GLD_prefix = '/Substation_'
        metadata = load_json(base_case + agent_prefix + str(dso_num), file_name)

        DSOmetadata = load_json(metadata_path, '8-metadata-lean.json')
        # TODO: This should be done in meta data and read in.
        dso_scaling_factor = DSOmetadata['DSO_' + str(dso_num)]['number_of_customers'] \
                             * DSOmetadata['DSO_' + str(dso_num)]['RCI customer count mix']['residential'] \
                             / DSOmetadata['DSO_' + str(dso_num)]['number_of_gld_homes']

        # Placeholder code to add whether a customer is participating or not.
        # TODO: this should be done in prepare case and read in as part of GLD meter metadata.
        agent_file_name = 'Substation_' + str(dso_num) + '_agent_dict.json'
        agent_metadata = load_json(base_case + agent_prefix + str(dso_num), agent_file_name)

        metadata = customer_meta_data(metadata, agent_metadata, tariff_path)

        # List of month names, data paths, and day ranges to be used for energy bill creation
        # month_def = [
        #             ['Jan', 'C:/Users/reev057/PycharmProjects/DSO+T\Data/Slim2/case_slim_1', 2, 31],
        #             ['Feb', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_2', 2, 30],
        #             ['March', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_3', 2, 31],
        #             ['April', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_4', 2, 31],
        #             ['May', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_5', 2, 31],
        #             ['June', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_6', 2, 30],
        #             ['July', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_7', 2, 31],
        #             ['August', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_8', 2, 7],
        #             ['Sept', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_9', 2, 30],
        #             ['Oct', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_10', 2, 31],
        #             ['Nov', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_11', 2, 30],
        #             ['Dec', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Slim2/case_slim_12', 2, 7]]
        month_def = [['Jan', 'C:/Users/reev057/PycharmProjects/DSO+T/Data/Simdata\DER2/V1.1-1336-gb74f2d99/lean_8', 2, 4]]

        #  -------------- Calculate dataframe of monthly power consumption and peak power demand ---------
        process_meters = True
        if process_meters:

            for i in range(len(month_def)):
                for day_num in range(month_def[i][2], month_def[i][3]):
                    retail_data_df, retail_index_df = load_retail_data(month_def[i][1], agent_prefix, str(dso_num),
                                                                       str(day_num), 'retail_site')
                tic()
                meter_df, energysum_df = read_meters(metadata, month_def[i][1], GLD_prefix, str(dso_num),
                                                     list(range(month_def[i][2], month_def[i][3])), dso_scaling_factor,
                                                     metadata_path)
                print('Meter reading complete: DSO ' + str(dso_num) + ', Month ' + month_def[i][0])
                toc()

        #  -------------- Create dataframe with all monthly energy metrics and create annual sum ---------

        year_meter_df, year_energysum_df, year_trans_sum_df = annual_energy(month_def, GLD_prefix, str(dso_num),
                                                                            metadata)
        os.chdir(data_path)
        year_meter_df.to_hdf('energy_dso_' + str(dso_num) + '_data.h5', key='energy_data')
        year_energysum_df.to_hdf('energy_dso_' + str(dso_num) + '_data.h5', key='energy_sums')
        year_trans_sum_df.to_hdf('transactive_dso_' + str(dso_num) + '_data.h5', key='trans_data')

        required_revenue = 10000000

        DSO_Cash_Flows, DSO_Revenues_and_Energy_Sales, tariff, surplus = DSO_rate_making(data_path, dso_num, metadata,
                                                                                         required_revenue,
                                                                                         tariff_path,
                                                                                         dso_scaling_factor)

        # Example of getting an annual customer bill in dictionary form:
        customer = list(metadata['billingmeters'].keys())[0]
        cust_bill_file = data_path + '/bill_dso_' + str(dso_num) + '_data.h5'
        cust_bills = pd.read_hdf(cust_bill_file, key='cust_bill_data', mode='r')
        cust_energy = pd.read_hdf(data_path + '/energy_dso_' + str(dso_num) + '_data.h5', key='energy_data', mode='r')
        customer_bill = get_cust_bill(customer, cust_bills, metadata, cust_energy)

        print(DSO_Cash_Flows)
        print(DSO_Revenues_and_Energy_Sales)
        print(customer_bill)
        print(surplus)

# Need to read-in scaling factors at DSO level to scale to correct number of buildings.
# Need separate function to calculate the aggregate industrial bill.
# function to calculate transactive bill
# Need function to read in cashflow (balance) sheets
# what are unit testing requirements for this code...
# add function to sum up all energy charges by customer class.
# add blended rate by customer class
# Calculate load factor for each building and compare to ORNL data.
# Calculate energy consumption by class and compare it to DSO meta-data file (both customer counts and energy consumption)

if __name__ == '__main__':
    _testing()
