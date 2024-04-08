
from rich import print
import polars as pl
import json

if __name__ == '__main__':
    # df = pl.read_parquet('datasets/reduce/output/member.parquet')
    df = pl.read_parquet('datasets\\reduce\\output\\member.parquet')  #windows
    _list = df.to_dicts()
    print(_list[0:10])
    data = {}
    for item in _list:
        try:
            data[item['member_id']][item['name']] = item['count']
        except:
            data[item['member_id']] = {}
            data[item['member_id']][item['name']] = item['count']
    
    # with open("datasets/reduce/output/member_transform.json", "w") as outfile:
    with open("datasets\\reduce\\output\\member_transform.json", "w") as outfile:  #windows
        json.dump(data, outfile)