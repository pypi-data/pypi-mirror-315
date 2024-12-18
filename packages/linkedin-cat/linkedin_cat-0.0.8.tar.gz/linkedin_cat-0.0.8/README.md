
# Introduction
## Install package
```shell
pip install linkedin_cat
```
## Preparation

- create file `linkedin_cookies.json`

- please use Chrome Extension `EditThisCookie` to export linkedin cookies to `linkedin_cookies.json`



##  Example Usage:

## - Linkedin Send Message

```python
from linkedin_cat.message import LinkedinMessage

# linkedin cookie file path
linkedin_cookies_json='./linkedin_cookies.json'
# headless mode
headless = False
# Ininialized LinkedinMessage
bot = LinkedinMessage(linkedin_cookies_json,headless)

# message to sent, use FIRSTNAME or FULLNAME to customized the message
message = "Hello FIRSTNAME,hope you are doing well. Glad to e-meet with you on linkedin"

# Send single request by url
url = "https://www.linkedin.com/in/chandlersong/"
bot.send_single_request(url,message)

# Send multi request by linkedin url list 
urls_list = [    
    	"https://www.linkedin.com/in/chandlersong/",
    	"https://www.linkedin.com/in/chandlersong/",
        ]

bot.send_multi_request(urls_list,message)
    
```



## - Linkedin Search

```python
# linkein search

from linkedin_cat.search import LinkedinSearch

bot = LinkedinSearch(linkedin_cookies_json='cookies.json')

# 关键词搜索
results = bot.search_keywords('chandler song recruitment') 
# 返回 list 结果
for result in results:
    print(result)

# 按照搜索条件搜索, 自定义搜索条件
url = bot.generate_linkedin_search_url(keywords, company=None, title=None,school=None,first_name=None, last_name=None)
html = bot.open_linkedin_url(url)
results = bot.parse_linkedin_results(html)
for result in results:
    print(result)
	# {'name': '', 'title': '', 'location': '', 'introduction': '', 'linkedin_url': '', 'image_url': ''}

# 搜索linkedin profile，并保存为json文件
save_folder = './linkedin'
url = "https://www.linkedin.com/in/chandlersong/"
bot.search_linkedin_profile(url,save_folder)

# 批量搜索linkedin profile，并保存为json文件
save_folder = './linkedin'
url_list = [
    "https://www.linkedin.com/in/chandlersong/"
    "https://www.linkedin.com/in/chandlersong/"
    "https://www.linkedin.com/in/chandlersong/"
    ]

bot.search_linkedin_profile_list(url_list,save_folder)
```



## Recruiter LLM

```python
import os
from jinja2 import Template
from cn_detect.detect import ChineseNameDetect
from linkedin_cat.search import LinkedinSearch # 继承了LinkedinMessage
from llm_cat.deepseek_api import deepseek_chat

# 添加自定义模块路径
# import sys
# sys.path.append(r'C:\Users\s84336076\pyfunc')
# from llm import llm

# LinkedIn cookie文件路径
linkedin_cookies_json = "cookies.json"
headless = True
token = "sk-xxxxxxxxxxxxxxxxxxxxxx"

# 创建LinkedinSearch对象
search_bot = LinkedinSearch(linkedin_cookies_json,headless=headless)
detector = ChineseNameDetect()

def judge_skill_prompt(mini_profile):
    # 构建评估候选人的模板
    prompt_template = """
                            Please assess if the candidate in #### is a security engineer. 
                            If yes, return True; if not, return False. 
                            Provide the response in JSON format. 
                            example:
                            {
                                "result": True
                            }
                            \n\n 
                            ####{{ short_profile }}####
                        """
    template = Template(prompt_template)
    prompt = template.render(short_profile=mini_profile)

    # 使用LLM评估候选人
    # reply = llm(prompt)
    reply = deepseek_chat(prompt, token)
    print(reply)
    return reply


def search_recruiter(keywords, company=None, title=None, school=None, first_name=None, last_name=None,
                     chinese_detect=True, send_message=True, save_resume=True,
                     message=f"Hello FIRSTNAME, hope you are doing well. Glad to e-meet with you on LinkedIn."):
    page = 1
    while True:
        # 生成LinkedIn搜索URL
        url = search_bot.generate_linkedin_search_url(keywords, company, title, school, first_name, last_name)
        if page != 1:
            url += f'&page={page}'

        # 打开LinkedIn URL并解析结果
        html = search_bot.open_linkedin_url(url)
        results = search_bot.parse_linkedin_results(html)

        # 如果没有结果，退出循环
        if not results:
            print('No results')
            break

        print('Total Results:', len(results))
        for result in results:
            print(result)
            try:
                name = result['name']
                url = result['linkedin_url'].split('?')[0]

                mini_profile = {key: result[key] for key in ['title', 'introduction', 'location']}

                # 判断linkedin是否存在
                filename = search_bot.extract_username_from_linkedin_url(url) + '.json'
                if os.path.exists(os.path.join('./linkedin', filename)):
                    print(f'{filename} already exists, skipping...')
                    continue

                # 判断是否需要检测中文
                should_continue = not chinese_detect or detector.detect_chinese_word(name) or detector.detect_family_name(name)

                if should_continue:
                    reply = judge_skill_prompt(mini_profile)
                    if 'True' in reply:
                        # 发送消息
                        if send_message:
                            search_bot.send_single_request(url, message)
                        # 保存简历
                        if save_resume:
                            search_bot.search_linkedin_profile(url, thread_pool=True)

            except Exception as e:
                print(f"Error: {e}")

        # 翻页
        page += 1

# 使用示例
search_recruiter('security', company='google',last_name='jiang',send_message=False,save_resume=True)
```



