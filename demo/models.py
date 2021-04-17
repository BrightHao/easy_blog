from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class ArticleClassification(models.Model):
    """文章分类"""
    Class_name = models.CharField(max_length=128, verbose_name="文章分类")

    def __str__(self):
        return self.Class_name

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """文章标签"""
    Tag_name = models.CharField(max_length=128, verbose_name="文章标签")

    def __str__(self):
        return self.Tag_name

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """"文章评论"""
    Comment_user = models.CharField(max_length=128, verbose_name="评论用户")
    Comment_content = models.CharField(max_length=1024, verbose_name="评论内容")
    Comment_time = models.DateTimeField(verbose_name="发布日期")

    def __str__(self):
        return self.Comment_content

    class Meta:
        verbose_name = "文章评论"
        verbose_name_plural = verbose_name


class Article(models.Model):
    """文章表"""
    title = models.CharField(max_length=128, verbose_name="文章标题")
    abstract = models.CharField(max_length=256, verbose_name="文章摘要", null=True, blank=True)
    # blank允许字段为空，null数据库内容为空
    cover = models.ImageField(upload_to="./article/%Y/%m%d/", verbose_name="文章封面", null=True, blank=True)
    public_time = models.DateTimeField(auto_now_add=True)  # 创建时间,不会变化
    latest_time = models.DateTimeField(auto_now=True)  # 最后修改时间，修改之后自动更新时间
    content = RichTextUploadingField(verbose_name="文章详情")
    # on_delete 当删除关联表中的数据时，当前表与其关联的行的行为。
    article_class = models.ForeignKey(ArticleClassification, on_delete=models.DO_NOTHING, related_name="ArticleClass",
                                      verbose_name="分类")
    article_tag = models.ManyToManyField(Tag, related_name="ArticleTag", verbose_name="标签", blank=True)
    view_times = models.IntegerField(default=0, verbose_name="浏览次数")
    comments = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, verbose_name="文章评论", related_name="comments",
                                 null=True, blank=True)
    is_recommend = models.BooleanField(default=False, verbose_name="置顶")
    is_object = models.BooleanField(default=False, verbose_name="是否项目")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章表"
        verbose_name_plural = verbose_name


class Mood(models.Model):
    """说说"""
    date = models.DateField(auto_now_add=True)
    content = models.CharField(max_length=2048)
    image = models.ImageField(upload_to="./mood/%Y/%m%d/", verbose_name="说说图片", null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "说说"
        verbose_name_plural = verbose_name
