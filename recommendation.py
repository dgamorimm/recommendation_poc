from typing import Any
from tqdm import tqdm
from rich import print
import time
import json

def stopwatch(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Execution time: {end - start:.4f} seconds")
        return result
    return wrapper
# @stopwatch
def get_recommendation_item(data : dict, similar_list : list[dict], user_id : Any) -> list[tuple]:
    data_user = data[user_id]
    rating={}
    total_similarity={}
    # print(f'1 ::::::::::: Dados do Membro :::::::::::\nDados: {data_user.items()}')
    # for (item, grade) in tqdm(data_user.items()):
    for (item, grade) in data_user.items():
        # print(f'2 ::::::::::: Item & Avaliação :::::::::::\nItem: {item}\nAvaliação: {grade}')
        # print(f'3 ::::::::::: Lista de Itens Similares :::::::::::\nLista: {similar_list[item]}')
        for (similarity, item2) in similar_list[item]:
            # print(f'4 ::::::::::: Similaridade & Item2 :::::::::::\nSimilaridade: {similarity}\nItem2: {item2}')
            # print(f'5 ::::::::::: Se o voucher estiver no membro, ignora, pois só vai recomendar o que ele ainda nunca usou :::::::::::')
            if item2 in data_user: continue
            # print(f'6 ::::::::::: Se o voucher NÃO estiver no membro, segue para recomendar :::::::::::')
            rating.setdefault(item2, 0)
            # print(f'7 ::::::::: Rating :::::::::::\nItem: {rating}')
            rating[item2] += similarity * grade
            # print(f'8 ::::::::: Adicionar o Item2 no Rating Calculando a Similaridade * Quantidad de vezes que ele resgatou:::::::::::\nItem2: {item2}\nSimilaridade: {similarity}\nAvaliação: {grade}\nCalculo: {similarity * grade}')
            total_similarity.setdefault(item2, 0)
            # print(f'9 ::::::::: Adicionando Total Similaridade no Item2:::::::::::\nItem2: {item2}\nTotal: {similarity}')
            total_similarity[item2] += similarity
    rankings=[]
    # print(f'10 ::::::::: Total Similaridade :::::::::::\nTotal: {total_similarity.items()}')
    # print(f'11 ::::::::: Ratings Itens :::::::::::\nItem: {rating.items()}')
    for item, score in rating.items():
        # print(f'12 ::::::::: Ratings Itens & Score :::::::::::\nItem: {item}\nScore: {score}')
        try:
            rankings.append((score/total_similarity[item], item))
            # print(f'13 ::::::::: Calculando o ranking :::::::::::\nScore: {score}\nTotal Similaridade Item: {total_similarity[item]}\nCalculo: {(score/total_similarity[item], item)}')
        except ZeroDivisionError:
            rankings.append((0.0, item))
    
    rankings.sort()
    rankings.reverse()
    return rankings

if __name__ == '__main__':
    similars_bytes = open('datasets/reduce/output/similars.json')
    members_bytes = open('datasets/reduce/output/member_transform.json')
    
    similar =  json.load(similars_bytes)
    members =  json.load(members_bytes)
    
    # print(similars['Carteira da Nossa Nova Loja: Degalls'])
    
    print(get_recommendation_item(members, similar, '0lM5f000001SKWqEAO'))
    # 0lM5f000001ASnFEAW
    # 0lM5f000001RLluEAG
    # 0lM5f000001SKWqEAO
    similars_bytes.close()
    members_bytes.close()