from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.views.generic import ListView

from  .forms import EmailPostForm,CommentForm,SearchForm

from django.core.mail import send_mail

from taggit.models import Tag

from django.db.models import Count

from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank,TrigramSimilarity
# Create your views here.

def index(request):

    # return HttpResponse('首页通知书')

    return render(request,'motangtest/index.html')


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 2
#     template_name = 'blog/post/list.html'

def post_list(request,tag_slug=None):
    object_list  = Post.published.all()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])


    paginator = Paginator(object_list,2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'blog/post/list.html',{'posts':posts,'tag': tag}) # 可以不用加page

# def post_detail(request,year,month,day,post):
#     post = get_object_or_404(Post,slug=post,status='published',publish__year = year,publish__month=month,publish__day = day)
#     # 获得数据或者404

#     return render(request,'blog/post/detail.html',{'post':post})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month, publish__day=day)
    
    comments = post.comments.filter(active=True)

    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_tags = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            
            new_comment = comment_form.save(commit=False)
            
            new_comment.post = post
            
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',{'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form,'similar_posts': similar_posts})

def post_share(request,post_id):

    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False

    if request.method == 'POST':

        form = EmailPostForm(request.POST)

        if form.is_valid():

            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject,message, '1580120495@qq.com ', [cd['to']],fail_silently=False)# 自己邮箱(form表单发来的邮件还不用后端固定的？) 自己的STMP服务器 to是发送的邮箱
            sent = True
            
    else:
        form = EmailPostForm()

    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent': sent})



def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # results = Post.objects.annotate(search=SearchVector('title', 'slug', 'body'), ).filter(search=query) # 使用搜索
            # 数据库应该不止postgres指出全局搜索吧(??)
            
            # search_vector = SearchVector('title', 'body')
            #可以对在标题中搜索到的结果给予比正文中搜索到的结果更大的权重
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(search=search_vector,rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            
            #results = Post.objects.annotate(similarity=TrigramSimilarity('title',query),).filter(similarity__gte=0.1).order_by('-similarity')

    return render(request, 'blog/post/search.html', {'query': query, "form": form, 'results': results})