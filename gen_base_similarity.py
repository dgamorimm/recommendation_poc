from math import sqrt
from tqdm import tqdm
from rich import print
import json
import time

def stopwatch(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Execution time: {end - start:.4f} seconds")
        return result
    return wrapper

def __euclidian(data : dict, object1 : str, object2 : str) -> float:
    
    # result = sum([
    #     pow(data[object1][item] - data[object2][item],2)
    #     for item in data[object1] if item in data[object2]
    # ])
    
    result_list = []
    for item in data[object1]:
        # print(f'5 ::::::::: Item dentro da base de voucher, pelo objeto 1 :::::::::::\nObjeto1: {object1}')
        if item in data[object2]:
            # print(f'6 ::::::::: Se item estiver dentro do Objeto2 :::::::::::\nObjeto2: {object2}\nDados Objeto2: {data[object2]}\nItem: {item}')
            sub = data[object1][item] - data[object2][item]
            # print(f'7 ::::::::: Subtrai o item do objeto 1 pelo item do objeto 2 :::::::::::\nObjeto1: {data[object1][item]}\nObjeto2: {data[object2][item]}\nSubtração: {sub}')
            elv = pow(sub,2)
            # print(f'8 ::::::::: Elevando a subtração ao quadrado :::::::::::\nSubtração: {sub}\nElevado ao Quadrado: {elv}')
            result_list.append(elv)
            
    if len(result_list) == 0: return 0
    result_sum = sum(result_list)
    # print(f'9 ::::::::: Somando a lista de resultados dos itens  :::::::::::\nSoma: {result_sum}')
    euclidian_distance = (1/(1 + sqrt(result_sum)))
    # print(f'10 ::::::::: Aplicando a fórmula estatistica da distância euclidiana  :::::::::::\nDistancia Euclidiana: {euclidian_distance}')
    return euclidian_distance
    # return (1/(1 + sqrt(result)))

def __get_similar(data : list[dict], object1 : str):
    # similarity = [
    #     (__euclidian(data, object1, object2), object2)
    #     for object2 in data if object2 != object1
        
    # ]
    similarity = []
    for object2 in data:
        # print(f'2 ::::::::: Objeto2 para Comparar :::::::::::\nObjeto2: {object2}')
        if object2 != object1:
            # print(f'3 ::::::::: Se Objeto2 for diferente de Objeto1 :::::::::::\nObjeto1: {object1}\nObjeto2: {object2}')
            # print(f'4 ::::::::: Calcular a Distancia Euclidiana :::::::::::')
            similarity.append((__euclidian(data, object1, object2), object2))
    similarity.sort()
    similarity.reverse()

    return similarity

@stopwatch
def calculate_similar_items(data: dict) -> list[dict]:
    result = {}
    for item in tqdm(data):
        # print(f'1 ::::::::: Dados dos Vouchers :::::::::::\nItem: {item}')
        vouchers = __get_similar(data, item)
        result[item] = vouchers
    return result

if __name__ == '__main__':
    # qty_vouchers = json.load(open('datasets/output/voucher_transform.json'))
    # qty_vouchers = json.load(open('datasets/reduce/output/voucher_transform.json'))
    qty_vouchers = json.load(open('datasets\\reduce\\output\\voucher_transform.json'))  #windows
    # esse processo aqui pode ser demorado, portanto, devemos ter uma base pré calculada e o custo pode ser alto
    data = calculate_similar_items(qty_vouchers)
    
    # with open("datasets/reduce/output/similars.json", "w") as outfile:
    with open("datasets\\reduce\\output\\similars.json", "w") as outfile:  #windows
        json.dump(data, outfile)
        