# 1. Shared table for tenants

## Performance

``` sh
docker run -e POSTGRES_PASSWORD=postgres --name psql postgres 
```

```sql
CREATE TABLE employee(id serial PRIMARY KEY, full_name text, manager_id int, company_id int);
```

| type | range |
| -- | -- |
| smallserial | 1 to 3j2,767 | 
| serial | 1 to 2,147,483,647 |
| bigserial | 1 to 9,223,372,036,854,775,807 |


```sql
INSERT INTO employee (
    full_name, manager_id, company_id
)
SELECT
    left(md5(i::text), 10),
    trunc(random()*100),
    trunc(random()*10)
FROM generate_series(1, 10000000) s(i);
```

```sql
SELECT * FROM employee LIMIT 50;
```

BUSCA EM ID

postgres=# EXPLAIN ANALYZE SELECT full_name FROM employee WHERE id=5000;

                                                       QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------
 Index Scan using employee_pkey on employee  (cost=0.42..8.44 rows=1 width=11) (actual time=0.034..0.035 rows=1 loops=1)
   Index Cond: (id = 5000)
 Planning Time: 2.967 ms
 Execution Time: 0.092 ms
(4 rows)

postgres=# EXPLAIN ANALYZE SELECT * FROM employee WHERE id=5001;

                                                       QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------
 Index Scan using employee_pkey on employee  (cost=0.42..8.44 rows=1 width=30) (actual time=0.104..0.109 rows=1 loops=1)
   Index Cond: (id = 5001)
 Planning Time: 0.286 ms
 Execution Time: 0.170 ms
(4 rows)

BUSCA EM MANAGER_ID PARA TODOS OS CAMPOS => SEQUENTIAL SCAN (PARALEL IN THIS CASE)

postgres=# EXPLAIN ANALYZE SELECT * FROM employee WHERE manager_id=50;

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


```sql
CREATE INDEX employee__manager_id_idx ON employee(manager_id);
```
PostgreSQL uses btree by default

HEAP SCAN

postgres=# EXPLAIN ANALYZE SELECT * FROM employee WHERE manager_id=51;

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

postgres=# SELECT count(id) FROM employee WHERE manager_id=51;
 count
-------
 10091
(1 row)


```sql
WITH RECURSIVE subordinate AS (
	SELECT id, manager_id, full_name
	FROM employee WHERE id = 2
	UNION
		SELECT e.id, e.manager_id, e.full_name
		FROM employee e
		INNER JOIN subordinate s ON s.id = e.manager_id
) SELECT * FROM subordinate;
```


postgres=# EXPLAIN ANALYZE WITH RECURSIVE subordinate AS (
	SELECT id, manager_id, full_name
	FROM employee WHERE id = 2
	UNION
		SELECT e.id, e.manager_id, e.full_name
		FROM employee e
		INNER JOIN subordinate s ON s.id = e.manager_id
) SELECT * FROM subordinate;
                                                                 QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------------------
 CTE Scan on subordinate  (cost=2311940.08..2511937.50 rows=9999871 width=40) (actual time=93.199..7130.447 rows=300094 loops=1)
   CTE subordinate
     ->  Recursive Union  (cost=0.43..2311940.08 rows=9999871 width=19) (actual time=93.194..7074.610 rows=300094 loops=1)
           ->  Index Scan using employee_pkey on employee  (cost=0.43..8.45 rows=1 width=19) (actual time=93.186..93.190 rows=1 loops=1)
                 Index Cond: (id = 2)
           ->  Hash Join  (cost=0.33..211193.42 rows=999987 width=19) (actual time=1140.019..1711.085 rows=75023 loops=4)
                 Hash Cond: (e.manager_id = s.id)
                 ->  Seq Scan on employee e  (cost=0.00..163693.71 rows=9999871 width=19) (actual time=0.008..564.394 rows=10000000 loops=4)
                 ->  Hash  (cost=0.20..0.20 rows=10 width=4) (actual time=15.859..15.859 rows=75024 loops=4)
                       Buckets: 131072 (originally 1024)  Batches: 2 (originally 1)  Memory Usage: 3073kB
                       ->  WorkTable Scan on subordinate s  (cost=0.00..0.20 rows=10 width=4) (actual time=1.941..7.825 rows=75024 loops=4)
 Planning Time: 0.871 ms
 JIT:
   Functions: 16
   Options: Inlining true, Optimization true, Expressions true, Deforming true
   Timing: Generation 12.688 ms, Inlining 8.712 ms, Optimization 58.021 ms, Emission 33.524 ms, Total 112.946 ms
 Execution Time: 7169.798 ms
(17 rows)

https://www.postgresql.org/docs/current/static/ltreehtml

```sql
CREATE TABLE position(
    id serial primary key,
    employee_id int,
    hierarchy_path ltree
);
CREATE INDEX employee__hierarchy_idx ON position USING gist (hierarchy_path);
CREATE INDEX employee__employee_id_idx ON position(employee_id);
```
Generalized Search Index (GiST)

```sql
INSERT INTO position(employee_id, hierarchy_path) VALUES ( 1, '1');
INSERT INTO position(employee_id, hierarchy_path) VALUES ( 2, '1.2');
INSERT INTO position(employee_id, hierarchy_path) VALUES ( 3, '1.3');
INSERT INTO position(employee_id, hierarchy_path) VALUES ( 4, '1.4');
INSERT INTO position(employee_id, hierarchy_path) VALUES ( 5, '5.1');
INSERT INTO position(employee_id, hierarchy_path) VALUES ( 6, '1.2.6');
INSERT INTO position(employee_id, hierarchy_path) VALUES ( 7, '1.2.7');
INSERT INTO position(employee_id, hierarchy_path) VALUES ( 8, '1.2.7.8');
```

postgres=# EXPLAIN ANALYZE SELECT employee_id FROM position WHERE hierarchy ~ '*.2.*';
                                                           QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on "position"  (cost=4.24..14.92 rows=12 width=4) (actual time=0.060..0.065 rows=4 loops=1)
   Recheck Cond: (hierarchy ~ '*.2.*'::lquery)
   Heap Blocks: exact=1
   ->  Bitmap Index Scan on employee__hierarchy_idx  (cost=0.00..4.23 rows=12 width=0) (actual time=0.038..0.038 rows=4 loops=1)
         Index Cond: (hierarchy ~ '*.2.*'::lquery)
 Planning Time: 2.594 ms
 Execution Time: 0.181 ms
(7 rows)

INSERT, UPDATE E DELETE COMPLEXOS

```sql
UPDATE position
SET hierarchy = text2ltree('9.1')::lpath || subpath(hierarchy,nlevel('9.1'))
WHERE hierarchy <@ '1';
```

```sql
DELETE position
SET hierarchy = text2ltree('9')::lpath || subpath(hierarchy,nlevel('9.1'))
WHERE hierarchy <@ '1';
```

# 2.  Schema-based

https://hackernoon.com/your-guide-to-schema-based-multi-tenant-systems-and-postgresql-implementation-gm433589

```sql
CREATE TABLE company(id serial PRIMARY KEY, name text);
```

```sql
CREATE SCHEMA org_1;
```

```sql
SET search_path TO org_1, public;
```

```sql
CREATE TABLE employee(id serial PRIMARY KEY, name text, manager_id int);
```

Cons
- DB management


# 3. Separate database per tenant (used in virtualization sample)

```sql
CREATE TABLE employee(id serial PRIMARY KEY, name text, manager_id int);
```

Cons
- DB management

# Postgresql configuration for high performance
https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization

````
postgresql.conf

data_directory = '/var/lib/pgsql/data'
hba_file = '/var/lib/pgsql/data/pg_hba.conf'
ident_file = '/var/lib/pgsql/data/pg_ident.conf'

port = 5432

max_connections = = GREATEST(4 x CPU cores, 100)
shared_buffers =  LEAST(RAM/2, 10GB)
work_mem = ((Total RAM - shared_buffers)/(16 x CPU cores))

authentication_timeout = 60
password_encryption = true
````

## Security

https://www.cybertec-postgresql.com/en/setting-up-ssl-authentication-for-postgresql/

### SSL
| File   |      Contents      |  Effect |
|----------|:-------------:|------:|
| '$PGDATA/server.crt' | server certificate | sent to client to indicate server's identity |
| '$PGDATA/server.key' | server private key | proves server certificate was sent by the owner; does not indicate certificate owner is trustworthy |
| '$PGDATA/root.crt' | trusted certificate authorities | checks that client certificate is signed by a trusted certificate authority |

```
# postgresql.conf
ssl_only = true
```

### Row Level Security

https://satoricyber.com/sql-server-security/sql-server-row-level-security/#:~:text=Row%2Dlevel%20security%20(RLS),number%20of%20exposed%20data%20rows

PostgreSQL 9.5 and newer includes a feature called Row Level Security (RLS). When you define security policies on a table, these policies restrict which rows in that table are returned by SELECT queries or which rows are affected by INSERT, UPDATE, and DELETE commands.

pgadmin

https://towardsdatascience.com/how-to-run-postgresql-and-pgadmin-using-docker-3a6a8ae918b5


# Consideration

Usar distribuição mais próxima da realidade para análise de performance

RH companies need to keep documents for a long timebox, maybe a soft delete for users and documents?