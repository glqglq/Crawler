#-*- encoding:utf-8 -*-

from test.textteaser import TextTeaser
import time

content1 = u"""据央视新闻报道，当地时间2017年6月3日晚，北京时间今天凌晨，英国伦敦的地标建筑伦敦桥附近，一辆汽车冲撞行人。
英国伦敦恐袭事件现场
据BBC快讯：伦敦桥撞人事件发生后，至少一人死亡，英国警方正在搜捕三名可能携带武器的嫌疑人。
英国伦敦恐袭事件现场
据报道，该车辆为一辆白色厢式货车。事发时，BBC记者Holly Jones当时正在现场。据她报道，撞人的小货车由一名男司机驾驶，当时时速或高达80公里。
英国伦敦恐袭事件现场
目前，警方已经封锁了现场，伦敦桥也关闭。英国铁路部门发布预警：伦敦桥附近数个火车站铁路交通受到影响，这些车站包括滑铁卢西站、查令十字车站、伦敦桥车站等。英国警方已将事件定性为恐怖袭击。继伦敦桥汽车撞人事件之后，附近的博罗市场以及沃克斯豪尔地区也相继报告了伤人事件。
英国伦敦恐袭事件现场
目前，警方正在调查这一“安全事件”。据环球网引述外媒报道，目击者表示，事发现场还发生持刀捅人事件，有人受伤。亦有目击者表示，看到三个人从货车上走下，拿着12英寸长的刀子袭击行人，至少3人被刺伤。
英国伦敦恐袭事件现场
英国伦敦恐袭事件现场
撞人事件发生地点位于伦敦桥，而非伦敦塔桥
据央视驻英国记者田晓春报道：伦敦恐怖袭击已造成2人死亡，20人受伤。BBC网站消息，警员称有两名袭击者据信已被击毙。""".encode('utf-8')
content2 = u"""
    　2017年5月20日，中国科学院计算技术研究所第十三届公众科学日活动在计算所举行，社会公众共计约3000余人参加了此次丰富多彩的科普活动。此次公众科学日的主题为“探索塑造未来”，主要是向社会全面展示中国科学院“面向世界科技前沿，面向国家重大需求，面向国民经济主战场”的科技创新成果，对公众进行科普宣传。


展区一角

　　为了让公众更好了解信息技术相关领域科技知识，计算所精心策划了一系列互动科普活动，包括“解密开宝箱”、“科学探索印章之旅”、“网络攻防现场演示”、“编程竟如此简单”、“超级计算机管理模拟体验”、参观“计算的脚步”展厅、科学体验互动活动等30余项丰富多彩的互动科普项目。生动、形象地向公众展示应用信息技术的魅力，激发青少年对信息技术的兴趣和热爱，通过寓教于乐的科普形式，让青少年们在游戏中学到知识、引起兴趣、培养科学精神。

　　说起编程，不少人的第一反应就是两个字：枯燥。针对这点，中科院计算所的科研人员们开发了一个有趣的应用，专门为小朋友量身定制的，采用图形化的编程界面，小朋友们很快就明白了编程的方法，编写出了一个个小程序，控制这小车在场地里跑来跑去。


小朋友编程控制工程车模型

　　新型“蠕虫”病毒WannaCry全球范围内爆发，让全世界的人们在计算机病毒的嚣张面前结结实实地“蓝瘦、香菇”了一把。WannaCry到底是何方神圣，网络攻防现场演示活动中为大家进行了解答。计算所还为公众请来了包括国内网络安全界被尊称为“TK教主”的“tombkeeper”等大咖，为公众演示了包括：扫描条码如何导致系统被入侵；发射携带攻击信息的激光束如何做到让条码阅读器在系统上执行任意命令；如何在移动端窃取通讯录、短信内容等隐私信息。这一系列网络攻防的现场演示让公众大开眼界。


“TK教主”带领观众体验网络入侵


从沙子到芯片 互动展区


观众参观


观众体验互动展示


小朋友成功解密打开宝箱

　　有妈妈在带孩子参加完计算所的公众科学日活动后，在朋友圈里分享了感受，她写到“第一次参加公众开放日活动，这里简直是孩子们的游乐场！带上一本通关护照，根据线索打开一个一个的密码箱，最终通关大奖也在密码箱里！小朋友看到了第一台103计算机模型，体验了虚拟现实，还开动脑筋翻译了摩尔斯码，当然最开心的还是穿梭于各层寻找密码箱！必须一提的是，小朋友第一次站在数据机房里，没有感叹眼前不断闪烁的指示灯，没有抱怨轰隆隆的噪声，而是惊讶的问了一句：‘妈妈，这是什么味道呀！’。原来这是我们家小猴子对数据机房的第一印象是高精尖的计算技术。以直观有趣的方式为孩子们启蒙和科普，这是计算所开放日最赞的地方！”
    """.encode('utf-8')
content3 = u"""
    据说一些大爷大妈已经是这个星球上最具战斗力的群体了。他们前一秒钟还在菜市场上跟小贩斗智斗勇，后一秒钟就能冲到股市里横扫大盘；刚在公交上被小年轻们让完座，转眼到了广场上就生龙活虎了。开启哪种模式，他们自己说了算。

这两天，一则“广场舞老人PK篮球小伙”的视频又印证了这一点。视频显示，一个赤裸上身的年轻小伙子与十几位中年大叔大妈发生了激烈冲突，小伙子被大叔大妈们围堵在一片围墙前进行殴打，被打几秒后小伙子开始还击，现场冲突激烈。

冲突因争夺篮球场地而起。跳广场舞的大爷大妈占领了篮球场的场地，打篮球的小伙子们要求一人一半场地，但从后面的冲突来看，这个要求显然没被大爷大妈接受。在争执中，冲突升级了。

这件事，再次引起人们“坏人变老了还是老人变坏了”的讨论，总之，舆论的倾向性很明显：是这些老人有错在先。

为什么这么说？第一，篮球场是用来打篮球的，不是用来跳广场舞的，或者说，篮球场的首要功能是用来打篮球，当没有人打篮球时，才可以用于其他活动。但这次，当有人来打篮球，大爷大妈并没有让出场地，反而起了冲突。

第二，争执中，是大爷大妈先动手打了人，并且至少是五六个人一起将拳头挥向了被逼在墙边的年轻人。年轻人无奈之下反击。

如此，是非对错就很明显了：这不过就是一个一群广场舞大爷大妈欺负篮球少年、篮球少年反击失败的故事。

于是，在基本的是非判断之外，夹杂着对广场舞扰民的愤怒，广大“吃瓜群众”走到了同一战线，纷纷给篮球小伙们讨要说法。各种关于老年人失德、广场舞大爷大妈的段子重新被扒出来，广场舞大爷大妈再次成为群嘲对象。

有一张合成的图片流传甚广：十年前，大爷大妈们跟小孩争抢公交，十年后，当年的孩子长大，大爷大妈们又来跟他们争抢篮球场。一张图片，将两代人的变与不变展示得一目了然，表达得意思也再明了不过：

孩子们都长大打篮球了，这些不讲道理的老年人依旧还活在强梁的想象中。

不过，你大妈虽然还是你大妈，但那些孩子却也不再只是望着他们的背影无能为力。面对占领篮球场的老年人，他们也可以据理力争。

有人说，大爷大妈跳广场舞，是因为他们是孤独的，广场舞是他们的社交。“他跳得越快，孤独就越追不上他”。但孤独之上，还有公德与良序在。你不能因为自己的孤独，就打扰了别人的清净。你之蜜糖，他人之砒霜。如果只顾自己的热闹与狂欢，不管别人受不受得了，这跟耍流氓又有什么区别？

有个词儿叫年高德劭，但也有人说“老而不死是为贼”，所以，有没有德行，要看个人。阿米尔?汗说得也不错，要不要尊重老人，不是要看年龄，而是要看具体的行为。一群霸占篮球场又打人的大爷大妈，年龄再大，又怎么能赢得别人的尊重呢？

一代人有一代人之需求，有时候因为公共空间的不足，不同群体的需求确实会产生冲突。这需要公共治理者出谋划策，但一个人、一个群体在满足自身需求的时候，至少不能侵占他人的权益。在人群多的地方跳广场舞本身就有“你若安好，那还得了”的嫌疑，何况这群大爷大妈们又占领了本用作他途的篮球场。再理直气壮地打人，真的挺不体面的。

据说，在警方介入后，事情非但没有缓和，到篮球场跳舞的反而更多了。大爷大妈们这一股“我不跳算我输”的精神，还真是霸气侧漏得厉害。

刊  沸腾
    """.encode('utf-8')
content4 = u"""
    　　许久不见博客君，甚是想念吧！

　　话说，几个月来博客君和小伙伴们一直在默默憋大招。终于！全新改版的新浪博客APP已在5月31日正式上线啦！

　　这一次，我们要搞点大事情！

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　莫非是——界面更新、体验优化、bug修复……NONONO！！！这些常规升级博客君就不磨叽了。今天，我主要为各位博主大大们隆重介绍新浪博客全新功能——主题功能！！！

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　新浪博客APP将通过主题功能，帮大家发现优质内容、聚合相同兴趣主旨的文章。敲重点，博客将启动最强大脑，猜各位的兴趣喜好，帮你邂逅更多美妙而有趣的文章！这是博客君充满智商和诚意的尝试，想想就有点小激动呢！

　　光看上面的描述，可能你会闻到一丝忽悠的味道——这就是你们搞的大事情？get不到你的点诶！

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　莫急，待我一一为你拆解。

　　首先，你为什么会需要一个主题功能？

　　有的人觉得编辑推荐的内容根本不符合自己的口味；有的人只想看娱乐八卦，却不得不忍受首页大而全的推荐；有的人认为一篇一篇收藏文章已经满足不了自己“天下好文，尽收囊中”的欲望；有的人则偏好发现各种冷门小众文章，展现在大家面前。每个人的诉求都不尽相同，但有一点可以确定的是，我们希望在这里看到自己感兴趣的文章，并乐于去发现它们。而新浪博客APP的主题功能，正好可以满足大家这一愿望。

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　以上，博客君安利完毕。聪明的你不禁要问，如此利国利民的主题功能该如何购买……咳！该如何使用呢？
搞事情|主题功能重磅上线，新浪博客还能这么玩
　　来来来，敲黑板划重点啦！

　　第一步，下载最新版的新浪博客APP并打开它。

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　登录之后切换至“我”界面，点击“我的主题”。进入后你会发现你的列表空空如也（请忽略博客君的列表，说多了都是泪……），那么果断右上角，选择新建。

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　仅仅只用填写主题名称、主题描述、上传主题头像，设置好主题的投稿及审核权限，再点击“完成”，一个崭新的主题就诞生了。最下方的选填项不是强制的，看各位博主大大们的心情啦！（我才不会告诉你选择了关联栏目，你的主题更容易被看到呢）

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　对了，每个用户最多可以创建5个主题，并最多成为20个主题的管理员，记住哦！

　　创建主题后怎样才能开始向主题里填充内容呢？如果开启了“主题接受投稿”选项，你会在“消息”界面发现需要处理的投稿请求，只需选择接受或拒绝，就能轻松地将文章收入你的主题。

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　除此之外，当你在阅读一篇文章时，如果想将它收入你所创建的主题，也可以直接在文章页面的右上角选择“收入主题”。

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　PS，同一篇文章最多能被5个主题收录哦！

　　讲完创建主题，聪明的你又要问了，如何发现并持续关注感兴趣的主题呢？在新浪博客APP的“发现”界面，你会看到“热门主题”版块，这里会随机展示近期最热门、最受欢迎的主题。

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　如果你还不满足于此，也可以点击查看更多，我们已经为各位博主大大们提供了详细的分类主题列表。总有一款主题适合你的口味！

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　当你对一个主题感兴趣，并希望长期关注它时，也可以在主题页面直接关注。之后你就可以在“关注”界面实时看到主题的更新啦！

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　到此，新浪博客APP的主题功能就介绍完毕了。有木有狠心动呢？赶紧麻溜儿地扫描下方二维码，去下载全新的新浪博客APP吧！

搞事情|主题功能重磅上线，新浪博客还能这么玩

　　最后，如果你在使用新浪博客APP的过程中遇到任何问题或是有任何不爽，欢迎加入我们的新浪博客APP交流QQ群，群号：517353813。博客君和一众产品汪、运营喵已经在群里准备好接锅了！（手动滑稽）
    """.encode('utf-8')


tt = TextTeaser()
start= time.time()
print tt.summarize('1', content1)[0].decode('utf-8'),time.time() - start


tt = TextTeaser()
start= time.time()
print tt.summarize('2', content2)[0].decode('utf-8'),time.time() - start

tt = TextTeaser()
start= time.time()
print tt.summarize('3', content3)[0].decode('utf-8'),time.time() - start

tt = TextTeaser()
start= time.time()
print tt.summarize('4', content4)[0].decode('utf-8'),time.time() - start