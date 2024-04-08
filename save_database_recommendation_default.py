from rich import print
import polars as pl
import json

# df_voucher = pl.read_parquet('datasets/input/base_voucher.parquet')
df_voucher = pl.read_parquet('datasets\\input\\base_voucher.parquet')  #windows

# Set the maximum string length to display without truncation
# pl.Config.set_fmt_str_lengths(900)

# # Set the maximum table width in characters
# pl.Config.set_tbl_width_chars(900)

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


# uri = "sqlite:////home/dgamorim/development/recomendation_poc/database/recommendation.db?charset=utf8"
uri = f'sqlite:///C:/Users/dpinheiro/development/recommendation_poc/database/recommendation.db' # windows
table_name = "recommendation_default"
df_new.write_database(table_name=table_name, connection=uri, if_table_exists='append')