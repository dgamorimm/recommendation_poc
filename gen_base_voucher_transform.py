
from rich import print
import polars as pl
import json

if __name__ == '__main__':
    df = pl.read_parquet('datasets/reduce/output/voucher.parquet')
    _list = df.to_dicts()
    print(_list[0:10])
    data = {}
    for item in _list:
        try:
            data[item['name']][item['member_id']] = item['count']
        except:
            data[item['name']] = {}
            data[item['name']][item['member_id']] = item['count']
    
    with open("datasets/reduce/output/voucher_transform.json", "w") as outfile:
        json.dump(data, outfile)