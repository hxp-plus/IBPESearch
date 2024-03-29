# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
# TODO:Remove proxy if you are not using
# proxies = { "http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080", } # 调试的时候在国内需要走代理
def search(request):
    context = {}
    if 'q' in request.GET and request.GET['action'] == 'google':
        context['items'] = []
        for i in range(5):
            response = requests.get("https://www.google.com/"+"search?q="+request.GET['q']+"&start="+str(10*i-10),
                                    headers=headers
                                    ).text
            soup = BeautifulSoup(response, 'lxml')
            divs = soup.find_all('div')
            for div in divs:
                if div.find('div'):
                    if div.find('div').find('div'):
                        if div.find('div').find('div').find('a'):
                            if div.find('div').find('div').find('a').find('h3'):
                                if str(div).find('<!--m-->') == -1:
                                    print(str(div))
                                    item = {}
                                    item['title'] = div.find('h3').text
                                    item['subtitle'] = div.find('cite').text
                                    item['link'] = div.find('a')['href']
                                    if div.find('span', class_="st"):
                                        item['preview'] = div.find('span', class_="st").text
                                    else:
                                        item['preview'] = "Preview not Supported"
                                    context['items'].append(item)
    if 'q' in request.GET and request.GET['action'] == 'wikipedia':
        context['items'] = []
        print("https://en.wikipedia.org/w/index.php?search="+request.GET['q']+"&limit=50")
        # TODO:Remove proxy if you are not using
        # response =\
        #     requests.get("https://en.wikipedia.org/w/index.php?search="+
        #                  request.GET['q']+
        #                  "&title=Special%3ASearch&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1",
        #                  headers=headers, proxies=proxies).text
        response =\
            requests.get("https://en.wikipedia.org/w/index.php?search="+
                         request.GET['q']+
                         "&title=Special%3ASearch&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1",
                         headers=headers).text
        soup = BeautifulSoup(response, 'lxml')
        lis = soup.find_all('li', class_="mw-search-result")
        for li in lis:
            item = {}
            a=li.find('div', class_="mw-search-result-heading").find('a')
            item['title'] = a.text
            item['link'] = a['href']
            item['preview'] = li.find('div', class_="searchresult").text
            item['date'] = li.find('div', class_="mw-search-result-data").text
            item['subtitle'] = ""
            context['items'].append(item)
    return render(request, 'search.html', context)


def downloadwiki(request, slug):
    print(slug)
    pdf_url = "https://en.wikipedia.org/api/rest_v1/page/pdf/"+slug
    # TODO:Remove proxy if you are not using
    # r = requests.get(pdf_url, proxies=proxies)
    r = requests.get(pdf_url)
    with open("pdf/"+slug + ".pdf", 'wb') as f:
        f.write(r.content)
    with open("pdf/"+slug + ".pdf", 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
    pdf.close()
    return response

