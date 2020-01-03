from django import template
from ..models import Post
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=3): # 默认显示数据库最新的三条 传入参数会覆盖
    latest_posts = Post.published.order_by('publish')[:count] #倒叙排行（-去掉就是正序找最旧的）
    return {'latest_posts': latest_posts}

@register.filter(name='markdown') #装饰器是负载一些原模板过滤器的作用的
def markdown_format(text):

    return mark_safe(markdown.markdown(text))