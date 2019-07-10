# -*- coding:utf-8 -*-
__author__ = 'wrz'
__data__ = '2019/7/2 11:01'

from django.core.paginator import Paginator

# 实现博客文章分页功能

def paginator(request, object, per_page_nums):
    '''
    :param request: django request 对象
    :param object: 查询集
    :param per_page_nums: 每页的数量
    :return:
    '''
    page = request.GET.get('page', 1)
    paginator = Paginator(object, per_page_nums)
    object_of_page = paginator.get_page(page)
    page = int(page)

    # todo:进行页码的控制，页面上最多显示5个页码
    # 1.总页数小于5页，显示所有页码
    # 2.如果当前页是前三页的时候，显示 1-5 页
    # 3.如果当前页是后三页，显示后五页
    # 4.其他情况，显示当前页的前两页，当前页，当前页的后两页
    num_pages = paginator.num_pages
    if num_pages < 5:
        pages = range(1, num_pages + 1)
    elif page < 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(page - 2, page + 3)
    return object_of_page,pages