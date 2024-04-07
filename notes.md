1 - _Para cada voucher, calcular a quantidade por membros que usaram (criar a base)_
2 - _Para cada membro, calcular todos os vouchers quantitativamente (criar a base)_
3 - _Calcular a simiaridade do para o item 1 d alista_
4 - Recomendar com os dados do item 2 passando o member_id
5 - Tenho que confrontar com o saldo
6 - Tenho que confrontar e ver se o beneficio esta ativo

> Lógica de aplicabilidade

- SIMILARIDADE
1. Primeiro ele pega um beneficio
2. Para cada beneficio que tem na lista ele verifica se os membros do primeiro beneficio estão nos outros beneficios da lista
3. Se esse caso ocorrer ele aplica o score da distancia euclidiana
4. Depois ele pega este primeiro beneficio e cria como chave uma lista de outros beneficios que são similares e o seu score
5. Faz isso como um plano cartesiano para todos os beneficios

- RECOMENDAÇÃO 
1. Tem que passar a lista de similaridade, a base de membros e seus beneficios resgatados individualmente, e o ID do membro que você deseja fazer a recomendação
2. Se o voucher NÃO estiver no membro, ou seja, ele nunca utilizou esse beneficio, segue para recomendar
3. Score: Ele pega a similaridade e multiplica pela quantidade de vezes que ele resgatou e adiciona a chave do beneficio que será recomendado de forma incremental
4. Total Similaridade: Salva nesse mesmo momento o total da similaridade para esse beneficio também de forma incremental
5. Percentual para recomendar : Aplica a normalização dividindo o score pelo total de similaridade do beneficio
6. Retorna uma lista em ordem decrescente avaliando o maior potencial para o menor em termos de recomendação

> Distancia Euclidiana

- Quanto mais próximo de 0 for o resultado da fórmula de similaridade, maior será a similaridade entre os pontos. Isso significa que os pontos são mais semelhantes entre si.
- Quanto mais próximo de 1 for o resultado da fórmula de similaridade, menor será a similaridade entre os pontos. Isso indica que os pontos são mais distintos entre si.

- Quanto mais próximo de 0, mais similaridade.
- Quanto mais próximo de 1, mais distância ou dissimilaridade.






