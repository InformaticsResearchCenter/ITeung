# ITeung
IT service utility integrated

Requirements: 
1. Install Microsoft Visual Studio (Newer Version) with C/C++ Compiler installed.
2. Install CMAKE
3. Chrome and chromedriver
4. Install mysql server
5. set config.py file

## Keyword Development

### for single keyword : 
1. insert into keyword table, with a lot of same name of keyword_group and a lot of different possibility keyword 
2. insert into reply table, with a lot of same name of keyword_group and a lot of different reply content

### for multiple keyword : 
1. Insert into multi_key table, with multi keyword joined at one row using dash (-) in multiple_keyword column
2. insert into keyword table, with a row of keyword_group and a row of keyword which is same with multiple_keyword field in multi_key table
3. insert into reply table, with a lot of same name of keyword_group and a lot of different reply content

## Module Development

### for single keyword : 
1. The name of keyword_group is join string of : 'm: + module_name' , for example : m:prodi
2. insert into keyword table, with a lot of same name of keyword_group(example: m:prodi) and a lot of different possibility keyword 
3. Do not insert into reply table
4. create file with module_name.py inside module folder
5. in the module_name.py , at least have two function to interact with bot apps: def replymsg(driver, data): return message; and auth(data) return Boolean
6. driver is the webdriver for selenium command and msg is a string that come from user message.

### for multiple keyword : 
1. Insert into multi_key table, with multi keyword joined at one row using dash (-) in multiple_keyword column
2. The name of keyword_group is join string of : 'm: + module_name' , for example : m:prodi
2. insert into keyword table, with a row of keyword_group and a row of keyword which is same with multiple_keyword field in multi_key table
3. do not insert into reply table
4. create file with module_name.py inside module folder
5. in the module_name.py , at least have two function to interact with bot apps : def replymsg(driver, data): return message; and auth(data) return Boolean
6. driver is the webdriver for selenium command and msg is a string that come from user message.

### Module Content
Module development example:

```py
import config
import os
from lib import wa,reply

def auth(data):
	if authenticated:
		ret=True
	else:
		ret=False
	return ret
	
def replymsg(driver,data):
	xxx
	#if you module takes time, please set waiting message for user
	waitmessage=reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
        waitmessage = waitmessage.replace('#BOTNAME#', config.bot_name)
	wa.typeAndSendMessage(driver,waitmessage)
	xxx
	stringmessage=resultfromyourmodule
	return stringmessage
```

### Variabels in Message Reply
* #ERROR# for error message from python
* #BOTNAME# return bot name for reply message

details :
* kuncenvm.bat use for make sure vm is still on by using genymotion.
