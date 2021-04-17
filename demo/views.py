from django.shortcuts import render
from .models import Article, ArticleClassification, Tag, Mood
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic.base import View
# from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def int_page(total, per):
    if total / per > total // per:
        return total // per + 1
    else:
        return total // per


def index(request):
    articles_object = Article.objects.filter(is_object=True).all()  # 筛选出是项目的文章
    if len(articles_object) > 6:
        articles_object = articles_object[:6]
    article_news = Article.objects.order_by('-public_time')  # 将所有项目按时间排序查找，最新发布栏
    article_top = Article.objects.filter(is_recommend=True).all()[0]  # 置顶
    classes = ArticleClassification.objects.all()  # 所有分类
    tags = Tag.objects.all()  # 所有文章标签
    kwgs = {
        "article_top": article_top,
        "articles": articles_object,
        "article_news": article_news,
        "classes": classes,
        "tags": tags
    }
    return render(request, "index.html", kwgs)


def about(request):
    return render(request, "about.html")


class _Article(View):
    per_page = 4
    articles = Article.objects.order_by('-public_time')
    classes = ArticleClassification.objects.all()  # 所有分类
    tags = Tag.objects.all()  # 所有文章标签
    paginator = Paginator(articles, per_page)
    article_news = Article.objects.order_by('-public_time')
    page_num = int_page(len(articles),per_page)

    def get(self, request):
        search_articles = self.paginator.page(1)
        kwgs = {
            "page_num": self.page_num,
            "articles": search_articles,
            "article_news": self.articles,
            "classes": self.classes,
            "tags": self.tags
        }
        return render(request, "article.html", kwgs)

    def post(self, request):
        page = int(request.POST.get("page", 1))
        try:
            search_articles = self.paginator.page(page)
        except(EmptyPage, InvalidPage, PageNotAnInteger) as ex:
            search_articles = self.paginator.page(1)
        kwgs = {
            "articles": search_articles,
            "article_news": search_articles,
        }
        return render(request, "request_result.html", kwgs)


def article_detail(request, id):
    id = int(id)
    article = Article.objects.get(id=id)
    ip = request.META["REMOTE_ADDR"]
    sessionid = ip + str(id)
    if not request.session.get(sessionid):
        article.view_times += 1
        article.save()
        request.session[sessionid] = True
    try:
        article_pre = Article.objects.get(id=id-1)
    except:
        article_pre = None
    try:
        article_next = Article.objects.get(id=id+1)
    except:
        article_next = None
    article_news = Article.objects.order_by('-public_time')
    kwgs = {
        "article": article,
        "article_news": article_news,
        "article_pre": article_pre,
        "article_next": article_next
    }
    return render(request, "article_detail.html", kwgs)


class _Mood(View):
    moods = Mood.objects.order_by('-date')
    per_page = 10
    paginator = Paginator(moods, per_page)

    def get(self, request):
        page_num = int_page(len(self.moods), self.per_page)
        moods = self.paginator.page(1)
        kwgs = {
            "moods": moods,
            "page_num": page_num
        }
        return render(request, "moodList.html", kwgs)

    def post(self, request):
        page = int(request.POST.get("page", 1))
        moods = self.paginator.page(page)
        kwgs = {
            "moods": moods
        }
        return render(request, "Request_mood_list.html", kwgs)


class Search(View):
    per_page = 3

    def get(self, request):
        keywords = request.GET.get("keywords", "")  # 取得关键字
        articles = Article.objects.filter(Q(abstract__icontains=keywords)  # 数据库查询
                                          | Q(title__icontains=keywords)
                                          | Q(content__icontains=keywords))
        paginator = Paginator(articles, self.per_page)  # 分页
        search_articles = paginator.page(1)
        search_article_num = len(articles)  # 总文章数
        page_num = int_page(search_article_num, self.per_page)
        article_news = Article.objects.order_by('-public_time')  # 将所有项目按时间排序查找，最新发布栏
        classes = ArticleClassification.objects.all()  # 所有分类
        tags = Tag.objects.all()  # 所有文章标签
        if len(articles) == 0:
            kwgs = {
                "article_news": article_news,
                "classes": classes,
                "tags": tags,
                "keywords": keywords
            }
            return render(request, "Noresult.html", kwgs)
        kwgs = {
            "search_article_num": search_article_num,
            "page_num": page_num,
            "articles": search_articles,
            "article_news": article_news,
            "classes": classes,
            "tags": tags,
            "keywords": keywords
        }
        return render(request, "search.html", kwgs)

    def post(self, request):
        keywords = request.GET.get("keywords", "")  # 取得关键字
        page = int(request.POST.get("page", 1))  # 获取分页页数
        articles = Article.objects.filter(Q(abstract__icontains=keywords)  # 数据库查询
                                          | Q(title__icontains=keywords)
                                          | Q(content__icontains=keywords))
        paginator = Paginator(articles, self.per_page)  # 分页
        search_articles = paginator.page(page)
        kwgs = {
            "articles": search_articles,
            "keywords": keywords
        }
        return render(request, "request_result.html", kwgs)


def Class(request, id):
    articles = Article.objects.filter(article_class=id).all()
    article_news = Article.objects.order_by('-public_time')
    classes = ArticleClassification.objects.all()  # 所有分类
    tags = Tag.objects.all()  # 所有文章标签
    kwgs = {
        "articles": articles,
        "article_news": article_news,
        "classes": classes,
        "tags": tags
    }
    return render(request, "article.html", kwgs)


def tag(request, id):
    articles = Article.objects.filter(article_tag=id).all()
    article_news = Article.objects.order_by('-public_time')
    classes = ArticleClassification.objects.all()  # 所有分类
    tags = Tag.objects.all()  # 所有文章标签
    kwgs = {
        "articles": articles,
        "article_news": article_news,
        "classes": classes,
        "tags": tags
    }
    return render(request, "article.html", kwgs)

