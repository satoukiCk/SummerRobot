# -*- coding:utf-8 -*-
from werobot import WeRoBot
import re
from weather import weather
from translation import translation
from werobot.replies import ArticlesReply, Article
from QSBK import QSBK
from logistics import logistics
from turing import TrRobot
from sae import memcache
from feedbackSQL import add_feedback


robot = WeRoBot(enable_session=False,
                token="",
                app_id='',
                app_secret='')


@robot.text
def turing(message):
    mc = memcache.Client()

    '''
    
    value = mc.get("some_key")
    mc.delete("some_key")
    value = mc.get("some_key")
    if value is None:
        return "nope"
    return value
    '''

    uid = str(message.source)
    stat = mc.get(uid)
    if stat is None:
        mc.set(uid, "0")
    msg = message.content.strip().lower().encode('utf8')
    if msg == 'bye':
        if stat != 'tr':
            return 'Goodbye.'
        mc.delete(uid)
        return "已退出图灵机器人，回到正常对话模式。"
    if stat == 'tr':
        reply = TrRobot(msg)
        data = reply.conversation()
        if data['code'] == 100000:
            return data['text']
        if data['code'] == 200000:
            reply = ArticlesReply(message=message)
            article = Article(
                title=data['text'],
                description="",
                img="",
                url=data['url']
            )
            reply.add_article(article)
            return reply
    if re.compile(".*?图灵机器人.*?").match(msg):
        mc.replace(uid,'tr',180)
        return "已进入图灵机器人对话模式。"



@robot.subscribe
def hello():
    return '你好，欢迎关注SummerRobot。回复"帮助"获取使用方法。'

@robot.unsubscribe
def cancel():
    return "再见！"


@robot.text
def receive_translation(message):
    msg = message.content.strip().lower().encode('utf8')
    if re.compile(".*?翻译:.*?").match(msg):
        if msg[7:] == '':
            return "请务必输入你的翻译内容。"
        if msg[7].isalpha():
            return translation(msg[7:],'en','zh').trans()
        else:
            return translation(msg[7:],'zh','en').trans()

'''
@robot.text
def echo(message):

    msg = message.content.strip().lower().encode('utf8')

    if re.compile(".*?你好.*?").match(msg) or\
        re.compile( ".*?嗨,*?").match(msg) or\
        re.compile(".*?hi.*?").match(msg) or\
        re.compile(".*?hello.*?").match(msg):
        #return message.source
        return "你好，欢迎关注(｀・ω・´)"
    elif re.compile(".*?厉害.*?").match(msg):
        return "我超厉害的!"
    elif re.compile(".*?美国总统.*?").match(msg):
        return "Donald Trump"
    elif re.compile(".*?quin.*?").match(msg):
        return "狗头人"
'''
@robot.text
def find_weather(message):
    msg = message.content.strip().lower().encode('utf8')
    if re.compile(".*?天气.*?").match(msg):
        position = msg.find('天气')
        if position==0:
            return "请问您要查询哪里的天气?"
        else:
            wea = weather(msg[0:position])
            return wea.get_weather()


@robot.text
def map(message):
    msg = message.content.strip().lower().encode('utf8')
    if re.compile(".*?导航:.*?").match(msg):
        if msg[7:] == "":
            return "请输入起点"
        position = msg.find(" ")
        if position==-1:
            return "请输入终点"
        src = msg[7:position]
        dst = msg[position+1:]
        reply = ArticlesReply(message=message)
        article = Article(
            title="查询结果",
            description="",
            img="",
            url=""
        )
        driving = Article(
            title="驾驶路线",
            description="",
            img="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1498549652503&di=ca8b8f886d0ed9a4a23af0979a3cd6bf&imgtype=0&src=http%3A%2F%2Fd15.lxyes.com%2F15xj%2Fprev%2F20150508%2F13%2F95695597.jpg",
            url="http://api.map.baidu.com/direction?origin=" + src + "&destination=" + dst + "&mode=driving&region=上海&output=html&src=SummerRobot"
        )
        walking = Article(
            title="步行路线",
            description="",
            img="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1498549689373&di=e5f637be0879d783161d3114842d9bca&imgtype=0&src=http%3A%2F%2Fi1.hdslb.com%2Fvideo%2F08%2F0830d621587a5b90d699d7000132c33c.jpg",
            url="http://api.map.baidu.com/direction?origin=" + src + "&destination=" + dst + "&mode=walking&region=上海&output=html&src=SummerRobot"
        )
        transit = Article(
            title="公交路线",
            description="",
            img="http://pic23.nipic.com/20120816/2900513_155030642132_2.jpg",
            url="http://api.map.baidu.com/direction?origin=" + src + "&destination=" + dst + "&mode=driving&region=上海&output=html&src=SummerRobot"
        )
        reply.add_article(article)
        reply.add_article(driving)
        reply.add_article(walking)
        reply.add_article(transit)
        return reply


@robot.text
def joke(message):
    msg = message.content.strip().lower().encode('utf8')
    if re.compile(".*?糗事百科.*?").match(msg):
        reply = QSBK()
        return reply.get_joke()

@robot.text
def logistics_info(message):
    msg = message.content.strip().lower().encode('utf8')
    if re.compile(".*?物流:.*?").match(msg):
        if msg[7:] == '':
            return "请输入物流单号"
        logistic_code = msg[7:]
        reply = logistics()
        return reply.show_order(lc=logistic_code)

'''
@robot.text
def turing_test(message):
    msg = message.content.strip().lower().encode('utf8')
    if re.compile(".*?图灵:.*?").match(msg):
        
'''

@robot.text
def feedback(message):
    msg = message.content.strip().lower().encode('utf8')
    if re.compile(".*?反馈:.*?").match(msg):
        if msg[7:] == '':
            return "请输入反馈内容"
        uid = str(message.source)
        return add_feedback(user_id=uid,content=msg[7:])


@robot.text
def help(message):
    msg = message.content.strip().lower().encode('utf8')
    if re.compile(".*?帮助.*?").match(msg):
        help_text = '本公众平台提供以下功能，请回复相应功能破折号后的内容进行互动ヾ(●´∀｀●) \n\n①、查询天气——城市 + "天气"\n②、中英互译——"翻译:" + 内容【请输入英文字符的冒号，下同】\n'\
                    '③、路线导航—— "导航:"+ 起点 + 空格 + 终点\n④、糗事百科段子——"糗事百科"\n⑤、查询快递物流——"物流:" + 物流单号\n⑥、图灵机器人对话模式——"图灵机器人"\n' \
                    '(进入该模式后，输入"bye"退出,或者3分钟后会自动退出)\n⑦、反馈功能——"反馈:" + 反馈内容'
        return help_text

@robot.text
def default(message):
    return '无类似功能。请回复"帮助"获取使用方法'
