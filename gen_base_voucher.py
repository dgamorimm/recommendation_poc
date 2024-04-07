from rich import print
import polars as pl

df_voucher = pl.read_parquet('datasets/input/base_voucher.parquet')

print(df_voucher)
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
df_ssu = df_voucher.filter(pl.col("shopping") == 'SSU')


# Agrupando por 'voucher' e 'member_id' e contando as ocorrências
result = df_ssu.group_by(['name', 'member_id']).agg(
    [pl.count("member_id").alias("count")]
)

# só para ver se está contando mais que 1
# result = result.filter(pl.col("count") > 1)
# só para ver se o voucher se repete
# result = result.filter(pl.col("name") == 'Oficinas Pkb Kids Folia - PKB')


print(result)

result.write_parquet('datasets/reduce/output/voucher.parquet')
# 0lM5f0000015ftgEAA