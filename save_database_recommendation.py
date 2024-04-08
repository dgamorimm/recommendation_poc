from recommendation import get_recommendation_item
from rich import print
from tqdm import tqdm
import polars as pl
import json

if __name__ == '__main__':
    # similars_bytes = open('datasets/reduce/output/similars.json')
    similars_bytes = open('datasets\\reduce\\output\\similars.json')  #windows
    # members_bytes = open('datasets/reduce/output/member_transform.json')
    members_bytes = open('datasets\\reduce\\output\\member_transform.json')  #windows
    
    similar =  json.load(similars_bytes)
    members =  json.load(members_bytes)
    
    # df = pl.read_parquet('datasets/reduce/output/member.parquet')
    df = pl.read_parquet('datasets\\reduce\\output\\member.parquet')  #windows
    _list = df.to_dicts()
    data = {'members': [], 'vouchers_recommendation' : []}
    id = 0
    for item in tqdm(_list):
        member = item.get('member_id')
        recommendations = get_recommendation_item(members, similar, member)
        data['members'].append(member)
        # id += 1
        # data['id'].append(id)
        vouchers = []
        for percentage, voucher in recommendations:
            if percentage > 0.0:
                vouchers.append(voucher)
        data['vouchers_recommendation'].append(json.dumps(vouchers))
        
    
    df = pl.DataFrame(data)
    print(df)
    
    # uri = "sqlite:////home/dgamorim/development/recomendation_poc/database/recommendation.db?charset=utf8"
    uri = f'sqlite:///C:/Users/dpinheiro/development/recommendation_poc/database/recommendation.db' # windows
    table_name = "recommendation"

    df.write_database(table_name=table_name, connection=uri, if_table_exists='append')
    
    similars_bytes.close()
    members_bytes.close()