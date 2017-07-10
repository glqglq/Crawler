#-*- encoding:utf-8 -*-

import re, pdb, sys, math,time
from collections import defaultdict


class Graph:
	def __init__(self):
		self.Vertices = []
		self.Edges = []

	def getRankedVertices(self):
		res = defaultdict(float)
		for e in self.Edges:
			res[e.Vertex1] += e.Weight
		return sorted(res.items(), key=lambda x: x[1], reverse=True)

class Vertex:
	def __init__(self):
		self.Sentence = None

class Edge:
	def __init__(self):
		self.Vertex1 = None
		self.Vertex2 = None
		self.Weight = 0

class WordType:
	Content=0
	Function=1
	ContentPunctuation=2
	FunctionPunctuation=3

class Word:
	def __init__(self):
		self.Text=''
		self.Type=''

class Sentence:
	def __init__(self):
		self.Words = []

	def getFullSentence(self):
		text = ''
		for w in self.Words:
			text += w.Text
		return text.strip()

	def getReducedSentence(self):
		sentenceText = ''
		sentenceEnd = self.Words[len(self.Words)-1]
		contentWords = filter(lambda w: w.Type == WordType.Content, self.Words)
		i = 0
		while i < len(contentWords):
			w = contentWords[i]
			# upper case the first character of the sentence
			if i == 0:
				li = list(w.Text)
				li[0] = li[0].upper()
				w.Text = ''.join(li)
			sentenceText += w.Text
			if i < len(contentWords)-1:
				sentenceText += ' '
			elif sentenceEnd.Text != w.Text:
				sentenceText += sentenceEnd.Text
			i = i+1
		return sentenceText
			

class Paragraph:
	def __init__(self):
		self.Sentences = []

class Reduction:
	functionPunctuation = ' ,-'
	contentPunctuation = '.?!\n'
	punctuationCharacters = functionPunctuation+contentPunctuation
	sentenceEndCharacters = '.?!'
	
	def isContentPunctuation(self, text):
		for c in self.contentPunctuation:
			if text.lower() == c.lower():
				return True
		return False

	def isFunctionPunctuation(self, text):
		for c in self.functionPunctuation:
			if text.lower() == c.lower():
				return True
		return False

	def isFunction(self, text, stopWords):
		for w in stopWords:
			if text.lower() == w.lower():
				return True
		return False

	def tag(self, sampleWords, stopWords):
		taggedWords = []
		for w in sampleWords:
			tw = Word()
			tw.Text = w
			if self.isContentPunctuation(w):
				tw.Type = WordType.ContentPunctuation
			elif self.isFunctionPunctuation(w):
				tw.Type = WordType.FunctionPunctuation
			elif self.isFunction(w, stopWords):
				tw.Type = WordType.Function
			else:
				tw.Type = WordType.Content
			taggedWords.append(tw)
		return taggedWords

	def tokenize(self, text):
		return filter(lambda w: w != '', re.split('([{0}])'.format(self.punctuationCharacters), text))	

	def getWords(self, sentenceText, stopWords):
		return self.tag(self.tokenize(sentenceText), stopWords) 

	def getSentences(self, line, stopWords):
		sentences = []
		sentenceTexts = filter(lambda w: w.strip() != '', re.split('[{0}]'.format(self.sentenceEndCharacters), line))	
		sentenceEnds = re.findall('[{0}]'.format(self.sentenceEndCharacters), line)
		sentenceEnds.reverse()
		for t in sentenceTexts:
			if len(sentenceEnds) > 0:
				t += sentenceEnds.pop()
			sentence = Sentence()
			sentence.Words = self.getWords(t, stopWords)
			sentences.append(sentence)
		return sentences

	def getParagraphs(self, lines, stopWords):
		paragraphs = []
		for line in lines:
			paragraph = Paragraph()
			paragraph.Sentences = self.getSentences(line, stopWords)
			paragraphs.append(paragraph)
		return paragraphs

	def findWeight(self, sentence1, sentence2):
		length1 = len(filter(lambda w: w.Type == WordType.Content, sentence1.Words))
		length2 = len(filter(lambda w: w.Type == WordType.Content, sentence2.Words))
		if length1 < 4 or length2 < 4:
			return 0
		weight = 0
		for w1 in filter(lambda w: w.Type == WordType.Content, sentence1.Words):
			for w2 in filter(lambda w: w.Type == WordType.Content, sentence2.Words):
				if w1.Text.lower() == w2.Text.lower():
					weight = weight + 1
		normalised1 = 0
		if length1 > 0:
			normalised1 = math.log(length1)
		normalised2 = 0
		if length2 > 0:
			normalised2 = math.log(length2)
		norm = normalised1 + normalised2
		if norm == 0:
			return 0
		return weight / float(norm)

	def buildGraph(self, sentences):
		g = Graph()
		for s in sentences:
			v = Vertex()
			v.Sentence = s
			g.Vertices.append(v)
		for i in g.Vertices:
			for j in g.Vertices:
				if i != j:
					w = self.findWeight(i.Sentence, j.Sentence)
					e = Edge()
					e.Vertex1 = i
					e.Vertex2 = j
					e.Weight = w
					g.Edges.append(e)
		return g

	def sentenceRank(self, paragraphs):
		sentences = []
		for p in paragraphs:
			for s in p.Sentences:
				sentences.append(s)
		g = self.buildGraph(sentences)
		return g.getRankedVertices()

	def reduce(self, text, reductionRatio):
		stopWordsFile = 'stopWords.txt'
		stopWords= open(stopWordsFile).read().splitlines()

		lines = text.splitlines()
		contentLines = filter(lambda w: w.strip() != '', lines)

		paragraphs = self.getParagraphs(contentLines, stopWords)

		rankedSentences = self.sentenceRank(paragraphs)

		orderedSentences = []
		for p in paragraphs:
			for s in p.Sentences:
				orderedSentences.append(s)

		reducedSentences = []
		i = 0
		while i < math.trunc(len(rankedSentences) * reductionRatio):
			s = rankedSentences[i][0].Sentence
			position = orderedSentences.index(s)
			reducedSentences.append((s, position))
			i = i + 1
		reducedSentences = sorted(reducedSentences, key=lambda x: x[1])
		
		reducedText = []
		for s,r in reducedSentences:
			reducedText.append(s.getFullSentence())
		return reducedText	

# 
reduction = Reduction()
content9 = """
<html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>中国科学院计算技术研究所</title>
<link href="./images/cn53css.css" rel="stylesheet" type="text/css">



</head>
<body onload="init()">
<table width="1000" border="0" align="center" cellpadding="0" cellspacing="0">
  <tbody><tr valign="top">
    <td width="15" background="./images/cn53l02.gif"><img src="./images/cn53l01.jpg"></td>
    <td width="970">
    
<script language="javascript" src="http://www.ict.cas.cn/images/one.js"></script>
<script language="javascript" src="http://www.ict.cas.cn/images/two.js"></script>
<style>
.mtDropdownMenu {
	LEFT: -1000px; OVERFLOW: hidden; POSITION: absolute; TOP: -1000px
}
.mtDropdownMenu .content {
	POSITION: relative
}
.mtDropdownMenu .items {
	BORDER-RIGHT: #676767 1px solid; BORDER-TOP: #676767 1px solid; Z-INDEX: 2; LEFT: 0px; BORDER-LEFT: #676767 1px solid; BORDER-BOTTOM: #676767 1px solid; POSITION: relative; TOP: 0px
}
.mtDropdownMenu .item {background-color:#E2F4ED;
	BORDER-RIGHT: medium none; BORDER-TOP: medium none; FONT-SIZE: 12px; BORDER-LEFT: medium none; CURSOR: hand; COLOR: #676767; BORDER-BOTTOM: medium none; FONT-FAMILY: "Verdana", "Arial", "Helvetica", "sans-serif"; TEXT-DECORATION: none; EXT-DECORATION: none
}
.mtDropdownMenu .background { 
	  Z-INDEX: 1; FILTER: alpha(opacity=75); LEFT: 0px; POSITION: absolute; TOP: 0px; moz-opacity: .8 
}
.mtDropdownMenu .shadowRight {
	Z-INDEX: 3; FILTER: alpha(opacity=40); WIDTH: 2px; POSITION: absolute; TOP: 3px; moz-opacity: .4
}
.mtDropdownMenu .shadowBottom {

	Z-INDEX: 1; FILTER: alpha(opacity=40); LEFT: 3px; POSITION: absolute; HEIGHT: 2px; moz-opacity: .4
}
.mtDropdownMenu .hover {
	BACKGROUND:#68A8D7; COLOR: #ffffff
}
.mtDropdownMenu .item IMG {
	MARGIN-LEFT: 10px
}
</style>
<script type="text/javascript">
function escapeTrs(str){//转义trs关键字
	var arr = new Array("\\\\","!","@","#","\\$","\%","\\^","\&","\\*","\\(","\\)","\\_","\\+","\-","\=","\\{","\\}","\\|","\\[","\\]",";","'",":","\"","\<","\>","\\?","\,","\\.","\/");
	
	for(var i=0;i<arr.length;i++){
	 var re = new RegExp(arr[i],"img");
	 str = str.replace(re, '\\' + arr[i]);
	}
	
	return str;
}
function dealKeywords(sword, relation)
{	
	var sTemp = "";
	var swordtemp = ""; 
	var sArray;

	if(sword.indexOf("*")<0&&sword.indexOf("+")<0&&sword.indexOf(")")<0&&sword.indexOf("(")<0&&sword.indexOf("\\")<0)
	{
		sword = escapeTrs(sword);
		//不含trs关键字
		sArray = sword.split(" ");//输入框空格处理,空格表示 relation 关系
		for(var i=0; i<sArray.length;i++)
		{	
			sTemp = sArray[i].replace(/^\s+|\s+$/g,"");//去掉sword前后空格
			if(sTemp!="")
			{
				swordtemp += "'"+ sTemp + "' "+relation+" ";/*加上''符号,处理trs带运算符的检索词报错的问题*/
			}					
		}
		if(swordtemp.lastIndexOf(" "+relation+" ")!=-1)//去掉relation结尾
		{
			swordtemp = swordtemp.substring(0,swordtemp.length-relation.length-2);
		} 
	}
	
	else//包含trs关键字
	{    
		 if(sword.indexOf("\\")!=-1){
		 	var re = new RegExp("\\\\","img");
	 		sword = sword.replace(re, '\\\\');
		 }
		 swordtemp = "'"+sword+"'";
	}
	return swordtemp;	
} 

function search_check() {
	var sword =document.getElementById("iptSword").value.replace(/^\s+|\s+$/g,"");
	
	if (sword=='' || sword=='请输入关键字') {
		alert('请输入关键字!');
		return false;
	} else {	
		document.searchform.searchword.value = dealKeywords(sword, "and");
		document.searchform.preKeyword.value=encodeURI(document.getElementById("iptSword").value);
		document.searchform.submit();
	}
}
</script>
<table align="center" width="970" border="0" cellpadding="0" cellspacing="0" background="http://www.ict.cas.cn/images/cnptop_bj.gif">
      <tbody><tr>
        <td width="361" align="left"><img src="http://www.ict.cas.cn/images/cnplogo.jpg" width="361" height="60"></td>
		<td width="301" align="right"><table width="45%" border="0" cellspacing="0" cellpadding="0" style="margin-top:3px;">
      <form name="searchform" action="http://search.cas.cn/search" method="post" target="_top" onsubmit="search_check()"></form>
        <input type="hidden" name="channelid" value="11518">
        <input type="hidden" name="option" value="ideosingle">
        <input type="hidden" name="searchword" id="searchword" value="">
		<input type="hidden" name="preKeyword" value="">
        <tbody><tr>
          <td width="27%" align="center" class="white"><input name="iptSword" id="iptSword" type="text" onclick="javascript:if(this.value=='请输入关键字') this.value=''" value="请输入关键字" border="0" size="15" style="filter:Alpha(Opacity=45);"></td>
          <td width="10%" class="white01"><input type="image" src="http://www.ict.cas.cn/images/cnc7_search.jpg" style="width:43; height:20px;"></td>
        </tr>
      
    </tbody></table></td>
        <td width="308" align="right" style="padding:0px 15px 0px 0px"><a href="http://webmail.ict.ac.cn/" class="cn51gghui" target="_top">邮箱登录</a>  <span class="cn51gghui">|</span> <a target="_top" href="http://poa.ict.ac.cn/" class="cn51gghui">所务办公</a> <span class="cn51gghui">|</span> <a target="_top" href="javascript:window.external.AddFavorite('http://www.ict.cas.cn/','中国科学院计算技术研究所')" class="cn51gghui">收藏本站</a> <span class="cn51gghui">|</span> <a target="_top" href="http://english.ict.cas.cn/" class="cn51gghui">English</a> <span class="cn51gghui">|</span> <a target="_top" href="http://www.cas.cn/" class="cn51gghui">中国科学院</a></td>
      </tr>
    </tbody></table>
	<table align="center" width="970" border="0" cellspacing="0" cellpadding="0">
        <tbody><tr>
          <td height="156" align="right" valign="top" background="http://www.ict.cas.cn/images/cn53img0.jpg">&nbsp;</td>
        </tr>
      </tbody></table>
      <table width="970" border="0" align="center" cellpadding="0" cellspacing="0">
        <tbody><tr>
          <td height="38" background="http://www.ict.cas.cn/images/cn53top04.gif"><table border="0" align="center" cellpadding="0" cellspacing="0">
              <tbody><tr>
                
                <td><a target="_top" href="http://www.ict.cas.cn/" class="cn51toppd">首页</a></td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
                <td>
              <a id="menu1" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/jssgk/">计算所概况</a> </td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
                <td>
              <a id="menu2" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/xwzx/">新闻动态</a> </td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
                <td>
              <a id="menu3" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/kycg/">科研成果</a> </td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
                <td>
              <a id="menu4" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/rcjy/">研究队伍</a> </td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
                <td>
              <a id="menu5" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/gjjl/">国际交流</a> </td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
                <td>
              <a id="menu6" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/jszy/">技术转移</a> </td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
                <td>
              <a id="menu7" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/yjsjy/">研究生教育</a> </td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
                <td>
              <a id="menu8" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/xscbw/">学术出版物</a> </td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
                <td>
              <a id="menu9" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/dj/">党群园地</a> </td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
                <td>
              <a id="menu10" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/kxcb/">科学传播</a> </td>
                <td>
              <a id="menu11" class="en55topwhite12bpd cn51toppd" target="_top" href="http://www.ict.cas.cn/xxgk/">信息公开</a> </td>
                <td width="2"><img src="http://www.ict.cas.cn/images/cn53top06.gif"></td>
              </tr>
            </tbody></table></td>
        </tr>
      </tbody></table>
	  <script language="JavaScript">
var ms = new mtDropDownSet(mtDropDown.direction.down,4, 1, mtDropDown.reference.bottomLeft);
<!-- menu1 -->
var menu1 = ms.addMenu(document.getElementById('menu1'));

menu1.addItem('计算所简介', 'http://www.ict.cas.cn/jssgk/jssjj/');

menu1.addItem('所长致辞', 'http://www.ict.cas.cn/jssgk/szzc/');

menu1.addItem('现任所领导', 'http://www.ict.cas.cn/jssgk/xrld/');

menu1.addItem('历任领导', 'http://www.ict.cas.cn/jssgk/lrld/');

menu1.addItem('学术委员会', 'http://www.ict.cas.cn/jssgk/xswyh/');

menu1.addItem('计算所定位', 'http://www.ict.cas.cn/jssgk/jssdw/');

menu1.addItem('院士专家', 'http://www.ict.cas.cn/rcjy/yszj/');

menu1.addItem('组织机构', 'http://www.ict.cas.cn/jgsz/');

menu1.addItem('历史沿革', 'http://www.ict.cas.cn/jssgk/lsyg/');

menu1.addItem('院所风貌', 'http://www.ict.cas.cn/jssgk/ysfm/');

<!-- menu2 -->
var menu2 = ms.addMenu(document.getElementById('menu2'));

menu2.addItem('计算所新闻', 'http://www.ict.cas.cn/xwzx/jssxw/');

menu2.addItem('媒体文摘', 'http://www.ict.cas.cn/xwzx/mtwz/');

<!-- menu3 -->
var menu3 = ms.addMenu(document.getElementById('menu3'));

menu3.addItem('科研概况', 'http://www.ict.cas.cn/kycg/kygk/');

menu3.addItem('科技奖励', 'http://www.ict.cas.cn/kycg/kjjl/');

menu3.addItem('成果年报', 'http://www.ict.cas.cn/kycg/cgnb/');

<!-- menu4 -->
var menu4 = ms.addMenu(document.getElementById('menu4'));

menu4.addItem('院士专家', 'http://www.ict.cas.cn/rcjy/yszj/');

menu4.addItem('杰出青年', 'http://www.ict.cas.cn/rcjy/jcqn/');

menu4.addItem('研究员', 'http://www.ict.cas.cn/rcjy/zgjgwry/');

menu4.addItem('副研究员', 'http://www.ict.cas.cn/rcjy/fgjgwry/');

menu4.addItem('人才招聘', 'http://www.ict.cas.cn/rcjy/rczp/');

menu4.addItem('百人计划', 'http://www.ict.cas.cn/rcjy/brjh/');

<!-- menu5 -->
var menu5 = ms.addMenu(document.getElementById('menu5'));

menu5.addItem('学术活动', 'http://www.ict.cas.cn/gjjl/xshd/');

menu5.addItem('交流动态', 'http://www.ict.cas.cn/gjjl/jldt/');

menu5.addItem('学术交流', 'http://www.ict.cas.cn/gjjl/xsjl/');

<!-- menu6 -->
var menu6 = ms.addMenu(document.getElementById('menu6'));

menu6.addItem('共性技术辐射（分所）', 'http://www.ict.cas.cn/jszy/gxjsfs/');

menu6.addItem('技术转让与孵化（NPO）', 'http://www.ict.cas.cn/jszy/fhjs/');

menu6.addItem('企业孵化（算源）', 'http://www.ict.cas.cn/jszy/qyfh/');

<!-- menu7 -->
var menu7 = ms.addMenu(document.getElementById('menu7'));

menu7.addItem('概况', 'http://www.ict.cas.cn/yjsjy/gk/');

menu7.addItem('招生信息', 'http://www.ict.cas.cn/yjsjy/zs/');

menu7.addItem('导师介绍', 'http://www.ict.cas.cn/yjsjy/dsjj/');

menu7.addItem('学生工作', 'http://www.ict.cas.cn/yjsjy/xsgz/');

menu7.addItem('教学与培养', 'http://www.ict.cas.cn/yjsjy/jxypy/');

menu7.addItem('学位管理', 'http://www.ict.cas.cn/yjsjy/xwgl/');

menu7.addItem('就业指导', 'http://www.ict.cas.cn/yjsjy/jyzd/');

menu7.addItem('博士后流动站', 'http://www.ict.cas.cn/yjsjy/bshldz/');

menu7.addItem('同学会', 'http://www.ict.cas.cn/yjsjy/txh/');

menu7.addItem('继续教育', 'http://www.ict.cas.cn/yjsjy/jxjy/');

<!-- menu8 -->
var menu8 = ms.addMenu(document.getElementById('menu8'));

menu8.addItem('学术期刊', 'http://www.ict.cas.cn/xscbw/xsqk/');

<!-- menu9 -->
var menu9 = ms.addMenu(document.getElementById('menu9'));

menu9.addItem('党委', 'http://www.ict.cas.cn/dj/dw/');

menu9.addItem('工作动态', 'http://www.ict.cas.cn/dj/gzdt/');

menu9.addItem('工青妇之窗', 'http://www.ict.cas.cn/dj/gqfzc/');

menu9.addItem('《创新·求实》', 'http://www.ict.cas.cn/dj/cxqs/');

<!-- menu10 -->
var menu10 = ms.addMenu(document.getElementById('menu10'));

menu10.addItem('热点与应用', 'http://www.ict.cas.cn/kxcb/kxr/');

menu10.addItem('硬件的故事', 'http://www.ict.cas.cn/kxcb/yjdgs/');

menu10.addItem('网络的故事', 'http://www.ict.cas.cn/kxcb/wldgs/');

menu10.addItem('计算机发展史', 'http://www.ict.cas.cn/kxcb/jsjfzs/');

menu10.addItem('科学专题', 'http://www.ict.cas.cn/kxcb/kxzt/');

menu10.addItem('视频动画', 'http://www.ict.cas.cn/kxcb/spdh/');


<!-- menu11 -->
var menu11 = ms.addMenu(document.getElementById('menu11'));

menu11.addItem('相关规定', 'http://www.ict.cas.cn/xxgk/xxbs/');

menu11.addItem('组织机构', 'http://www.ict.cas.cn/xxgk/zzjg/');

menu11.addItem('信息公开年报', 'http://www.ict.cas.cn/xxgk/xxgknb/');

mtDropDown.renderAll();		
</script><div id="mtDropDown0" class="mtDropdownMenu top" style="width: 75px; height: 268px; visibility: hidden;"><div class="content" style="width: 73px; height: 266px; top: -268px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">计算所简介</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">所长致辞</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">现任所领导</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">历任领导</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">学术委员会</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">计算所定位</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">院士专家</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">组织机构</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">历史沿革</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">院所风貌</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 264px; width: 68px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 71px; height: 263px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 71px; height: 264px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div><div id="mtDropDown1" class="mtDropdownMenu top" style="width: 75px; height: 60px; visibility: hidden;"><div class="content" style="width: 73px; height: 58px; top: -60px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">计算所新闻</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">媒体文摘</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 56px; width: 68px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 71px; height: 55px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 71px; height: 56px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div><div id="mtDropDown2" class="mtDropdownMenu top" style="width: 63px; height: 86px; visibility: hidden;"><div class="content" style="width: 61px; height: 84px; top: -86px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">科研概况</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">科技奖励</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">成果年报</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 82px; width: 56px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 59px; height: 81px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 59px; height: 82px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div><div id="mtDropDown3" class="mtDropdownMenu top" style="width: 63px; height: 164px; visibility: hidden;"><div class="content" style="width: 61px; height: 162px; top: -164px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">院士专家</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">杰出青年</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">研究员</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">副研究员</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">人才招聘</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">百人计划</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 160px; width: 56px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 59px; height: 159px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 59px; height: 160px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div><div id="mtDropDown4" class="mtDropdownMenu top" style="width: 63px; height: 86px; visibility: hidden;"><div class="content" style="width: 61px; height: 84px; top: -86px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">学术活动</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">交流动态</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">学术交流</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 82px; width: 56px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 59px; height: 81px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 59px; height: 82px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div><div id="mtDropDown5" class="mtDropdownMenu top" style="width: 148px; height: 86px; visibility: hidden;"><div class="content" style="width: 146px; height: 84px; top: -86px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">共性技术辐射（分所）</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">技术转让与孵化（NPO）</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">企业孵化（算源）</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 82px; width: 141px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 144px; height: 81px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 144px; height: 82px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div><div id="mtDropDown6" class="mtDropdownMenu top" style="width: 87px; height: 268px; visibility: hidden;"><div class="content" style="width: 85px; height: 266px; top: -268px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">概况</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">招生信息</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">导师介绍</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">学生工作</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">教学与培养</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">学位管理</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">就业指导</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">博士后流动站</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">同学会</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">继续教育</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 264px; width: 80px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 83px; height: 263px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 83px; height: 264px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div><div id="mtDropDown7" class="mtDropdownMenu top" style="width: 63px; height: 34px; visibility: hidden;"><div class="content" style="width: 61px; height: 32px; top: -34px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">学术期刊</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 30px; width: 56px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 59px; height: 29px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 59px; height: 30px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div><div id="mtDropDown8" class="mtDropdownMenu top" style="width: 91px; height: 112px; visibility: hidden;"><div class="content" style="width: 89px; height: 110px; top: -112px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">党委</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">工作动态</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">工青妇之窗</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">《创新·求实》</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 108px; width: 84px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 87px; height: 107px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 87px; height: 108px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div><div id="mtDropDown9" class="mtDropdownMenu top" style="width: 87px; height: 164px; visibility: hidden;"><div class="content" style="width: 85px; height: 162px; top: -164px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">热点与应用</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">硬件的故事</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">网络的故事</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">计算机发展史</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">科学专题</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">视频动画</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 160px; width: 80px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 83px; height: 159px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 83px; height: 160px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div><div id="mtDropDown10" class="mtDropdownMenu top" style="width: 87px; height: 86px; visibility: hidden;"><div class="content" style="width: 85px; height: 84px; top: -86px;"><table class="items" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td colspan="2"><img src="" width="1" height="1"></td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">相关规定</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">组织机构</td></tr><tr class="item"><td nowrap="" style="padding:4px; padding-left:5px;">信息公开年报</td></tr><tr><td colspan="2"><img src="" width="1" height="1"></td></tr></tbody></table><div class="shadowBottom" style="top: 82px; width: 80px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="shadowRight" style="left: 83px; height: 81px; background-color: rgb(136, 136, 136);"><img src="" width="1" height="1"></div><div class="background" style="width: 83px; height: 82px; background-color: rgb(255, 255, 255);"><img src="" width="1" height="1"></div></div></div>
      <table width="970" border="0" cellspacing="0" cellpadding="0">
        <tbody><tr valign="top">
          <td width="235" bgcolor="#E3E7EB"><table width="235" border="0" cellspacing="0" cellpadding="0">
              <tbody><tr>
                <td height="36" background="./images/cnpl01_bj.gif"><table width="235" border="0" cellpadding="0" cellspacing="0" class="cn51white12b">
                    <tbody><tr>
                      <td width="30" align="center"><img src="./images/cn53left02.gif" width="14" height="14"></td>
                      <td width="205">计算所概况</td>
                    </tr>
                  </tbody></table></td>
              </tr>
              <tr>
                <td height="1" bgcolor="#738B98"></td>
              </tr>
              <tr>
                <td height="1" bgcolor="#FFFFFF"></td>
              </tr>
            </tbody></table>
            <table width="235" border="0" cellspacing="0" cellpadding="0">
              <tbody><tr>
                <td><img src="./images/cn53left03.gif" width="235" height="13"></td>
              </tr>
              <tr>
                <td valign="top" background="./images/cn53left04.gif"><table width="225" border="0" align="center" cellpadding="0" cellspacing="0">
                    <tbody><tr>
                      <td class="cn51leftjj" style="padding:0 0 5px 0"><table width="216" border="0" align="center" cellpadding="0" cellspacing="0" class="cn51blue12">
                          <tbody><tr align="left">
                            <td width="36" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="68"><a href="./jssgk/jssjj/" class="cn51blue12">计算所简介</a></td>
                            <td width="36" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="76"><a href="./rcjy/yszj/" class="cn51blue12">院士专家</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
                          <tr align="left">
                            <td height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td><a href="./jssgk/szzc/" class="cn51blue12">所长致辞</a></td>
                            <td align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td><a href="http://www.ict.cas.cn/jgsz/" class="cn51blue12">组织机构</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>

                          </tr>
                          <tr align="left">
                            <td height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td><a href="./jssgk/xrld/" class="cn51blue12">现任所领导</a></td>
                            <td align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td><a href="./jssgk/lrld/" class="cn51blue12">历任领导</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
                          <tr align="left">
                            <td height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td><a href="./jssgk/xswyh/" class="cn51blue12">学术委员会</a></td>
                            <td align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td><a href="./jssgk/jssdw/" class="cn51blue12">计算所定位</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
                          <tr align="left">
                            <td height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td><a href="./jssgk/lsyg/" class="cn51blue12">历史沿革</a></td>
                            <td align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td><a href="./jssgk/ysfm/" class="cn51blue12">院所风貌</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
                        </tbody></table></td>
                    </tr>
                  </tbody></table></td>
              </tr>
              <tr>
                <td><img src="./images/cn53left05.gif" width="235" height="13"></td>
              </tr>
              <tr>
                <td height="1" bgcolor="#E3E7EB"></td>
              </tr>
            </tbody></table>
            <table width="235" border="0" cellspacing="0" cellpadding="0">
              <tbody><tr>
                <td><table width="235" border="0" cellpadding="0" cellspacing="0" background="./images/cnpl02_bj.gif">
                    <tbody><tr>
                      <td width="30" height="28" align="center"><img src="./images/cn53left02.gif" width="14" height="14"></td>
                      <td width="163" class="cn51white12b">科研部门</td>
                    </tr>
                    <tr>
                      <td height="1" colspan="3" bgcolor="#FFFFFF"></td>
                    </tr>
                  </tbody></table></td>
              </tr>
              <tr>
                <td valign="top" style="padding:8px 0 10px 0"><table width="235" border="0" cellspacing="0" cellpadding="0">
              <tbody><tr>
                <td><img src="./images/cn53left03.gif" width="235" height="13"></td>
              </tr>
              <tr>
                <td valign="top" background="./images/cn53left04.gif"><table width="225" border="0" align="center" cellpadding="0" cellspacing="0">
                    <tbody><tr>
                      <td class="cn51leftjj" style="padding:0 0 5px 0"><table width="216" border="0" align="center" cellpadding="0" cellspacing="0" class="cn51blue12">
                          
						  <tbody><tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/xtjgsys/" class="cn51blue12">计算机体系结构国家重点实验室</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/wclqyjzx/" class="cn51blue12">微处理器研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/znclq/" class="cn51blue12">智能处理器研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/gxnjsyjzx/" class="cn51blue12">高性能计算机研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/gtljsj/" class="cn51blue12">高通量计算机研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/xjjsj/" class="cn51blue12">先进计算机系统研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/sjcc/" class="cn51blue12">数据存储技术研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/jcyyzx/" class="cn51blue12">计算机应用研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/wlzdsys/" class="cn51blue12">网络数据科学与技术重点实验室</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/wljsyjzx/" class="cn51blue12">网络技术研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/ydjs/" class="cn51blue12">移动计算与新型终端北京市重点实验室</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/xjwxjslhzx/" class="cn51blue12">无线通信技术研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/zxzx/" class="cn51blue12">专项技术研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/znxnzdsys/" class="cn51blue12">智能信息处理重点实验室</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/fzjsxt/" class="cn51blue12">泛在计算系统研究中心</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
						  <tr align="left">
                            <td width="30" height="28" align="center"><img src="./images/cn53left08.gif" width="11" height="11"></td>
                            <td width="186"><a href="./jgsz/kyxt/qzyjsys/" class="cn51blue12">前瞻研究实验室</a></td>
                          </tr>
                          <tr>
                            <td height="1" colspan="4" background="./images/cn53left07.gif"></td>
                          </tr>
						  
                        </tbody></table></td>
                    </tr>
                  </tbody></table></td>
              </tr>
              <tr>
                <td><img src="./images/cn53left05.gif" width="235" height="13"></td>
              </tr>
              <tr>
                <td height="1" bgcolor="#E3E7EB"></td>
              </tr>
            </tbody></table></td>
              </tr>
            </tbody></table>
            <table width="235" border="0" cellspacing="0" cellpadding="0">
                    <tbody><tr>
                      <td height="1"></td>
                    </tr>
                    <tr>
                      <td height="36" background="./images/cnpl01_bj.gif"><table width="230" border="0" cellspacing="0" cellpadding="0">
                          <tbody><tr>
                            <td width="29" align="center"><img src="./images/cn53right01.gif" width="14" height="14"></td>
                            <td width="158" class="cn51white12b">所属网站</td>
                            <td width="47"><a href="./shye/sswz/"><img src="./images/cn53c05.gif" width="37" height="13" border="0"></a></td>
                          </tr>
                        </tbody></table></td>
                    </tr>
                    <tr>
                      <td height="1" bgcolor="#B6BDB3"></td>
                    </tr>
                  </tbody></table></td>
          <td width="505" bgcolor="#FFFFFF"><table width="480" border="0" align="center" cellpadding="0" cellspacing="0">
              <tbody><tr>
                <td height="160">
				
				<table width="480" border="0" cellspacing="0" cellpadding="0">
                  <tbody><tr>
                    <td height="30" align="center" valign="middle" class="cnphong16c_h"><a href="./xwzx/jssxw/201706/t20170628_4819362.html" class="cnphong16c_h">中科院计算所2017届研究生毕业典礼隆重举行</a></td>
                  </tr>
                </tbody></table>
                <table width="480" border="0" cellspacing="0" cellpadding="0">
                    <tbody><tr>
                      <td width="198" align="left"><table width="184" border="0" cellpadding="1" cellspacing="1" bgcolor="#728895">
                          <tbody><tr>
                            <td align="center" valign="middle" bgcolor="#FFFFFF"><a href="./xwzx/jssxw/201706/t20170628_4819362.html"><img src="./xwzx/jssxw/201706/W020170630542566679210.jpg" width="185" height="125" border="0"></a></td>
                          </tr>
                        </tbody></table></td>
                      <td width="288" valign="top"><table width="280" border="0" cellpadding="0" cellspacing="0" class="cn51hui122">
						  <tbody><tr><td height="10"></td></tr>
						  <tr>
                            <td width="100%">6月24日上午，中科院计算所2017届研究生毕业典礼在计算所一层报告厅隆重举行。今年计算所共有名237名研究生毕业，其中67名博士研究生，170名硕士研究生。所长孙凝晖、所党委书记李锦涛、所学位评定委员会主席陈熙霖、副主席李晓维、所学位评定委员会委员卜东波、陈益强、山世光...<a href="./xwzx/jssxw/201706/t20170628_4819362.html"><img src="./images/cn53c05.gif" width="37" height="13" border="0"></a></td>
                          </tr>
                        </tbody></table>
                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                          <tbody><tr>
                            <td align="right" style="padding:2px 6px 2px 0"><a href="./xwzx/jssxw/">更多&gt;&gt;</a></td>
                          </tr>
                        </tbody></table></td>
                    </tr>
                  </tbody></table>
				  
				  </td>
              </tr>
            </tbody></table>
            <table width="486" border="0" align="center" cellpadding="0" cellspacing="0">
              <tbody><tr>
                <td valign="top"><table width="486" border="0" align="center" cellpadding="0" cellspacing="0" class="cn51black12b">
                    <tbody><tr>
                      <td height="26" background="./images/cn53c03.gif"><table width="486" border="0" cellspacing="0" cellpadding="0">
                          <tbody><tr>
                            <td width="30" align="center"><img src="./images/cn53c04.gif" width="14" height="14"></td>
                            <td width="409" class="cn5lan12b">综合新闻</td>
                            <td width="47"><a href="./xwzx/"><img src="./images/cn53c05.gif" width="37" height="13" border="0"></a></td>
                          </tr>
                        </tbody></table></td>
                    </tr>
                    <tr>
                      <td height="1" bgcolor="#FFFFFF"></td>
                    </tr>
                    <tr>
                      <td height="1" bgcolor="#C8C8C8"></td>
                    </tr>
                  </tbody></table>
                  <table width="486" border="0" align="center" cellpadding="0" cellspacing="0">
                    <tbody><tr>
                      <td valign="top" style="padding:12px 0 18px 0"><table width="468" border="0" align="center" cellpadding="0" cellspacing="0" class="cn51blue123">
                          
						  <tbody><tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347">[<a href="./xwzx/jssxw/" class="cn51blue123">计算所新闻</a>] <a href="./xwzx/jssxw/201706/t20170628_4819362.html" target="_blank" title="中科院计算所2017届研究生毕业典礼隆重举行" class="cn51blue123">中科院计算所2017届研究生毕业典礼隆重举行</a></td>
                            <td width="91">(2017-06-28)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347">[<a href="./xwzx/jssxw/" class="cn51blue123">计算所新闻</a>] <a href="./xwzx/jssxw/201706/t20170622_4816752.html" target="_blank" title="中科院计算所入选全国第二批双创示范基地" class="cn51blue123">中科院计算所入选全国第二批双创示范基地</a></td>
                            <td width="91">(2017-06-22)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347">[<a href="./xwzx/jssxw/" class="cn51blue123">计算所新闻</a>] <a href="./xwzx/jssxw/201706/t20170622_4816751.html" target="_blank" title="苏州市集成电路设计企业市场应用对接交流会成功举办" class="cn51blue123">苏州市集成电路设计企业市场应用对接交流...</a></td>
                            <td width="91">(2017-06-22)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347">[<a href="./xwzx/jssxw/" class="cn51blue123">计算所新闻</a>] <a href="./xwzx/jssxw/201706/t20170619_4815194.html" target="_blank" title="国家重点研发计划“软件定义的云计算基础理论与方法” 项目实施方案论证暨年度进展情况汇报会" class="cn51blue123">国家重点研发计划“软件定义的云计算基础...</a></td>
                            <td width="91">(2017-06-19)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347">[<a href="./xwzx/jssxw/" class="cn51blue123">计算所新闻</a>] <a href="./xwzx/jssxw/201706/t20170614_4812286.html" target="_blank" title="网络数据科学与技术重点实验室开源Easy Machine Learning系统" class="cn51blue123">网络数据科学与技术重点实验室开源Easy Ma...</a></td>
                            <td width="91">(2017-06-14)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347">[<a href="./xwzx/jssxw/" class="cn51blue123">计算所新闻</a>] <a href="./xwzx/jssxw/201706/t20170605_4808009.html" target="_blank" title="计算所济宁分所助力山东省中小微企业创新竞技行动计划" class="cn51blue123">计算所济宁分所助力山东省中小微企业创新...</a></td>
                            <td width="91">(2017-06-05)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347">[<a href="./xwzx/jssxw/" class="cn51blue123">计算所新闻</a>] <a href="./xwzx/jssxw/201705/t20170520_4794655.html" target="_blank" title="中科院计算所第十三届公众科学日活动成功举办" class="cn51blue123">中科院计算所第十三届公众科学日活动成功举办</a></td>
                            <td width="91">(2017-05-20)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347">[<a href="./xwzx/jssxw/" class="cn51blue123">计算所新闻</a>] <a href="./xwzx/jssxw/201705/t20170517_4793298.html" target="_blank" title="大数据分析系统国家工程实验室召开第一届理事会第一次会议" class="cn51blue123">大数据分析系统国家工程实验室召开第一届...</a></td>
                            <td width="91">(2017-05-17)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347">[<a href="./xwzx/jssxw/" class="cn51blue123">计算所新闻</a>] <a href="./xwzx/jssxw/201705/t20170511_4786897.html" target="_blank" title="中科院计算所成立I-Tech创新创业学院" class="cn51blue123">中科院计算所成立I-Tech创新创业学院</a></td>
                            <td width="91">(2017-05-11)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347">[<a href="./xwzx/jssxw/" class="cn51blue123">计算所新闻</a>] <a href="./xwzx/jssxw/201705/t20170510_4786598.html" target="_blank" title="中科院计算所烟台分所成功获批国家级高级研修项目" class="cn51blue123">中科院计算所烟台分所成功获批国家级高级...</a></td>
                            <td width="91">(2017-05-10)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
                      </tbody></table></td>
                    </tr>
                  </tbody></table></td>
              </tr>
            </tbody></table>
            <table width="486" border="0" align="center" cellpadding="0" cellspacing="0">
              <tbody><tr>
                <td valign="top"><table width="486" border="0" align="center" cellpadding="0" cellspacing="0" class="cn51black12b">
                    <tbody><tr>
                      <td height="26" background="./images/cn53c03.gif"><table width="486" border="0" cellspacing="0" cellpadding="0">
                          <tbody><tr>
                            <td width="30" align="center"><img src="./images/cn53c04.gif" width="14" height="14"></td>
                            <td width="409" class="cn5lan12b">学术活动</td>
                            <td width="47"><a href="./gjjl/xshd/"><img src="./images/cn53c05.gif" width="37" height="13" border="0"></a></td>
                          </tr>
                        </tbody></table></td>
                    </tr>
                    <tr>
                      <td height="1" bgcolor="#FFFFFF"></td>
                    </tr>
                    <tr>
                      <td height="1" bgcolor="#C8C8C8"></td>
                    </tr>
                  </tbody></table>
                  <table width="486" border="0" align="center" cellpadding="0" cellspacing="0">
                    <tbody><tr>
                      <td valign="top" style="padding:12px 0 18px 0"><table width="468" border="0" align="center" cellpadding="0" cellspacing="0" class="cn51blue123">
                          
						  <tbody><tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347"><a href="./gjjl/xshd/201706/U020170630542507718798.pdf" target="_blank" title="Context in Analysis of Multimodal Social Behavior" class="cn51blue123">Context in Analysis of Multimodal Social Behavior</a></td>
                            <td width="91">(2017-06-30)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347"><a href="./gjjl/xshd/201706/P020170627585437653417.pdf" target="_blank" title="New Deep Learning Approaches for Brain Image Segmentation, Analysis, and Related Problems" class="cn51blue123">New Deep Learning Approaches for Brain Image Segmentation...</a></td>
                            <td width="91">(2017-06-27)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347"><a href="./gjjl/xshd/201706/P020170627584790243445.pdf" target="_blank" title="Network Resource Management in Wireless Networked Control Systems" class="cn51blue123">Network Resource Management in Wireless Networked Control...</a></td>
                            <td width="91">(2017-06-27)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347"><a href="./gjjl/xshd/201706/P020170627584302683417.pdf" target="_blank" title="Dependable Wireless Control through Cyber-Physical Co-Design" class="cn51blue123">Dependable Wireless Control through Cyber-Physical Co-Design</a></td>
                            <td width="91">(2017-06-27)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347"><a href="./gjjl/xshd/201706/P020170627583825738986.pdf" target="_blank" title="整脑图灵机模型、自动通用编程机和未来人工智能产业" class="cn51blue123">整脑图灵机模型、自动通用编程机和未来人工智能产业</a></td>
                            <td width="91">(2017-06-27)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347"><a href="./gjjl/xshd/201706/t20170622_4816658.html" target="_blank" title="Meta Paths and Meta Structures: Analysing Large Heterogeneous Information Networks" class="cn51blue123">Meta Paths and Meta Structures: Analysing Large Heterogen...</a></td>
                            <td width="91">(2017-06-22)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347"><a href="./gjjl/xshd/201706/t20170622_4816657.html" target="_blank" title="TextScope: Enhance Human Perception via Text Mining" class="cn51blue123">TextScope: Enhance Human Perception via Text Mining</a></td>
                            <td width="91">(2017-06-22)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
						  <tr>
                            <td width="30" height="23" align="center"><img src="./images/cn53c06.gif" width="9" height="9"></td>
                            <td width="347"><a href="./gjjl/xshd/201706/P020170619578853364536.pdf" target="_blank" title="SRN: Side-output Residual Network for Object Symmetry Detection in the Wild" class="cn51blue123">SRN: Side-output Residual Network for Object Symmetry Det...</a></td>
                            <td width="91">(2017-06-19)</td>
                          </tr>
                          <tr>
                            <td height="1" colspan="3" background="./images/cn53c07.gif"></td>
                          </tr>
                          
                        </tbody></table></td>
                    </tr>
                  </tbody></table></td>
              </tr>
            </tbody></table>
            </td>
          <td width="230" bgcolor="#E6E6E6"><table width="230" border="0" cellspacing="0" cellpadding="0">
              <tbody><tr>
                <td><table width="230" border="0" cellspacing="0" cellpadding="0">
                    <tbody><tr>
                      <td height="1"></td>
                    </tr>
                    <tr>
                      <td height="36" background="./images/cnpl01_bj.gif"><table width="230" border="0" cellspacing="0" cellpadding="0">
                          <tbody><tr>
                            <td width="29" align="center"><img src="./images/cn53right01.gif" width="14" height="14"></td>
                            <td width="158" class="cn51white12b">通知公告</td>
                            <td width="43"><a href="./shye/tzgg/"><img src="./images/cn53c05.gif" width="37" height="13" border="0"></a></td>
                          </tr>
                        </tbody></table></td>
                    </tr>
                    <tr>
                      <td height="1" bgcolor="#B6BDB3"></td>
                    </tr>
                  </tbody></table></td>
              </tr>
              <tr>
                <td valign="top" style="padding:8px 0 10px 0"><table width="208" border="0" align="center" cellpadding="0" cellspacing="0">
                    
					<tbody><tr>
                      <td width="22" align="center"><img src="./images/cn53right03.gif" width="8" height="5"></td>
                      <td width="186" class="cn51gghui">
                        <a href="./shye/tzgg/201705/t20170511_4786955.html" target="_blank" title="欢迎参加中科院计算所2017年公众科学日" class="cn51gghui">欢迎参加中科院计算所2017年公...</a></td>
                    </tr>
                    <tr>
                      <td height="1" colspan="2" background="./images/cn53right02.gif"></td>
                    </tr>
					
					<tr>
                      <td width="22" align="center"><img src="./images/cn53right03.gif" width="8" height="5"></td>
                      <td width="186" class="cn51gghui">
                        <a href="./shye/tzgg/201705/t20170510_4786377.html" target="_blank" title="2017年“中国科学院大学生创新实践训练计划”计算所项目申报指南" class="cn51gghui">2017年“中国科学院大学生创新...</a></td>
                    </tr>
                    <tr>
                      <td height="1" colspan="2" background="./images/cn53right02.gif"></td>
                    </tr>
					
					<tr>
                      <td width="22" align="center"><img src="./images/cn53right03.gif" width="8" height="5"></td>
                      <td width="186" class="cn51gghui">
                        <a href="./shye/tzgg/201705/t20170508_4785191.html" target="_blank" title="“计算未来”全国大学生计算技术暑期研修班招生简章" class="cn51gghui">“计算未来”全国大学生计算技...</a></td>
                    </tr>
                    <tr>
                      <td height="1" colspan="2" background="./images/cn53right02.gif"></td>
                    </tr>
					
					<tr>
                      <td width="22" align="center"><img src="./images/cn53right03.gif" width="8" height="5"></td>
                      <td width="186" class="cn51gghui">
                        <a href="./shye/tzgg/201705/P020170503651424863783.pdf" target="_blank" title="计算所2017年度第六批拟聘员工人选公示" class="cn51gghui">计算所2017年度第六批拟聘员工...</a></td>
                    </tr>
                    <tr>
                      <td height="1" colspan="2" background="./images/cn53right02.gif"></td>
                    </tr>
					
                  </tbody></table></td>
              </tr>
            </tbody></table>
            <table width="230" border="0" cellspacing="0" cellpadding="0">
              <tbody><tr>
                <td><table width="230" border="0" cellspacing="0" cellpadding="0">
                    <tbody><tr>
                      <td height="1"></td>
                    </tr>
                    <tr>
                      <td height="28" background="./images/cnpl02_bj.gif"><table width="230" border="0" cellspacing="0" cellpadding="0">
                          <tbody><tr>
                            <td width="30" align="center"><img src="./images/cn53right01.gif" width="14" height="14"></td>
                            <td width="200" class="cn51white12b">专题</td>
                          </tr>
                        </tbody></table></td>
                    </tr>
                    <tr>
                      <td height="1" bgcolor="#B6BDB3"></td>
                    </tr>
                  </tbody></table></td>
              </tr>
              <tr>
                <td align="center" valign="middle" style="padding:10px 0 10px 0"><table width="0" border="0" cellspacing="0" cellpadding="5">
                  
				  <tbody><tr>
                    <td><a href="http://www.ict.ac.cn/ztwz/60zn/" target="_blank"><img src="./ztwz/200907/W020160718626096052014.jpg" alt="1st.jpg" width="200" height="80" border="0"></a></td>
                  </tr>
                  
				  <tr>
                    <td><a href="http://www.ict.cas.cn/rcjy/rczp/" target="_blank"><img src="./ztwz/201205/W020120509370609413428.jpg" width="200" height="80" border="0"></a></td>
                  </tr>
                  
				  <tr>
                    <td><a href="http://www.ict.cas.cn/liguojiewenxuan" target="_blank"><img src="./ztwz/200907/W020090819508874014762.jpg" width="200" height="80" border="0"></a></td>
                  </tr>
                  
                </tbody></table></td>
              </tr>
            </tbody></table>
            <table width="230" border="0" cellspacing="0" cellpadding="0">
              <tbody><tr>
                <td><table width="230" border="0" cellspacing="0" cellpadding="0">
                    <tbody><tr>
                      <td height="1"></td>
                    </tr>
                    <tr>
                      <td height="28" background="./images/cnpl02_bj.gif"><table width="230" border="0" cellspacing="0" cellpadding="0">
                          <tbody><tr>
                            <td width="30" align="center"><img src="./images/cn53right01.gif" width="14" height="14"></td>
                            <td width="200" class="cn51white12b">推荐链接</td>
                          </tr>
                        </tbody></table></td>
                    </tr>
                    <tr>
                      <td height="1" bgcolor="#B6BDB3"></td>
                    </tr>
                  </tbody></table></td>
              </tr>
              <tr>
                <td valign="top" style="padding:8px 0 10px 0"><table width="98%%" border="0" align="center" cellpadding="0" cellspacing="0" class="cn51hui12">
                    <tbody><tr>
                      <td valign="top">
					<marquee onmouseover="this.stop()" onmouseout="this.start()" scrollamount="1" scrolldelay="60" direction="up" width="100%" height="200">
                        <p style="MARGIN-TOP: 2px; MARGIN-BOTTOM: 1px; LINE-HEIGHT: 140%">
					</p><table cellspacing="0" cellpadding="0" width="100%" border="0">
					
					<tbody><tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://www.castt.ac.cn" target="_blank" title="中国科学院科技产业网" class="cn51hui12">中国科学院科技产业网</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://www.cambricon.com" target="_blank" title="中科寒武纪" class="cn51hui12">中科寒武纪</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://www.ict-ttc.com/" target="_blank" title="计算所技术转移中心" class="cn51hui12">计算所技术转移中心</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://www.chineseLDC.org" target="_blank" title="中文语言资源联盟" class="cn51hui12">中文语言资源联盟</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://lib.ict.ac.cn" target="_blank" title="计算所图书馆" class="cn51hui12">计算所图书馆</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://www.cas.cn/" target="_blank" title="中国科学院" class="cn51hui12">中国科学院</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://www.carch.ac.cn/" target="_blank" title="计算机体系结构国家重点实验室" class="cn51hui12">计算机体系结构国家重点实验室</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://awtrc.ict.ac.cn" target="_blank" title="无线通信技术研究中心" class="cn51hui12">无线通信技术研究中心</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://www.bioinfo.org.cn" target="_blank" title="中科院计算所生物信息课题组" class="cn51hui12">中科院计算所生物信息课题组</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://www.bjkp.gov.cn" target="_blank" title="北京科普之窗" class="cn51hui12">北京科普之窗</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://gs.ict.ac.cn" target="_blank" title="计算所研究生教育" class="cn51hui12">计算所研究生教育</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://www.siat.ac.cn" target="_blank" title="深圳先进技术研究院" class="cn51hui12">深圳先进技术研究院</a></span></p></td>
                    </tr>
					
					<tr>
                      <td width="20" height="20" align="right"><img src="./images/cn53left12.gif" width="10" height="10"></td>
					  <td width="10"></td>
                      <td width="230" align="left"><p style="MARGIN-TOP: 4px; MARGIN-BOTTOM: 4px; LINE-HEIGHT: 100%"><span style="FONT-SIZE: 13px"><a href="http://dragonstar.ict.ac.cn/" target="_blank" title="龙星计划" class="cn51hui12">龙星计划</a></span></p></td>
                    </tr>
					
					</tbody></table>
                    	<p></p>
                    </marquee>
					</td>
					</tr>
                  </tbody></table></td>
              </tr>
            </tbody></table></td>
        </tr>
      </tbody></table></td>
    <td width="15" background="./images/cn53r02.gif"><img src="./images/cn53r01.jpg"></td>
  </tr>
</tbody></table>
<script src="http://tracker2.cas.cn/wbtrk2.js" type="text/javascript"></script><script type="text/javascript">var iutTracker=_iutt._getTracker("UT-62877-1");iutTracker._trackPageview();</script>
<table width="1000" border="0" align="center" cellpadding="0" cellspacing="0">
  <tbody><tr>
    <td width="15" background="http://www.ict.cas.cn/images/cn53l02.gif">&nbsp;</td>
    <td width="970" bgcolor="#FFFFFF"><table width="970" border="0" align="center" cellpadding="0" cellspacing="6" bgcolor="#d1e0e8">
        <tbody><tr align="center">
          <td><a href="http://www.ict.cas.cn/qtgn/wzdt/" class="cn51blue123">网站地图</a>　|　<a href="http://www.ict.cas.cn/qtgn/lxfs/" class="cn51blue123">联系我们</a>　|　<a href="http://www.ict.cas.cn/qtgn/yjfk/" class="cn51blue123">意见反馈</a>　|　<a href="http://www.ict.cas.cn/qtgn/szxx/" class="cn51blue123">所长信箱</a> </td>
        </tr>
    </tbody></table></td>
    <td width="15" background="http://www.ict.cas.cn/images/cn53r02.gif">&nbsp;</td>
  </tr>
</tbody></table>
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0">
  <tbody><tr>
    <td align="center" valign="top" background="http://www.ict.cas.cn/images/cn53bottom01.gif"><table width="970" height="70" border="0" cellspacing="0" cellpadding="0">
        <tbody><tr bgcolor="#5A6871">
          <td width="250" align="center">
		  </td>
          <td width="520" class="cn51white12" style="padding:0 0 0 20px">京ICP备05002829号　京公网安备1101080060号</td>
          <td width="200" class="cn51white12" style="padding:0 0 0 20px"><script type="text/javascript">document.write(unescape("%3Cspan id='_ideConac' %3E%3C/span%3E%3Cscript src='http://dcs.conac.cn/js/33/000/0000/60440102/CA330000000604401020002.js' type='text/javascript'%3E%3C/script%3E"));</script><span id="_ideConac"><a href="//bszs.conac.cn/sitename?method=show&amp;id=08E6159BAAA4168DE053022819AC06AE" target="_blank"><img id="imgConac" vspace="0" hspace="0" border="0" src="//dcs.conac.cn/image/blue.png" data-bd-imgshare-binded="1"></a></span><script src="http://dcs.conac.cn/js/33/000/0000/60440102/CA330000000604401020002.js" type="text/javascript"></script><span id="_ideConac"></span></td>
        </tr>
    </tbody></table></td>
  </tr>
</tbody></table>

</body></html>
"""
reduction_ratio = 1.0
# 
# start = time.time()
print reduction.reduce(content9, reduction_ratio)[0].decode('utf-8')
# print reduction.reduce(content10, reduction_ratio)[0].decode('utf-8'),time.time() - start