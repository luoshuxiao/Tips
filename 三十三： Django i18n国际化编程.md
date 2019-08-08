#  django项目国际化: i18n -- 
**18表示Internationalization这个单词首字母I和结尾字母N之间的字母有18个**

	涉及到的包：
	from django.utils import translation
	from django.utils.translation import ugettext as _
### 1. 安装工具包： pip install gettext,需要注意的是，linux或者苹果系统下可以直接安装，windows系统下安装不成功的话，需要先下载另外一个工具：https://mlocati.github.io/articles/gettext-iconv-windows.html?tdsourcetag=s_pcqq_aiomsg，安装该工具后再安装gettext；

### 2. 在settings中配置存放语言转换的文件夹路径：
	LOCALE_PATHS = (
	    os.path.join(BASE_DIR, 'locale'),
	)
### 3. 在代码中将需要转换的语句通过ugettext转换
		from django.shortcuts import render
		from django.http import HttpResponse
		from django.utils import translation
		from django.utils.translation import ugettext as _
		
		
		def test(request):
		    user_language = request.GET.get('lang_code', 'en')  # 接受url的参数，设置语音
		    translation.activate(user_language)  # 将全局语言设置为user_language
		    output = _('hello my world!')
		    return HttpResponse(output)
        其中：
        后端将变量或者字符串语言类型转换： output = _('hello my world!')

        前端转换，需要在第一行加入load i18n：
		{% load i18n %}
		
		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <title>internationalization</title>
		</head>
		<body>
		       <!--第一种(推荐使用)-->
		       <div>{% blocktrans %}hello world!{% endblocktrans %}</div>
		       <!--第二种-->
		       <div>{% trans "ohell" %}</div>
		       <div>{{ data }}</div>
		</body>
		</html>
### 4. 生成语言转换文件：
    虚拟环境下输入命令： python manage.py makemessages -l zh_hans
    其中： zh_hans代表简体中文，ja代表日文，en代表英文等等
### 5. 在生成的语言文件夹下修改需要转换的语句：
    修改django.po文件中的msgstr，即将msgid的内容翻译成对应的语言，放在msgstr中
    其他代码不要动，如果在下面代码段中有出现  #fuzzy 说明有重复、模糊的翻译，

			#: .\internationlization\views.py:17
			msgid "i am back to forward"
			msgstr "私は後から前へ"
			
			#: .\templates\test.html:10
			msgid "hello world!"
			msgstr "ただいま"
			
			#: .\templates\test.html:11
			msgid "ohell"
			msgstr "ただ"
### 6. 如果修改了项目代码中需要转换的词语，需要再次生成语言文件进行更新替换：
     python manage.py makemessages

### 7. 修改语言文件后，再生成代码的编译文件django.mo：
    python manage.py compilemessages
    这个命令生成的是项目程序会编译的代码程序，不能随意更改