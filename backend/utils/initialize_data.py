import pandas as pd
import mysql.connector
from datetime import datetime
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--creator_id', type=int, required=True)
    parser.add_argument('--organization_id', type=int, required=True)


    file_paths = ['file:///home/ngochainguyen/Documents/AIC/dong-nai/cpi_data.xlsx', 'file:///home/ngochainguyen/Documents/AIC/dong-nai/iip_data.xlsx']
    cpi_indexes = ('CPI', 'food_service', 'cereal', 'food', 'eating_out', 'beverage_cigarette', 'garment', 'housing', 'household_equipment', 'medicine_medical_service', 'communication', 'telecommunication', 'education', 'culture_entertainment_travel', 'other_good_services')
    iip_indexes = ('IIP', 'mining_industry', 'manufacturing_processing_industry', 'gas_electricity_industry', 'waste_treatment_water_supply', 'mineral_exploitation', 'food', 'cigarette', 'textile', 'costume', 'leather_product', 'paper_product', 'chemical_product', 'plastic_product',
                'non_metalic_mineral_product', 'prefabricated_metal_product', 'electrical_product', 'other_products', 'motor_vehicle', 
                'furniture', 'other_manufacturing_processing', 'water_supply', 'gas_electricity')
    args = parser.parse_args()
    creator_id = args.creator_id
    organization_id = args.organization_id
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='forecasting',
                                            user='hainn',
                                            password='@dmin@123')
        current_Date = datetime.now()
        cursor = connection.cursor()
        # convert date in the format you want
        formatted_date = current_Date.strftime('%Y-%m-%d %H:%M:%S')
        for path in file_paths:
            data = pd.read_excel(path, header=None)
            df = data.iloc[:, 1:]
            for time in range(df.shape[1]):
                data = df.iloc[:, time]
                year = data[0].year
                month = data[0].month
                data_dict = {}
                if 'cpi' in path:
                    data_dict = dict(zip(cpi_indexes, tuple(data[1:])))
                if 'iip' in path:
                    data_dict = dict(zip(iip_indexes, tuple(data[1:])))
                data_dict['year'] = year
                data_dict['month'] = month
                data_dict['created_at'] = current_Date
                data_dict['updated_at'] = current_Date
                data_dict['creator_id'] = creator_id
                data_dict['organization_id'] = organization_id
                data_dict['base_period'] = 2014

                if 'cpi' in path:
                    table = 'cpi'
                    placeholders = ', '.join(['%s'] * len(data_dict))
                    columns = ', '.join(data_dict.keys())
                    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)       
                    cursor.execute(sql, list(data_dict.values()))
                if 'iip' in path:
                    table = 'iip'
                    placeholders = ', '.join(['%s'] * len(data_dict))
                    columns = ', '.join(data_dict.keys())
                    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)       
                    cursor.execute(sql, list(data_dict.values()))
                
                
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into table")
        cursor.close()

    except mysql.connector.Error as error:
        connection.rollback()
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")



