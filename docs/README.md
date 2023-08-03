## 记录

### python venv

```
pyenv virtualenv system slack-todo
pyenv local slack-todo
```

### 文档

- [slackapi/python-slack-sdk: Slack Developer Kit for Python](https://github.com/slackapi/python-slack-sdk) 
- [Python Slack SDK — Python Slack SDK](https://slack.dev/python-slack-sdk/) 
- [slack_sdk.web.client API documentation](https://slack.dev/python-slack-sdk/api-docs/slack_sdk/web/client.html#slack_sdk.web.client.WebClient) **看这个**


### 遇到的问题

#### urlopen error EOF occurred in violation of protocol 

```
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/urllib/request.py", line 1391, in https_open
    return self.do_open(http.client.HTTPSConnection, req,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/urllib/request.py", line 1351, in do_open
    raise URLError(err)
urllib.error.URLError: <urlopen error EOF occurred in violation of protocol (_ssl.c:1002)>
```

- [Getting error EOF occurred in violation of protocol (_ssl.c:1123) slack-app · Issue #227 · slackapi/bolt-python](https://github.com/slackapi/bolt-python/issues/227) 


##### 解决

```
WebClient(proxy='xxxx')
```

也可以通过设置 `HTTPS_PROXY`, `HTTP_PROXY` 环境变量解决



#### unable to get local issuer certificate

```
  File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/urllib/request.py", line 1351, in do_open
    raise URLError(err)
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1002)>
```

- [SSL Certification error · Issue #334 · slackapi/python-slack-sdk](https://github.com/slackapi/python-slack-sdk/issues/334#issuecomment-571818369) 

##### 解决

```
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

WebClient(ssl=ssl_context)
```

