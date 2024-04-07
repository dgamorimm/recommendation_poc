from rich import print
import polars as pl
import json

df_voucher = pl.read_parquet('datasets/input/base_voucher.parquet')

# print(df_voucher)
print('')

#só para ver se o voucher_code seria o id do beneficio
# result = df_voucher.filter(pl.col("name") == 'Ativação - Acesso Multi - MBS')

# Agrupando por shooping para ver a volumetria de cada
# result = df_voucher.group_by(['shopping']).agg(
#     [pl.count("shopping").alias("count")]
# )
# result = result.sort('count')
# print(result)

#filtrando por shopping para gerar uma base menor de dados
df= df_voucher.filter(pl.col("shopping") != '')

df_unique_shoppings = df.select(pl.col("shopping")).unique()
shopping_list = df_unique_shoppings['shopping'].to_list()

df = df.select(pl.col("name"), pl.col("shopping"))

df_new = pl.DataFrame()
for shopping in shopping_list:
    df_shopping = df.filter(pl.col("shopping") == shopping)
    df_group_by = df_shopping.group_by(['name', 'shopping']).agg(
        [pl.count("name").alias("count")]
    )
    df_sorted = df_group_by.sort('count', descending=True)
    df_top_10 = df_sorted.head(10)
    unique_shopping_list = df_top_10['shopping'].unique().to_list()
    vouchers_list = json.dumps(df_top_10['name'].to_list())
    df_transform = pl.DataFrame({'shoppings' : unique_shopping_list, 'vouchers_recommendation' : vouchers_list})
    df_new.vstack(df_transform, in_place=True)  # vai concatenado os dfs

print(df_new)


print(df_group_by_top_10_shoppings)

# result.write_parquet('datasets/reduce/output/voucher.parquet')