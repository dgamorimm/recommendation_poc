from rich import print
import polars as pl

df_voucher = pl.read_parquet('datasets/input/base_voucher.parquet')

print(df_voucher)
print('')

#só para ver se o voucher_code seria o id do beneficio
# result = df_voucher.filter(pl.col("name") == 'Ativação - Acesso Multi - MBS')

#filtrando por shopping para gerar uma base menor de dados
df_ssu = df_voucher.filter(pl.col("shopping") == 'SSU')

# Agrupando por 'voucher' e 'member_id' e contando as ocorrências
result = df_ssu.group_by(['member_id', 'name']).agg(
    [pl.count("name").alias("count")]
)

# só para ver se está contando mais que 1
# result = result.filter(pl.col("count") > 1)
# só para ver se o voucher se repete
# result = result.filter(pl.col("name") == 'Oficinas Pkb Kids Folia - PKB')


print(result)

result.write_parquet('datasets/reduce/output/member.parquet')
# 0lM5f000001AKDdEAO