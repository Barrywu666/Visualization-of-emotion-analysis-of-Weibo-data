import json

import pymysql
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from .word_cloud import word_cloud


# Create your views here.


def change(request):
    db = pymysql.connect("localhost", "root", "w123", "bigdata")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM kunming "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()

    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    print(results)
    i = 0
    myData = []
    while results[i][0]:
        dict = {'name': results[i][0], 'value': [results[i][1], results[i][2], results[i][3], results[i][4]]}
        myData.append(dict)
        i = i + 1
        try:
            results[i][0]
        except:
            break
    return render(request, 'page3.html', {'myData': json.dumps(myData)})


def word(request):
    global results
    db = pymysql.connect("localhost", "root", "w123", "bigdata")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    if request.method == "POST":
        a = request.POST.get("time")
        b = request.POST.get("myselect")
        print(a)
        print(b)
        sql = "SELECT content FROM emotiondata WHERE date ='%s' and name = '%s'" % (a, b)
        sql2 = "SELECT name,jd,wd,emotion FROM emotiondata WHERE date ='%s' and name = '%s'" % (a, b)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            print(3)
            results = cursor.fetchall()
            print(4)
            print(results)
            filepath = 'D:\\PyCharmworkspace\\pyworkspace\\大数据分析\\BigData\\static\\image\\cloud.png'
            content = str(results)
            print(5)
            word_cloud.draw_wordcloud(filepath, content)
            print(7)
            print(8)
        except:
            print("Error: unable to fecth data")
            a = '没有数据'
            return render(request, 'page3.html', {'a': a})
        try:
            # 执行SQL语句
            cursor.execute(sql2)
            # 获取所有记录列表
            results = cursor.fetchall()

        except:
            print("Error: unable to fecth data")
        print(results)
        i = 0
        myData = []
        while results[i][0]:
            dict = {'name': results[i][0], 'value': [results[i][1], results[i][2], results[i][3], 500]}
            myData.append(dict)
            i = i + 1
            try:
                results[i][0]
            except:
                break
        db.close()
        # 关闭数据库连接
        return render(request, 'page3.html', {'a': a, 'b': b, 'myData': myData})
    if request.method == "GET":
        a = request.GET.get("time2")
        sql = "SELECT content FROM emotiondata WHERE date ='%s'" % a
        sql2 = "SELECT name,jd,wd,emotion FROM emotiondata WHERE date ='%s'" % a
        print(a)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            print(3)
            results = cursor.fetchall()
            print(4)
            print(results)
            filepath = 'D:\\PyCharmworkspace\\pyworkspace\\大数据分析\\BigData\\static\\image\\cloud.png'
            content = str(results)
            print(5)
            word_cloud.draw_wordcloud(filepath, content)
            print(7)
            print(8)
        except:
            print("Error: unable to fecth data")
            a = '没有数据'
            return render(request, 'page3.html', {'c': a})
        try:
            # 执行SQL语句
            cursor.execute(sql2)
            # 获取所有记录列表
            results = cursor.fetchall()

        except:
            print("Error: unable to fecth data")
        print(results)
        i = 0
        myData = []
        while results[i][0]:
            dict = {'name': results[i][0], 'value': [results[i][1], results[i][2], results[i][3], 500]}
            myData.append(dict)
            i = i + 1
            try:
                results[i][0]
            except:
                break
        # 关闭数据库连接
        db.close()
        return render(request, 'page3.html', {'c': a, 'myData': myData})


def demo_ajax(request):
    return render(request, 'page2.html')


def demo_ajax2(request):
    return render(request, 'test.html')


def demo_test2(request, recordid):
    a = recordid
    global results
    db = pymysql.connect("localhost", "root", "w123", "bigdata")
    cursor = db.cursor()
    sql = "select userid,date,name,content from emotiondata where userid = '" + a + "' order by date asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    content_list = []
    for res in results:
        content_list.append(res)
    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(content_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            books = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            books = paginator.page(paginator.num_pages)
    template_view = 'test2.html'
    return render(request, template_view, {'books': books, 'username': a})


def demo_search(request):
    global results
    a = request.GET['a']
    b = request.GET['b']
    db = pymysql.connect("localhost", "root", "w123", "bigdata")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    print(a)
    print(b)
    # SQL 查询语句
    sql = "SELECT 喜,怒,哀,乐,平和,主流情感,主感数 FROM 分类 WHERE date ='" + a + "' and name = '" + b + "' "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print(results)
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    xi = results[0][0]
    nu = results[0][1]
    ai = results[0][2]
    le = results[0][3]
    pe = results[0][4]
    zhu = results[0][5]
    zs = results[0][6]
    c = HttpResponse()
    c.content = xi, ',', nu, ',', ai, ',', le, ',', pe, ',', zhu, ',', zs
    return c


def demo_graph(request):
    global results
    name = request.GET['c']
    db = pymysql.connect("localhost", "root", "w123", "bigdata")
    cursor = db.cursor()
    sql = "select date,name,主流情感 from 分类 where name = '" + name + "' order by date asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    i = 0
    res = []
    while results[i][0]:
        res.append(results[i][0])
        res.append(",")
        res.append(results[i][2])
        res.append(",")
        i = i + 1
        try:
            results[i][0]
        except:
            break
    ret = HttpResponse((res))
    return ret


def demo_test(request):
    global results
    db = pymysql.connect("localhost", "root", "w123", "bigdata")
    cursor = db.cursor()
    sql = "select userid,date,name,content,mingan from emotiondata where mingan != ' ' order by date asc"
    cursor.execute(sql)
    results = cursor.fetchall()
    book_list = []
    for res in results:
        book_list.append(res)
    print(res[0])
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(book_list, 10)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            books = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            books = paginator.page(paginator.num_pages)
    template_view = 'test.html'
    return render(request, template_view, {'books': books})


def search(request):
    global results
    a = request.GET.get("searchcontent")
    db = pymysql.connect("localhost", "root", "w123", "bigdata")
    cursor = db.cursor()
    sql = "select userid,date,name,content,emotion from emotiondata where CONCAT(IFNULL(content,''),IFNULL(date,'')," \
          "IFNULL(name,''),IFNULL(emotion,''),IFNULL(userid,'')) like '%%%s%%' " %a
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results[0][2])
    except:
        return HttpResponse('抱歉，你搜索的记录走丢了')
    book_list = []
    for res in results:
        book_list.append(res)
    '''
    userid like '%%%s%%' or  date like '%%%s%%' or " 
          "name like  '%%%s%%' or content like '%%%s%%' or emotion
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(book_list, 10)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            books = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            books = paginator.page(paginator.num_pages)
    template_view = 'searchresults.html'
    return render(request, template_view, {'books': books,'select':a})
