# install https://wkhtmltopdf.org/downloads.html
import urllib.request
from bs4 import BeautifulSoup
import pdfkit
import os
import random

user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def downloadPage(url, name):
    name = name.title()
    name = name.translate(
        str.maketrans(
            {"-": r"", " ": r"", "]": r"", "\\": r"", "^": r"", "$": r"", "*": r"", ".": r"", "[": r"", "…": r""}))
    pdf_file = path + name + ".pdf"
    if not os.path.exists(pdf_file):
        link = url
        pdfkit.from_url(link, pdf_file)
        print(name + " opgeslagen!")


print(os.getcwd())
print("Geef de link van de pagina met alle linken")
link = input("URL:")
print("Hoe moet de output map heten?")
directory = input("Foldernaam:")

path = os.getcwd() + "/output/" + directory + "/"
if not os.path.exists(path):
    print("Making dir " + path)
    os.mkdir(path)

user_agent = random.choice(user_agent_list)
request = urllib.request.Request(link, headers={'User-Agent': user_agent})

with urllib.request.urlopen(request) as url:
    s = url.read()
    soup = BeautifulSoup(s, "html.parser", from_encoding="utf-8")
    if ("stackoverflow" in link):
        getAmountOfPages = soup.select("a:nth-child(5n+7) span")
        print(getAmountOfPages[0].text)
        for x in range(int(getAmountOfPages[0].text)):
            print("PAGE " + str(x) + " OF " + str(getAmountOfPages[0].text))
            link2 = link.replace(" ", "") + "&pagesize=50&page=" + str(x)
            # print(link2)
            user_agent = random.choice(user_agent_list)
            request = urllib.request.Request(link2, headers={'User-Agent': user_agent})
            with urllib.request.urlopen(request) as newLink:
                s2 = newLink.read()
                soup2 = BeautifulSoup(s2, "html.parser", from_encoding="utf-8")
                getArticleInformation = soup2.select("#questions .question-summary")
                for y in range(len(getArticleInformation)):
                    selector = "#questions .question-summary:nth-child(" + str(y) + ") div.status.answered-accepted"
                    getArticleInformation = soup2.select(selector)
                    # print(getArticleInformation)
                    if getArticleInformation != []:
                        selector = "#questions .question-summary:nth-child(" + str(
                            y) + ") h3 a"
                        getArticleLink = soup2.select(selector)
                        downloadLink = str("https://stackoverflow.com" + getArticleLink[0]['href'])
                        downloadName = str(getArticleLink[0].text)
                        downloadPage(downloadLink, downloadName)

                    # ArticleInformation = getArticleInformation[y].select("div.status")
        # print(amountOfPages)
        # for y in range(amountOfPages):
        #    page = "https://stackoverflow.com/questions/tagged/java?tab=newest&pagesize=50&page=" + y
        #    with urllib.request.urlopen(page) as url2:
        #        s2 = url2.read()
        #        soup2 = BeautifulSoup(s2, "html.parser", from_encoding="utf-8")
        #        amountOfQuestions = soup2.select("question-summary")
        #        for z in range(amountOfQuestions):
        #            print(z)
    else:
        print("Vul de selector in:")
        selector = input()
        found = soup.select(selector)
        # page-numbers
        for x in range(len(found)):
            line = found[x]['href']
            downloadPage(link, line)
    print("Done!")

# import urllib2
# import html2text
# url=''
# page = urllib2.urlopen(url)
# html_content = page.read()
# rendered_content = html2text.html2text(html_content)
# file = open('file_text.txt', 'w')
# file.write(rendered_content)
# file.close()
