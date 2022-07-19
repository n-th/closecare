tabela com coluna de organizacoes

# Performance

docker run -e POSTGRES_PASSWORD=postgres --name psql postgres


CREATE TABLE employee(id serial PRIMARY KEY, name text, manager_id int, company_id text);

INSERT INTO employee (
    name, manager_id, company_id
)
SELECT
    left(md5(i::text), 10),
    trunc(random()*100),
    right(md5(i::text), 10)
FROM generate_series(1, 1000000) s(i);


SELECT * FROM employee LIMIT 10;



###BUSCA EM ID
postgres=# explain analyze select name from employee where id=5000;
                                                       QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------
 Index Scan using employee_pkey on employee  (cost=0.42..8.44 rows=1 width=11) (actual time=0.034..0.035 rows=1 loops=1)
   Index Cond: (id = 5000)
 Planning Time: 2.967 ms
 Execution Time: 0.092 ms
(4 rows)

###BUSCA EM ID COM CACHE
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

###BUSCA EM MANAGER_ID PARA TODOS OS CAMPOS => SEQUENTIAL SCAN
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



