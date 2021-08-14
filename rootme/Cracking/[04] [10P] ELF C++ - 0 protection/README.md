## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Cracking/)] [[ELF C++ - 0 protection](https://www.root-me.org/en/Challenges/Cracking/ELF-C-0-protection)] [[解题报告](http://exp-blog.com/2019/02/25/pid-3384/)]

------

## 初步分析

不太水的水题，需要懂得反汇编工具的使用，以及一些汇编原理。

开始挑战后下载了一个 `ch25.bin` 文件，判断是 Linux 下编译的可执行二进制文件。

放到 Linux 下执行 `./ch25.bin`  （注意赋予 `x` 执行权限），提示使用方法为 `./ch25.bin password`

尝试输入任意密码执行，提示密码错误。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/01.png)

初步判断可能密码以常量方式存储在代码中。

使用文本编辑器打开，尝试搜索关键字 `password` ，发现一段常量文字，但是密码被隐藏其中：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/02.png)

看来只能 **反编译** 了。


------------

## 反汇编

Linux 下的反汇编可以直接使用 `objdump` 工具，执行以下命令生成反汇编源码：

`objdump ch25.bin -S >> ch25-src.asm`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/03.png)


```asm
;ch25-src.asm

ch25.bin:     file format elf32-i386


Disassembly of section .init:

08048738 <_init>:
 8048738:	53                   	push   %ebx
 8048739:	83 ec 08             	sub    $0x8,%esp
 804873c:	e8 7f 01 00 00       	call   80488c0 <__x86.get_pc_thunk.bx>
 8048741:	81 c3 bf 28 00 00    	add    $0x28bf,%ebx
 8048747:	8b 83 fc ff ff ff    	mov    -0x4(%ebx),%eax
 804874d:	85 c0                	test   %eax,%eax
 804874f:	74 05                	je     8048756 <_init+0x1e>
 8048751:	e8 3a 00 00 00       	call   8048790 <__gmon_start__@plt>
 8048756:	83 c4 08             	add    $0x8,%esp
 8048759:	5b                   	pop    %ebx
 804875a:	c3                   	ret    

Disassembly of section .plt:

08048760 <.plt>:
 8048760:	ff 35 04 b0 04 08    	pushl  0x804b004
 8048766:	ff 25 08 b0 04 08    	jmp    *0x804b008
 804876c:	00 00                	add    %al,(%eax)
	...

08048770 <__cxa_atexit@plt>:
 8048770:	ff 25 0c b0 04 08    	jmp    *0x804b00c
 8048776:	68 00 00 00 00       	push   $0x0
 804877b:	e9 e0 ff ff ff       	jmp    8048760 <.plt>

08048780 <_ZNSspLEc@plt>:
 8048780:	ff 25 10 b0 04 08    	jmp    *0x804b010
 8048786:	68 08 00 00 00       	push   $0x8
 804878b:	e9 d0 ff ff ff       	jmp    8048760 <.plt>

08048790 <__gmon_start__@plt>:
 8048790:	ff 25 14 b0 04 08    	jmp    *0x804b014
 8048796:	68 10 00 00 00       	push   $0x10
 804879b:	e9 c0 ff ff ff       	jmp    8048760 <.plt>

080487a0 <_ZNSsixEj@plt>:
 80487a0:	ff 25 18 b0 04 08    	jmp    *0x804b018
 80487a6:	68 18 00 00 00       	push   $0x18
 80487ab:	e9 b0 ff ff ff       	jmp    8048760 <.plt>

080487b0 <_ZNSt8ios_base4InitC1Ev@plt>:
 80487b0:	ff 25 1c b0 04 08    	jmp    *0x804b01c
 80487b6:	68 20 00 00 00       	push   $0x20
 80487bb:	e9 a0 ff ff ff       	jmp    8048760 <.plt>

080487c0 <__libc_start_main@plt>:
 80487c0:	ff 25 20 b0 04 08    	jmp    *0x804b020
 80487c6:	68 28 00 00 00       	push   $0x28
 80487cb:	e9 90 ff ff ff       	jmp    8048760 <.plt>

080487d0 <_ZNKSs6lengthEv@plt>:
 80487d0:	ff 25 24 b0 04 08    	jmp    *0x804b024
 80487d6:	68 30 00 00 00       	push   $0x30
 80487db:	e9 80 ff ff ff       	jmp    8048760 <.plt>

080487e0 <_ZNSt8ios_base4InitD1Ev@plt>:
 80487e0:	ff 25 28 b0 04 08    	jmp    *0x804b028
 80487e6:	68 38 00 00 00       	push   $0x38
 80487eb:	e9 70 ff ff ff       	jmp    8048760 <.plt>

080487f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>:
 80487f0:	ff 25 2c b0 04 08    	jmp    *0x804b02c
 80487f6:	68 40 00 00 00       	push   $0x40
 80487fb:	e9 60 ff ff ff       	jmp    8048760 <.plt>

08048800 <_ZNSsD1Ev@plt>:
 8048800:	ff 25 30 b0 04 08    	jmp    *0x804b030
 8048806:	68 48 00 00 00       	push   $0x48
 804880b:	e9 50 ff ff ff       	jmp    8048760 <.plt>

08048810 <_ZNKSs7compareEPKc@plt>:
 8048810:	ff 25 34 b0 04 08    	jmp    *0x804b034
 8048816:	68 50 00 00 00       	push   $0x50
 804881b:	e9 40 ff ff ff       	jmp    8048760 <.plt>

08048820 <_ZNSsC1EPKcRKSaIcE@plt>:
 8048820:	ff 25 38 b0 04 08    	jmp    *0x804b038
 8048826:	68 58 00 00 00       	push   $0x58
 804882b:	e9 30 ff ff ff       	jmp    8048760 <.plt>

08048830 <_ZNSaIcED1Ev@plt>:
 8048830:	ff 25 3c b0 04 08    	jmp    *0x804b03c
 8048836:	68 60 00 00 00       	push   $0x60
 804883b:	e9 20 ff ff ff       	jmp    8048760 <.plt>

08048840 <_ZNSolsEPFRSoS_E@plt>:
 8048840:	ff 25 40 b0 04 08    	jmp    *0x804b040
 8048846:	68 68 00 00 00       	push   $0x68
 804884b:	e9 10 ff ff ff       	jmp    8048760 <.plt>

08048850 <_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_@plt>:
 8048850:	ff 25 44 b0 04 08    	jmp    *0x804b044
 8048856:	68 70 00 00 00       	push   $0x70
 804885b:	e9 00 ff ff ff       	jmp    8048760 <.plt>

08048860 <_ZNSaIcEC1Ev@plt>:
 8048860:	ff 25 48 b0 04 08    	jmp    *0x804b048
 8048866:	68 78 00 00 00       	push   $0x78
 804886b:	e9 f0 fe ff ff       	jmp    8048760 <.plt>

08048870 <__gxx_personality_v0@plt>:
 8048870:	ff 25 4c b0 04 08    	jmp    *0x804b04c
 8048876:	68 80 00 00 00       	push   $0x80
 804887b:	e9 e0 fe ff ff       	jmp    8048760 <.plt>

08048880 <_Unwind_Resume@plt>:
 8048880:	ff 25 50 b0 04 08    	jmp    *0x804b050
 8048886:	68 88 00 00 00       	push   $0x88
 804888b:	e9 d0 fe ff ff       	jmp    8048760 <.plt>

Disassembly of section .text:

08048890 <_start>:
 8048890:	31 ed                	xor    %ebp,%ebp
 8048892:	5e                   	pop    %esi
 8048893:	89 e1                	mov    %esp,%ecx
 8048895:	83 e4 f0             	and    $0xfffffff0,%esp
 8048898:	50                   	push   %eax
 8048899:	54                   	push   %esp
 804889a:	52                   	push   %edx
 804889b:	68 90 8d 04 08       	push   $0x8048d90
 80488a0:	68 20 8d 04 08       	push   $0x8048d20
 80488a5:	51                   	push   %ecx
 80488a6:	56                   	push   %esi
 80488a7:	68 86 8a 04 08       	push   $0x8048a86
 80488ac:	e8 0f ff ff ff       	call   80487c0 <__libc_start_main@plt>
 80488b1:	f4                   	hlt    
 80488b2:	66 90                	xchg   %ax,%ax
 80488b4:	66 90                	xchg   %ax,%ax
 80488b6:	66 90                	xchg   %ax,%ax
 80488b8:	66 90                	xchg   %ax,%ax
 80488ba:	66 90                	xchg   %ax,%ax
 80488bc:	66 90                	xchg   %ax,%ax
 80488be:	66 90                	xchg   %ax,%ax

080488c0 <__x86.get_pc_thunk.bx>:
 80488c0:	8b 1c 24             	mov    (%esp),%ebx
 80488c3:	c3                   	ret    
 80488c4:	66 90                	xchg   %ax,%ax
 80488c6:	66 90                	xchg   %ax,%ax
 80488c8:	66 90                	xchg   %ax,%ax
 80488ca:	66 90                	xchg   %ax,%ax
 80488cc:	66 90                	xchg   %ax,%ax
 80488ce:	66 90                	xchg   %ax,%ax

080488d0 <deregister_tm_clones>:
 80488d0:	b8 5f b0 04 08       	mov    $0x804b05f,%eax
 80488d5:	2d 5c b0 04 08       	sub    $0x804b05c,%eax
 80488da:	83 f8 06             	cmp    $0x6,%eax
 80488dd:	77 01                	ja     80488e0 <deregister_tm_clones+0x10>
 80488df:	c3                   	ret    
 80488e0:	b8 00 00 00 00       	mov    $0x0,%eax
 80488e5:	85 c0                	test   %eax,%eax
 80488e7:	74 f6                	je     80488df <deregister_tm_clones+0xf>
 80488e9:	55                   	push   %ebp
 80488ea:	89 e5                	mov    %esp,%ebp
 80488ec:	83 ec 18             	sub    $0x18,%esp
 80488ef:	c7 04 24 5c b0 04 08 	movl   $0x804b05c,(%esp)
 80488f6:	ff d0                	call   *%eax
 80488f8:	c9                   	leave  
 80488f9:	c3                   	ret    
 80488fa:	8d b6 00 00 00 00    	lea    0x0(%esi),%esi

08048900 <register_tm_clones>:
 8048900:	b8 5c b0 04 08       	mov    $0x804b05c,%eax
 8048905:	2d 5c b0 04 08       	sub    $0x804b05c,%eax
 804890a:	c1 f8 02             	sar    $0x2,%eax
 804890d:	89 c2                	mov    %eax,%edx
 804890f:	c1 ea 1f             	shr    $0x1f,%edx
 8048912:	01 d0                	add    %edx,%eax
 8048914:	d1 f8                	sar    %eax
 8048916:	75 01                	jne    8048919 <register_tm_clones+0x19>
 8048918:	c3                   	ret    
 8048919:	ba 00 00 00 00       	mov    $0x0,%edx
 804891e:	85 d2                	test   %edx,%edx
 8048920:	74 f6                	je     8048918 <register_tm_clones+0x18>
 8048922:	55                   	push   %ebp
 8048923:	89 e5                	mov    %esp,%ebp
 8048925:	83 ec 18             	sub    $0x18,%esp
 8048928:	89 44 24 04          	mov    %eax,0x4(%esp)
 804892c:	c7 04 24 5c b0 04 08 	movl   $0x804b05c,(%esp)
 8048933:	ff d2                	call   *%edx
 8048935:	c9                   	leave  
 8048936:	c3                   	ret    
 8048937:	89 f6                	mov    %esi,%esi
 8048939:	8d bc 27 00 00 00 00 	lea    0x0(%edi,%eiz,1),%edi

08048940 <__do_global_dtors_aux>:
 8048940:	80 3d 8c b1 04 08 00 	cmpb   $0x0,0x804b18c
 8048947:	75 13                	jne    804895c <__do_global_dtors_aux+0x1c>
 8048949:	55                   	push   %ebp
 804894a:	89 e5                	mov    %esp,%ebp
 804894c:	83 ec 08             	sub    $0x8,%esp
 804894f:	e8 7c ff ff ff       	call   80488d0 <deregister_tm_clones>
 8048954:	c6 05 8c b1 04 08 01 	movb   $0x1,0x804b18c
 804895b:	c9                   	leave  
 804895c:	f3 c3                	repz ret 
 804895e:	66 90                	xchg   %ax,%ax

08048960 <frame_dummy>:
 8048960:	a1 00 af 04 08       	mov    0x804af00,%eax
 8048965:	85 c0                	test   %eax,%eax
 8048967:	74 1f                	je     8048988 <frame_dummy+0x28>
 8048969:	b8 00 00 00 00       	mov    $0x0,%eax
 804896e:	85 c0                	test   %eax,%eax
 8048970:	74 16                	je     8048988 <frame_dummy+0x28>
 8048972:	55                   	push   %ebp
 8048973:	89 e5                	mov    %esp,%ebp
 8048975:	83 ec 18             	sub    $0x18,%esp
 8048978:	c7 04 24 00 af 04 08 	movl   $0x804af00,(%esp)
 804897f:	ff d0                	call   *%eax
 8048981:	c9                   	leave  
 8048982:	e9 79 ff ff ff       	jmp    8048900 <register_tm_clones>
 8048987:	90                   	nop
 8048988:	e9 73 ff ff ff       	jmp    8048900 <register_tm_clones>

0804898d <_Z5ploufSsSs>:
 804898d:	55                   	push   %ebp
 804898e:	89 e5                	mov    %esp,%ebp
 8048990:	57                   	push   %edi
 8048991:	56                   	push   %esi
 8048992:	53                   	push   %ebx
 8048993:	83 ec 2c             	sub    $0x2c,%esp
 8048996:	8d 45 e3             	lea    -0x1d(%ebp),%eax
 8048999:	89 04 24             	mov    %eax,(%esp)
 804899c:	e8 bf fe ff ff       	call   8048860 <_ZNSaIcEC1Ev@plt>
 80489a1:	8d 45 e3             	lea    -0x1d(%ebp),%eax
 80489a4:	89 44 24 08          	mov    %eax,0x8(%esp)
 80489a8:	c7 44 24 04 b0 8d 04 	movl   $0x8048db0,0x4(%esp)
 80489af:	08 
 80489b0:	8b 45 08             	mov    0x8(%ebp),%eax
 80489b3:	89 04 24             	mov    %eax,(%esp)
 80489b6:	e8 65 fe ff ff       	call   8048820 <_ZNSsC1EPKcRKSaIcE@plt>
 80489bb:	8d 45 e3             	lea    -0x1d(%ebp),%eax
 80489be:	89 04 24             	mov    %eax,(%esp)
 80489c1:	e8 6a fe ff ff       	call   8048830 <_ZNSaIcED1Ev@plt>
 80489c6:	c7 45 e4 00 00 00 00 	movl   $0x0,-0x1c(%ebp)
 80489cd:	eb 5c                	jmp    8048a2b <_Z5ploufSsSs+0x9e>
 80489cf:	8b 45 e4             	mov    -0x1c(%ebp),%eax
 80489d2:	89 44 24 04          	mov    %eax,0x4(%esp)
 80489d6:	8b 45 0c             	mov    0xc(%ebp),%eax
 80489d9:	89 04 24             	mov    %eax,(%esp)
 80489dc:	e8 bf fd ff ff       	call   80487a0 <_ZNSsixEj@plt>
 80489e1:	0f b6 30             	movzbl (%eax),%esi
 80489e4:	8b 5d e4             	mov    -0x1c(%ebp),%ebx
 80489e7:	8b 45 10             	mov    0x10(%ebp),%eax
 80489ea:	89 04 24             	mov    %eax,(%esp)
 80489ed:	e8 de fd ff ff       	call   80487d0 <_ZNKSs6lengthEv@plt>
 80489f2:	89 c7                	mov    %eax,%edi
 80489f4:	89 d8                	mov    %ebx,%eax
 80489f6:	ba 00 00 00 00       	mov    $0x0,%edx
 80489fb:	f7 f7                	div    %edi
 80489fd:	89 d1                	mov    %edx,%ecx
 80489ff:	89 c8                	mov    %ecx,%eax
 8048a01:	89 44 24 04          	mov    %eax,0x4(%esp)
 8048a05:	8b 45 10             	mov    0x10(%ebp),%eax
 8048a08:	89 04 24             	mov    %eax,(%esp)
 8048a0b:	e8 90 fd ff ff       	call   80487a0 <_ZNSsixEj@plt>
 8048a10:	0f b6 00             	movzbl (%eax),%eax
 8048a13:	31 f0                	xor    %esi,%eax
 8048a15:	0f be c0             	movsbl %al,%eax
 8048a18:	89 44 24 04          	mov    %eax,0x4(%esp)
 8048a1c:	8b 45 08             	mov    0x8(%ebp),%eax
 8048a1f:	89 04 24             	mov    %eax,(%esp)
 8048a22:	e8 59 fd ff ff       	call   8048780 <_ZNSspLEc@plt>
 8048a27:	83 45 e4 01          	addl   $0x1,-0x1c(%ebp)
 8048a2b:	8b 45 e4             	mov    -0x1c(%ebp),%eax
 8048a2e:	89 44 24 04          	mov    %eax,0x4(%esp)
 8048a32:	8b 45 0c             	mov    0xc(%ebp),%eax
 8048a35:	89 04 24             	mov    %eax,(%esp)
 8048a38:	e8 63 fd ff ff       	call   80487a0 <_ZNSsixEj@plt>
 8048a3d:	0f b6 00             	movzbl (%eax),%eax
 8048a40:	84 c0                	test   %al,%al
 8048a42:	0f 95 c0             	setne  %al
 8048a45:	84 c0                	test   %al,%al
 8048a47:	75 86                	jne    80489cf <_Z5ploufSsSs+0x42>
 8048a49:	eb 2e                	jmp    8048a79 <_Z5ploufSsSs+0xec>
 8048a4b:	89 c3                	mov    %eax,%ebx
 8048a4d:	8d 45 e3             	lea    -0x1d(%ebp),%eax
 8048a50:	89 04 24             	mov    %eax,(%esp)
 8048a53:	e8 d8 fd ff ff       	call   8048830 <_ZNSaIcED1Ev@plt>
 8048a58:	89 d8                	mov    %ebx,%eax
 8048a5a:	89 04 24             	mov    %eax,(%esp)
 8048a5d:	e8 1e fe ff ff       	call   8048880 <_Unwind_Resume@plt>
 8048a62:	89 c3                	mov    %eax,%ebx
 8048a64:	8b 45 08             	mov    0x8(%ebp),%eax
 8048a67:	89 04 24             	mov    %eax,(%esp)
 8048a6a:	e8 91 fd ff ff       	call   8048800 <_ZNSsD1Ev@plt>
 8048a6f:	89 d8                	mov    %ebx,%eax
 8048a71:	89 04 24             	mov    %eax,(%esp)
 8048a74:	e8 07 fe ff ff       	call   8048880 <_Unwind_Resume@plt>
 8048a79:	8b 45 08             	mov    0x8(%ebp),%eax
 8048a7c:	83 c4 2c             	add    $0x2c,%esp
 8048a7f:	5b                   	pop    %ebx
 8048a80:	5e                   	pop    %esi
 8048a81:	5f                   	pop    %edi
 8048a82:	5d                   	pop    %ebp
 8048a83:	c2 04 00             	ret    $0x4

08048a86 <main>:
 8048a86:	8d 4c 24 04          	lea    0x4(%esp),%ecx
 8048a8a:	83 e4 f0             	and    $0xfffffff0,%esp
 8048a8d:	ff 71 fc             	pushl  -0x4(%ecx)
 8048a90:	55                   	push   %ebp
 8048a91:	89 e5                	mov    %esp,%ebp
 8048a93:	53                   	push   %ebx
 8048a94:	51                   	push   %ecx
 8048a95:	83 ec 20             	sub    $0x20,%esp
 8048a98:	89 cb                	mov    %ecx,%ebx
 8048a9a:	83 3b 01             	cmpl   $0x1,(%ebx)
 8048a9d:	7f 4f                	jg     8048aee <main+0x68>
 8048a9f:	8b 43 04             	mov    0x4(%ebx),%eax
 8048aa2:	8b 18                	mov    (%eax),%ebx
 8048aa4:	c7 44 24 04 b1 8d 04 	movl   $0x8048db1,0x4(%esp)
 8048aab:	08 
 8048aac:	c7 04 24 60 b0 04 08 	movl   $0x804b060,(%esp)
 8048ab3:	e8 38 fd ff ff       	call   80487f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
 8048ab8:	89 5c 24 04          	mov    %ebx,0x4(%esp)
 8048abc:	89 04 24             	mov    %eax,(%esp)
 8048abf:	e8 2c fd ff ff       	call   80487f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
 8048ac4:	c7 44 24 04 ba 8d 04 	movl   $0x8048dba,0x4(%esp)
 8048acb:	08 
 8048acc:	89 04 24             	mov    %eax,(%esp)
 8048acf:	e8 1c fd ff ff       	call   80487f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
 8048ad4:	c7 44 24 04 50 88 04 	movl   $0x8048850,0x4(%esp)
 8048adb:	08 
 8048adc:	89 04 24             	mov    %eax,(%esp)
 8048adf:	e8 5c fd ff ff       	call   8048840 <_ZNSolsEPFRSoS_E@plt>
 8048ae4:	bb 05 00 00 00       	mov    $0x5,%ebx
 8048ae9:	e9 2b 01 00 00       	jmp    8048c19 <main+0x193>
 8048aee:	8d 45 eb             	lea    -0x15(%ebp),%eax
 8048af1:	89 04 24             	mov    %eax,(%esp)
 8048af4:	e8 67 fd ff ff       	call   8048860 <_ZNSaIcEC1Ev@plt>
 8048af9:	8d 45 eb             	lea    -0x15(%ebp),%eax
 8048afc:	89 44 24 08          	mov    %eax,0x8(%esp)
 8048b00:	c7 44 24 04 c4 8d 04 	movl   $0x8048dc4,0x4(%esp)
 8048b07:	08 
 8048b08:	8d 45 f4             	lea    -0xc(%ebp),%eax
 8048b0b:	89 04 24             	mov    %eax,(%esp)
 8048b0e:	e8 0d fd ff ff       	call   8048820 <_ZNSsC1EPKcRKSaIcE@plt>
 8048b13:	8d 45 ea             	lea    -0x16(%ebp),%eax
 8048b16:	89 04 24             	mov    %eax,(%esp)
 8048b19:	e8 42 fd ff ff       	call   8048860 <_ZNSaIcEC1Ev@plt>
 8048b1e:	8d 45 ea             	lea    -0x16(%ebp),%eax
 8048b21:	89 44 24 08          	mov    %eax,0x8(%esp)
 8048b25:	c7 44 24 04 cc 8d 04 	movl   $0x8048dcc,0x4(%esp)
 8048b2c:	08 
 8048b2d:	8d 45 f0             	lea    -0x10(%ebp),%eax
 8048b30:	89 04 24             	mov    %eax,(%esp)
 8048b33:	e8 e8 fc ff ff       	call   8048820 <_ZNSsC1EPKcRKSaIcE@plt>
 8048b38:	8d 45 ec             	lea    -0x14(%ebp),%eax
 8048b3b:	8d 55 f4             	lea    -0xc(%ebp),%edx
 8048b3e:	89 54 24 08          	mov    %edx,0x8(%esp)
 8048b42:	8d 55 f0             	lea    -0x10(%ebp),%edx
 8048b45:	89 54 24 04          	mov    %edx,0x4(%esp)
 8048b49:	89 04 24             	mov    %eax,(%esp)
 8048b4c:	e8 3c fe ff ff       	call   804898d <_Z5ploufSsSs>
 8048b51:	83 ec 04             	sub    $0x4,%esp
 8048b54:	8d 45 f0             	lea    -0x10(%ebp),%eax
 8048b57:	89 04 24             	mov    %eax,(%esp)
 8048b5a:	e8 a1 fc ff ff       	call   8048800 <_ZNSsD1Ev@plt>
 8048b5f:	8d 45 ea             	lea    -0x16(%ebp),%eax
 8048b62:	89 04 24             	mov    %eax,(%esp)
 8048b65:	e8 c6 fc ff ff       	call   8048830 <_ZNSaIcED1Ev@plt>
 8048b6a:	8d 45 f4             	lea    -0xc(%ebp),%eax
 8048b6d:	89 04 24             	mov    %eax,(%esp)
 8048b70:	e8 8b fc ff ff       	call   8048800 <_ZNSsD1Ev@plt>
 8048b75:	8d 45 eb             	lea    -0x15(%ebp),%eax
 8048b78:	89 04 24             	mov    %eax,(%esp)
 8048b7b:	e8 b0 fc ff ff       	call   8048830 <_ZNSaIcED1Ev@plt>
 8048b80:	8b 43 04             	mov    0x4(%ebx),%eax
 8048b83:	83 c0 04             	add    $0x4,%eax
 8048b86:	8b 00                	mov    (%eax),%eax
 8048b88:	89 44 24 04          	mov    %eax,0x4(%esp)
 8048b8c:	8d 45 ec             	lea    -0x14(%ebp),%eax
 8048b8f:	89 04 24             	mov    %eax,(%esp)
 8048b92:	e8 60 01 00 00       	call   8048cf7 <_ZSteqIcSt11char_traitsIcESaIcEEbRKSbIT_T0_T1_EPKS3_>
 8048b97:	84 c0                	test   %al,%al
 8048b99:	74 4a                	je     8048be5 <main+0x15f>
 8048b9b:	c7 44 24 04 fc 8d 04 	movl   $0x8048dfc,0x4(%esp)
 8048ba2:	08 
 8048ba3:	c7 04 24 00 b1 04 08 	movl   $0x804b100,(%esp)
 8048baa:	e8 41 fc ff ff       	call   80487f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
 8048baf:	c7 44 24 04 50 88 04 	movl   $0x8048850,0x4(%esp)
 8048bb6:	08 
 8048bb7:	89 04 24             	mov    %eax,(%esp)
 8048bba:	e8 81 fc ff ff       	call   8048840 <_ZNSolsEPFRSoS_E@plt>
 8048bbf:	c7 44 24 04 34 8e 04 	movl   $0x8048e34,0x4(%esp)
 8048bc6:	08 
 8048bc7:	c7 04 24 00 b1 04 08 	movl   $0x804b100,(%esp)
 8048bce:	e8 1d fc ff ff       	call   80487f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
 8048bd3:	c7 44 24 04 50 88 04 	movl   $0x8048850,0x4(%esp)
 8048bda:	08 
 8048bdb:	89 04 24             	mov    %eax,(%esp)
 8048bde:	e8 5d fc ff ff       	call   8048840 <_ZNSolsEPFRSoS_E@plt>
 8048be3:	eb 24                	jmp    8048c09 <main+0x183>
 8048be5:	c7 44 24 04 65 8e 04 	movl   $0x8048e65,0x4(%esp)
 8048bec:	08 
 8048bed:	c7 04 24 00 b1 04 08 	movl   $0x804b100,(%esp)
 8048bf4:	e8 f7 fb ff ff       	call   80487f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
 8048bf9:	c7 44 24 04 50 88 04 	movl   $0x8048850,0x4(%esp)
 8048c00:	08 
 8048c01:	89 04 24             	mov    %eax,(%esp)
 8048c04:	e8 37 fc ff ff       	call   8048840 <_ZNSolsEPFRSoS_E@plt>
 8048c09:	bb 00 00 00 00       	mov    $0x0,%ebx
 8048c0e:	8d 45 ec             	lea    -0x14(%ebp),%eax
 8048c11:	89 04 24             	mov    %eax,(%esp)
 8048c14:	e8 e7 fb ff ff       	call   8048800 <_ZNSsD1Ev@plt>
 8048c19:	89 d8                	mov    %ebx,%eax
 8048c1b:	eb 75                	jmp    8048c92 <main+0x20c>
 8048c1d:	89 c3                	mov    %eax,%ebx
 8048c1f:	8d 45 f0             	lea    -0x10(%ebp),%eax
 8048c22:	89 04 24             	mov    %eax,(%esp)
 8048c25:	e8 d6 fb ff ff       	call   8048800 <_ZNSsD1Ev@plt>
 8048c2a:	eb 11                	jmp    8048c3d <main+0x1b7>
 8048c2c:	89 c3                	mov    %eax,%ebx
 8048c2e:	8d 45 ec             	lea    -0x14(%ebp),%eax
 8048c31:	89 04 24             	mov    %eax,(%esp)
 8048c34:	e8 c7 fb ff ff       	call   8048800 <_ZNSsD1Ev@plt>
 8048c39:	eb 02                	jmp    8048c3d <main+0x1b7>
 8048c3b:	89 c3                	mov    %eax,%ebx
 8048c3d:	8d 45 ea             	lea    -0x16(%ebp),%eax
 8048c40:	89 04 24             	mov    %eax,(%esp)
 8048c43:	e8 e8 fb ff ff       	call   8048830 <_ZNSaIcED1Ev@plt>
 8048c48:	8d 45 f4             	lea    -0xc(%ebp),%eax
 8048c4b:	89 04 24             	mov    %eax,(%esp)
 8048c4e:	e8 ad fb ff ff       	call   8048800 <_ZNSsD1Ev@plt>
 8048c53:	eb 11                	jmp    8048c66 <main+0x1e0>
 8048c55:	89 c3                	mov    %eax,%ebx
 8048c57:	8d 45 ec             	lea    -0x14(%ebp),%eax
 8048c5a:	89 04 24             	mov    %eax,(%esp)
 8048c5d:	e8 9e fb ff ff       	call   8048800 <_ZNSsD1Ev@plt>
 8048c62:	eb 02                	jmp    8048c66 <main+0x1e0>
 8048c64:	89 c3                	mov    %eax,%ebx
 8048c66:	8d 45 eb             	lea    -0x15(%ebp),%eax
 8048c69:	89 04 24             	mov    %eax,(%esp)
 8048c6c:	e8 bf fb ff ff       	call   8048830 <_ZNSaIcED1Ev@plt>
 8048c71:	89 d8                	mov    %ebx,%eax
 8048c73:	89 04 24             	mov    %eax,(%esp)
 8048c76:	e8 05 fc ff ff       	call   8048880 <_Unwind_Resume@plt>
 8048c7b:	89 c3                	mov    %eax,%ebx
 8048c7d:	8d 45 ec             	lea    -0x14(%ebp),%eax
 8048c80:	89 04 24             	mov    %eax,(%esp)
 8048c83:	e8 78 fb ff ff       	call   8048800 <_ZNSsD1Ev@plt>
 8048c88:	89 d8                	mov    %ebx,%eax
 8048c8a:	89 04 24             	mov    %eax,(%esp)
 8048c8d:	e8 ee fb ff ff       	call   8048880 <_Unwind_Resume@plt>
 8048c92:	8d 65 f8             	lea    -0x8(%ebp),%esp
 8048c95:	59                   	pop    %ecx
 8048c96:	5b                   	pop    %ebx
 8048c97:	5d                   	pop    %ebp
 8048c98:	8d 61 fc             	lea    -0x4(%ecx),%esp
 8048c9b:	c3                   	ret    

08048c9c <_Z41__static_initialization_and_destruction_0ii>:
 8048c9c:	55                   	push   %ebp
 8048c9d:	89 e5                	mov    %esp,%ebp
 8048c9f:	83 ec 18             	sub    $0x18,%esp
 8048ca2:	83 7d 08 01          	cmpl   $0x1,0x8(%ebp)
 8048ca6:	75 31                	jne    8048cd9 <_Z41__static_initialization_and_destruction_0ii+0x3d>
 8048ca8:	81 7d 0c ff ff 00 00 	cmpl   $0xffff,0xc(%ebp)
 8048caf:	75 28                	jne    8048cd9 <_Z41__static_initialization_and_destruction_0ii+0x3d>
 8048cb1:	c7 04 24 8d b1 04 08 	movl   $0x804b18d,(%esp)
 8048cb8:	e8 f3 fa ff ff       	call   80487b0 <_ZNSt8ios_base4InitC1Ev@plt>
 8048cbd:	c7 44 24 08 58 b0 04 	movl   $0x804b058,0x8(%esp)
 8048cc4:	08 
 8048cc5:	c7 44 24 04 8d b1 04 	movl   $0x804b18d,0x4(%esp)
 8048ccc:	08 
 8048ccd:	c7 04 24 e0 87 04 08 	movl   $0x80487e0,(%esp)
 8048cd4:	e8 97 fa ff ff       	call   8048770 <__cxa_atexit@plt>
 8048cd9:	c9                   	leave  
 8048cda:	c3                   	ret    

08048cdb <_GLOBAL__sub_I__Z5ploufSsSs>:
 8048cdb:	55                   	push   %ebp
 8048cdc:	89 e5                	mov    %esp,%ebp
 8048cde:	83 ec 18             	sub    $0x18,%esp
 8048ce1:	c7 44 24 04 ff ff 00 	movl   $0xffff,0x4(%esp)
 8048ce8:	00 
 8048ce9:	c7 04 24 01 00 00 00 	movl   $0x1,(%esp)
 8048cf0:	e8 a7 ff ff ff       	call   8048c9c <_Z41__static_initialization_and_destruction_0ii>
 8048cf5:	c9                   	leave  
 8048cf6:	c3                   	ret    

08048cf7 <_ZSteqIcSt11char_traitsIcESaIcEEbRKSbIT_T0_T1_EPKS3_>:
 8048cf7:	55                   	push   %ebp
 8048cf8:	89 e5                	mov    %esp,%ebp
 8048cfa:	83 ec 18             	sub    $0x18,%esp
 8048cfd:	8b 45 0c             	mov    0xc(%ebp),%eax
 8048d00:	89 44 24 04          	mov    %eax,0x4(%esp)
 8048d04:	8b 45 08             	mov    0x8(%ebp),%eax
 8048d07:	89 04 24             	mov    %eax,(%esp)
 8048d0a:	e8 01 fb ff ff       	call   8048810 <_ZNKSs7compareEPKc@plt>
 8048d0f:	85 c0                	test   %eax,%eax
 8048d11:	0f 94 c0             	sete   %al
 8048d14:	c9                   	leave  
 8048d15:	c3                   	ret    
 8048d16:	66 90                	xchg   %ax,%ax
 8048d18:	66 90                	xchg   %ax,%ax
 8048d1a:	66 90                	xchg   %ax,%ax
 8048d1c:	66 90                	xchg   %ax,%ax
 8048d1e:	66 90                	xchg   %ax,%ax

08048d20 <__libc_csu_init>:
 8048d20:	55                   	push   %ebp
 8048d21:	57                   	push   %edi
 8048d22:	31 ff                	xor    %edi,%edi
 8048d24:	56                   	push   %esi
 8048d25:	53                   	push   %ebx
 8048d26:	e8 95 fb ff ff       	call   80488c0 <__x86.get_pc_thunk.bx>
 8048d2b:	81 c3 d5 22 00 00    	add    $0x22d5,%ebx
 8048d31:	83 ec 1c             	sub    $0x1c,%esp
 8048d34:	8b 6c 24 30          	mov    0x30(%esp),%ebp
 8048d38:	8d b3 fc fe ff ff    	lea    -0x104(%ebx),%esi
 8048d3e:	e8 f5 f9 ff ff       	call   8048738 <_init>
 8048d43:	8d 83 f4 fe ff ff    	lea    -0x10c(%ebx),%eax
 8048d49:	29 c6                	sub    %eax,%esi
 8048d4b:	c1 fe 02             	sar    $0x2,%esi
 8048d4e:	85 f6                	test   %esi,%esi
 8048d50:	74 27                	je     8048d79 <__libc_csu_init+0x59>
 8048d52:	8d b6 00 00 00 00    	lea    0x0(%esi),%esi
 8048d58:	8b 44 24 38          	mov    0x38(%esp),%eax
 8048d5c:	89 2c 24             	mov    %ebp,(%esp)
 8048d5f:	89 44 24 08          	mov    %eax,0x8(%esp)
 8048d63:	8b 44 24 34          	mov    0x34(%esp),%eax
 8048d67:	89 44 24 04          	mov    %eax,0x4(%esp)
 8048d6b:	ff 94 bb f4 fe ff ff 	call   *-0x10c(%ebx,%edi,4)
 8048d72:	83 c7 01             	add    $0x1,%edi
 8048d75:	39 f7                	cmp    %esi,%edi
 8048d77:	75 df                	jne    8048d58 <__libc_csu_init+0x38>
 8048d79:	83 c4 1c             	add    $0x1c,%esp
 8048d7c:	5b                   	pop    %ebx
 8048d7d:	5e                   	pop    %esi
 8048d7e:	5f                   	pop    %edi
 8048d7f:	5d                   	pop    %ebp
 8048d80:	c3                   	ret    
 8048d81:	eb 0d                	jmp    8048d90 <__libc_csu_fini>
 8048d83:	90                   	nop
 8048d84:	90                   	nop
 8048d85:	90                   	nop
 8048d86:	90                   	nop
 8048d87:	90                   	nop
 8048d88:	90                   	nop
 8048d89:	90                   	nop
 8048d8a:	90                   	nop
 8048d8b:	90                   	nop
 8048d8c:	90                   	nop
 8048d8d:	90                   	nop
 8048d8e:	90                   	nop
 8048d8f:	90                   	nop

08048d90 <__libc_csu_fini>:
 8048d90:	f3 c3                	repz ret 

Disassembly of section .fini:

08048d94 <_fini>:
 8048d94:	53                   	push   %ebx
 8048d95:	83 ec 08             	sub    $0x8,%esp
 8048d98:	e8 23 fb ff ff       	call   80488c0 <__x86.get_pc_thunk.bx>
 8048d9d:	81 c3 63 22 00 00    	add    $0x2263,%ebx
 8048da3:	83 c4 08             	add    $0x8,%esp
 8048da6:	5b                   	pop    %ebx
 8048da7:	c3                   	ret
```

从源码可知这是一个 32 位的 ELF 文件，但是纯文本的组织方式不好分析代码。

这里改用 Windows 的 IDA 工具打开 `ch25.bin` 文件（注意使用 `ELF for Intel 386` 方式打开）。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/04.png)

从左侧的 `Fouction name` 列表找到 `main` 函数，定位到 `main` 函数的代码块。

在代码块的最后有一个条件分支语句 `jg      short loc_8048AEE`

根据图例可知，当 `loc_8048AEE <= 0` 时，代码会走红色分支；而当 `loc_8048AEE > 0` 时，代码会走绿色分支。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/05.png)

跟踪红色分支，发现分支代码中的一些常量字符串就是前面在 Linux 运行脚本时，没有给定 password 入参时的使用说明，说明这个红色分支不是我们的目标分支。

由此也可以推断，绿色分支的功能就是当我们给定 password 入参时，进行密码比较的代码分支。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/06.png)


------------

## 定位关键代码

进而分析绿色分支的代码块，暂时看不出个所以然，但是在这个代码块的最后依然有一个条件分支语句 `jz      short loc_8048BE5` 。

根据图例可知，当 `loc_8048BE5 != 0` 时，代码会走红色分支；而当 `loc_8048AEE == 0` 时，代码会走绿色分支，其中从红绿分支代码中的常量字符串中可以知道，当 password 正确时会走红色分支，而当 password 错误时会走绿色分支。

而影响 `loc_8048BE5` 值的是前面一个调用的一个名为 `_ZSteqIcSt11char_traitsIcESaIcEEbRKSbIT_T0_T1_EPKS3_` 的函数。

分析可知该函数作用是比较两个字符串是否相同，其中入参 1 是一个字符串变量（推断就是脚本输入的 password），而入参 2 是一个字符串常量（推断就是真正的 password）。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/07.png)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/08.png)

很明显，真正的密码就隐藏在 `_ZSteqIcSt11char_traitsIcESaIcEEbRKSbIT_T0_T1_EPKS3_` 函数前面的代码块。

发现这部分代码块中用到了两个变量 `unk_8048DC4` 和 `unk_8048DCC` ：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/09.png)

跟踪这两个变量到数据段，发现不是直接可读的字符串，推测是做了某些运算。

但是从汇编代码直接分析做了什么操作还是有点麻烦的，于是我决定走个捷径：

在 `_ZSteqIcSt11char_traitsIcESaIcEEbRKSbIT_T0_T1_EPKS3_` 函数做断点，直接通过 debug 从内存获取函数参数 2 （即真正 password ）的值。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/10.png)


------------

## DEBUG

回到 Linux 系统，这次使用 `gdb` 工具进行 debug 调试。

输入命令 `gdb ch25.bin` 进入 debug 模式：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/11.png)

通过输入 `layout asm` 命令可以查看反汇编源码，此时通过键盘的 `↑` 或 `↓` 按键可以查看汇编代码，找到 `_ZSteqIcSt11char_traitsIcESaIcEEbRKSbIT_T0_T1_EPKS3_` 函数，发现该函数的地址为 `0x8048b92` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/12.png)

知道地址就可以添加断点了，输入命令：`break *0x8048b92` （注意 `*` 不能丢，表示地址指针）。

`gdb` 提示成功在 `0x8048b92` 位置添加了 1 号断点。

此时输入命令 `info break` 可以查看当前的断点信息。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/13.png)


执行命令 `r www.exp-blog.com` （其中 `r` 是命令 `run` 的缩写，表示运行代码，后面的是给代码的入参，任意值均可，如此处为 `www.exp-blog.com` ），代码运行到前面设置的断点处暂停了。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/14.png)


------------

## 查看内存值

现在要查看函数 `_ZSteqIcSt11char_traitsIcESaIcEEbRKSbIT_T0_T1_EPKS3_` 的内存值。

需知道函数内存是存储在【栈】的，因此我们需要查看【栈指针】 ESP（Extended stack pointer） 的内容。

输入命令 `x/50wx $esp` 查看栈指针 ESP 当前所指向的栈中，从栈顶开始向后 50 个单位所存储的内容。

> `x/50wx` 命令释义：
<br/>　　　　*x ： examine 命令的缩写，用于查看内存地址中的值*
<br/>　　　　*/ ： 分隔符，前面是命令名称，后面是控制输出内容的格式*
<br/>　　　　*50 ： 表示取 50 个单位（数值任意控制均可）*
<br/>　　　　*w ： 表示每个单位的长度为 4 字节*
<br/>　　　　*x ： 表示按十六进制显示*

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/15.png)

不难发现均是地址值（需要知道这些地址每次运行程序都会变化的），为了查看真正的内容，

再输入命令 `x/s address` 查看特定地址中存储的值，如：`x/s 0x08050c8c` 。

> `x/s` 命令释义：
<br/>　　　　*x ： examine 命令的缩写，用于查看内存地址中的值*
<br/>　　　　*/ ： 分隔符，前面是命令名称，后面是控制输出内容的格式*
<br/>　　　　*s ： 表示按字符串形式显示*

有兴趣可以每个地址都查一下内容是什么，这里我就不逐个看了。

第一行第二列的地址，存储的就是入参 1 的值，亦即前面我们随意输入的 `www.exp-blog.com` 。

第二行第二列的地址，存储的就是入参 2 的值，亦即前面我们推测的真正的密码，可以发现其值为 `Here_you_have_to_understand_a_little_C++_stuffs` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/16.png)

为了验证猜想，我们退出 `gdb` 模式执行脚本，输入命令：

`./ch25.bin Here_you_have_to_understand_a_little_C++_stuffs`

提示密码正确，猜测是对的。完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B04%5D%20%5B10P%5D%20ELF%20C%2B%2B%20-%200%20protection/imgs/17.png)



------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
