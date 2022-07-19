tabela com coluna de organizacoes

# Performance

``` docker run -e POSTGRES_PASSWORD=postgres --name psql postgres```

```
CREATE TABLE employee(id serial PRIMARY KEY, name text, manager_id int, company_id int);
```

serial range 1 to 2147483647
bigserial range 1 to 9223372036854775807


```
INSERT INTO employee (
    name, manager_id, company_id
)
SELECT
    left(md5(i::text), 10),
    trunc(random()*100),
    trunc(random()*10),
FROM generate_series(1, 10000000) s(i);
```

```
SELECT * FROM employee LIMIT 50;
```

## Analysis

BUSCA EM ID

postgres=# explain analyze select name from employee where id=5000;

                                                       QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------
 Index Scan using employee_pkey on employee  (cost=0.42..8.44 rows=1 width=11) (actual time=0.034..0.035 rows=1 loops=1)
   Index Cond: (id = 5000)
 Planning Time: 2.967 ms
 Execution Time: 0.092 ms
(4 rows)

BUSCA EM ID COM CACHE COM RETORNO DE TODAS COLUNAS

postgres=# explain analyze select * from employee where id=5000;

                                                       QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------
 Index Scan using employee_pkey on employee  (cost=0.42..8.44 rows=1 width=30) (actual time=0.034..0.038 rows=1 loops=1)
   Index Cond: (id = 5000)
 Planning Time: 0.721 ms
 Execution Time: 0.084 ms  
(4 rows)

postgres=# explain analyze select * from employee where id=5001;

                                                       QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------
 Index Scan using employee_pkey on employee  (cost=0.42..8.44 rows=1 width=30) (actual time=0.104..0.109 rows=1 loops=1)
   Index Cond: (id = 5001)
 Planning Time: 0.286 ms
 Execution Time: 0.170 ms
(4 rows)

BUSCA EM MANAGER_ID PARA TODOS OS CAMPOS => SEQUENTIAL SCAN (PARALELL IN THIS CASE)

postgres=# explain analyze select * from employee where manager_id=50;

                                                       QUERY PLAN
------------------------------------------------------------------------------------------------------------------------
 Gather  (cost=1000.00..13561.43 rows=1 width=30) (actual time=27.489..35.435 rows=0 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   ->  Parallel Seq Scan on employee  (cost=0.00..12561.33 rows=1 width=30) (actual time=20.861..20.862 rows=0 loops=3)
         Filter: (manager_id = 50)
         Rows Removed by Filter: 333333
 Planning Time: 0.142 ms
 Execution Time: 35.461 ms
(8 rows)


```
CREATE INDEX employee__manager_id_idx on employee(manager_id);
```
PostgreSQL uses btree by default

HEAP SCAN

postgres=# explain analyze select * from employee where manager_id=51;

                                                             QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on employee  (cost=59.17..8677.00 rows=5000 width=72) (actual time=5.025..26.420 rows=10091 loops=1)
   Recheck Cond: (manager_id = 51)
   Heap Blocks: exact=6468
   ->  Bitmap Index Scan on employee__manager_id  (cost=0.00..57.92 rows=5000 width=0) (actual time=3.256..3.257 rows=10091 loops=1)
         Index Cond: (manager_id = 51)
 Planning Time: 0.931 ms
 Execution Time: 27.206 ms
(7 rows)

postgres=# select count(id) from employee where manager_id=51;
 count
-------
 10091
(1 row)




# Consideration

Usar distribuição mais próxima da realidade para análise de performance
RH companies need to keep documents for a long timebox, maybe a soft delete for users and documents?
