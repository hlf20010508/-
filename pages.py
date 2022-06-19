import tkinter as tk
from tkinter import ttk
from custom_widget import spacex, spacey, message_box, multipleList
import pymysql
import json

try:
    config_file = open('config.json')
except:
    print('未找到数据库配置文件，请先运行config.py')
    print('python config.py')
    exit()

config = json.load(config_file)
config_file.close()


db = pymysql.connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    database=config['database'])

cursor = db.cursor()

pwd_admin = '123' #管理员密码


def isnum(s):
    l = s.split('.')
    if len(l) > 2:
        return 0
    elif len(l) == 1:
        if l[0].isdigit():
            return 1
        else:
            return 0
    elif len(l) == 2:
        if l[0].isdigit() and l[1].isdigit():
            return 2
        else:
            return 0


def sql(s):
    global cursor
    cursor.execute(s)
    try:
        data = cursor.fetchall()
        result = []
        for item in data:
            result.append(list(item))
        for i in range(len(result)):
            for j in range(len(result[i])):
                if isinstance(result[i][j], str):
                    result[i][j] = result[i][j].rstrip()
        return result
    except Exception:
        return


class help_page:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('帮助')

        sw = self.root.winfo_screenwidth()//2
        sh = self.root.winfo_screenheight()//2
        self.root.geometry('250x150+{}+{}'.format(sw-200, sh-200))

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        spacey(self.frame, 10)

        name_label = tk.Label(
            self.frame,
            text='学生成绩管理系统')
        name_label.pack()

        spacey(self.frame, 10)

        class_label = tk.Label(
            self.frame,
            text='作者')
        class_label.pack()

        spacey(self.frame, 10)

        author_label = tk.Label(
            self.frame,
            text='L-ING')
        author_label.pack()

        spacey(self.frame, 10)

        exit = tk.Button(
            self.frame,
            text='退出',
            command=self.exit)
        exit.pack()

    def exit(self):
        self.root.destroy()


class query_page:
    def __init__(self, master):  # 需要重定义self.get_sql(),self.get_area(),self.root.title(),self.exit()
        self.area = self.get_area()
        self.sql = self.get_sql()
        self.data = self.get_data()

        self.root = master
        self.root.geometry('500x400')

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        spacey(self.frame, 10)

        top_sub_frame = tk.Frame(self.frame)
        top_sub_frame.pack(fill='x')

        help = tk.Button(
            top_sub_frame,
            text='帮助',
            command=self.help)
        help.pack(side='left')

        spacex(top_sub_frame, 10, side='left')

        exit = tk.Button(
            top_sub_frame,
            text='退出',
            command=self.exit)
        exit.pack(side='left')

        tk.Frame(top_sub_frame).pack(side='left', fill='x')

        spacey(self.frame, 10)

        id_sub_frame = tk.Frame(self.frame)
        id_sub_frame.pack()

        id_label = tk.Label(
            id_sub_frame,
            text='学号')
        id_label.pack(side='left')

        spacex(id_sub_frame, 5, side='left')

        self.search_entry = tk.Entry(id_sub_frame)
        self.search_entry.pack(side='left')

        spacex(id_sub_frame, 5, side='left')

        search = tk.Button(
            id_sub_frame,
            text='查询',
            command=self.search)
        search.pack(side='left')

        spacex(id_sub_frame, 5, side='left')

        reset = tk.Button(
            id_sub_frame,
            text='复位',
            command=self.load)
        reset.pack(side='left')

        spacey(self.frame, 10)

        self.details_list = self.get_list()
        self.details_list.pack()

        self.load()

    def get_list(self):
        _list = multipleList(
            self.frame,
            area=self.area,
            command=self.search_double_click,
            height=15)
        return _list

    def get_area(self):
        return 0

    def get_sql(self):
        return 0

    def clear(self):
        for item in self.details_list.get_children():
            self.details_list.delete(item)

    def get_data(self):
        return sql(self.sql)

    def load(self):
        self.clear()
        for item in self.data:
            self.details_list.insert('', 'end', values=item)

    def search(self):
        _id = self.search_entry.get()
        self.load()
        if isnum(_id) == 1:
            result = sql(self.sql+' where sno=%s' % _id)
            if _id not in [item[0] for item in result]:
                message_box('学号不存在，请重新输入！')
            else:
                self.clear()
                for item in result:
                    self.details_list.insert('', 'end', values=item)
        elif _id == '':
            message_box('学号不能为空!')
        else:
            message_box('请输入数字！')

    def search_double_click(self, event):
        _id = self.details_list.item(self.details_list.focus(), 'values')[0]
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, _id)
        self.search()

    def help(self):
        help_page()

    def exit(self):
        return 0


class course_details_student_page(query_page):
    def __init__(self, master):
        super(course_details_student_page, self).__init__(master)
        self.root.title('开课情况查询')

    def get_area(self):
        return ('学号', '课程号', '课程名', '学分')

    def get_sql(self):
        return 'select * from xskkqk'

    def exit(self):
        self.frame.destroy()
        student_menu_page(self.root)


class each_grade_query_student_page(query_page):
    def __init__(self, master):
        super(each_grade_query_student_page, self).__init__(master)
        self.root.geometry('550x400')
        self.root.title('单科成绩查询')

    def get_area(self):
        return ('学号', '姓名', '班级', '科目', '成绩')

    def get_sql(self):
        return 'select * from xsdkcj'

    def exit(self):
        self.frame.destroy()
        grade_query_mode_student_page(self.root)


class sum_grade_query_student_page(query_page):
    def __init__(self, master):
        super(sum_grade_query_student_page, self).__init__(master)
        self.root.title('总成绩查询')

    def get_area(self):
        return ('学号', '姓名', '班级', '总成绩')

    def get_sql(self):
        return 'select * from xszcj'

    def search_double_click(self, event):
        _id = self.details_list.item(self.details_list.focus(), 'values')[0]
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, _id)

    def exit(self):
        self.frame.destroy()
        grade_query_mode_student_page(self.root)


class grade_query_mode_student_page:
    def __init__(self, master):
        self.root = master
        self.root.title('学生成绩查询模式')
        self.root.geometry('200x110')

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        spacey(self.frame, 10)

        top_sub_frame = tk.Frame(self.frame)
        top_sub_frame.pack()

        help = tk.Button(
            top_sub_frame,
            text='帮助',
            command=self.help)
        help.pack(side='left')

        spacex(top_sub_frame, 10, side='left')

        exit = tk.Button(
            top_sub_frame,
            text='退出',
            command=self.exit)
        exit.pack(side='left')

        spacey(self.frame, 10)

        each_grade = tk.Button(
            self.frame,
            text='单科成绩',
            command=self.each_grade)
        each_grade.pack()

        spacey(self.frame, 10)

        sum_grade = tk.Button(
            self.frame,
            text='总成绩',
            command=self.sum_grade)
        sum_grade.pack()

        spacey(self.frame, 10)

    def each_grade(self):
        self.frame.destroy()
        each_grade_query_student_page(self.root)

    def sum_grade(self):
        self.frame.destroy()
        sum_grade_query_student_page(self.root)

    def help(self):
        help_page()

    def exit(self):
        self.frame.destroy()
        student_menu_page(self.root)


class student_menu_page:
    def __init__(self, master):
        self.root = master
        self.root.title('学生操作菜单')
        self.root.geometry('200x110')

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        spacey(self.frame, 10)

        top_sub_frame = tk.Frame(self.frame)
        top_sub_frame.pack()

        help = tk.Button(
            top_sub_frame,
            text='帮助',
            command=self.help)
        help.pack(side='left')

        spacex(top_sub_frame, 10, side='left')

        exit = tk.Button(
            top_sub_frame,
            text='退出',
            command=self.exit)
        exit.pack(side='left')

        spacey(self.frame, 10)

        bottom_sub_frame = tk.Frame(self.frame)
        bottom_sub_frame.pack()

        course_details = tk.Button(
            bottom_sub_frame,
            text='开课情况查询',
            command=self.course_details)
        course_details.pack()

        spacey(bottom_sub_frame, 10)

        grade_query_mode = tk.Button(
            bottom_sub_frame,
            text='学生成绩查询',
            command=self.grade_query_mode)
        grade_query_mode.pack()

        spacey(self.frame, 10)

    def help(self):
        help_page()

    def exit(self):
        self.frame.destroy()
        mode_choosing_page(self.root)

    def course_details(self):
        self.frame.destroy()
        course_details_student_page(self.root)

    def grade_query_mode(self):
        self.frame.destroy()
        grade_query_mode_student_page(self.root)


class course_details_admin_page(query_page):
    def __init__(self, master):
        self.sql = self.get_sql()
        self.data = self.get_data()

        self.root = master
        self.root.title('开课情况')
        self.root.geometry('350x280')

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        spacey(self.frame, 10)

        top_sub_frame = tk.Frame(self.frame)
        top_sub_frame.pack(fill='x')

        help = tk.Button(
            top_sub_frame,
            text='帮助',
            command=self.help)
        help.pack(side='left')

        spacex(top_sub_frame, 10, side='left')

        exit = tk.Button(
            top_sub_frame,
            text='退出',
            command=self.exit)
        exit.pack(side='left')

        tk.Frame(top_sub_frame).pack(side='left', fill='x')

        spacey(self.frame, 10)

        self.details_list = multipleList(
            self.frame,
            area=('课程号', '课程名', '绩点'),
            height=11)
        self.details_list.pack()

        self.load()

    def exit(self):
        self.frame.destroy()
        admin_menu_page(self.root)

    def get_sql(self):
        return 'select * from kc'


class grade_query_admin_page(query_page):
    def __init__(self, master):
        super(grade_query_admin_page, self).__init__(master)
        self.root.title('学生成绩查询')
        self.root.geometry('1000x500')

    def get_list(self):
        _list = multipleList(
            self.frame,
            area=self.area,
            height=20,
            width=(100, 50, 30, 55, 75, 55, 40, 35,
                   55, 100, 65, 55, 55, 40, 40, 40),
            command=self.search_double_click)
        return _list

    def get_area(self):
        return ('学号', '姓名', '班级', '线性代数', '政治经济原理', '数据结构', '英语', 'C++', '电子技术', '计算机组成原理', '计算机网络', '哲学原理', '数值分析', '体育', '总分', '排名')

    def get_sql(self):
        return 'select * from xscjxqpm'

    def search_double_click(self, event):
        _id = self.details_list.item(self.details_list.focus(), 'values')[0]
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, _id)

    def exit(self):
        self.frame.destroy()
        admin_menu_page(self.root)


class stu_info_query_admin_page(query_page):
    def __init__(self, master):
        super(stu_info_query_admin_page, self).__init__(master)
        self.root.geometry('550x400')
        self.root.title('学生信息查询')

    def get_area(self):
        return ('学号', '姓名', '性别', '班级', '年龄')

    def get_sql(self):
        return 'select * from xsxx'

    def search_double_click(self, event):
        _id = self.details_list.item(self.details_list.focus(), 'values')[0]
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, _id)

    def exit(self):
        self.frame.destroy()
        admin_menu_page(self.root)


class stu_mtnc_page(query_page):
    def __init__(self, master):
        self.area = self.get_area()
        self.sql = self.get_sql()
        self.data = self.get_data()

        self.root = master
        self.root.title('学生成绩维护')
        self.root.geometry('500x500')

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        spacey(self.frame, 10)

        mode_sub_frame = tk.Frame(self.frame)
        mode_sub_frame.pack()

        help = tk.Button(
            mode_sub_frame,
            text='帮助',
            command=self.help)
        help.pack(side='left')

        spacex(mode_sub_frame, 10)

        exit = tk.Button(
            mode_sub_frame,
            text='退出',
            command=self.exit)
        exit.pack(side='left')

        spacex(mode_sub_frame, 10)

        query_button = tk.Button(
            mode_sub_frame,
            text='查询',
            command=self.search)
        query_button.pack(side='left')

        spacex(mode_sub_frame, 10)

        reset_button = tk.Button(
            mode_sub_frame,
            text='复位',
            command=self.load)
        reset_button.pack(side='left')

        spacex(mode_sub_frame, 10)

        add_button = tk.Button(
            mode_sub_frame,
            text='增加',
            command=self.add)
        add_button.pack(side='left')

        spacex(mode_sub_frame, 10)

        edit_button = tk.Button(
            mode_sub_frame,
            text='修改',
            command=self.edit)
        edit_button.pack(side='left')

        spacex(mode_sub_frame, 10)

        delete_button = tk.Button(
            mode_sub_frame,
            text='删除',
            command=self.delete)
        delete_button.pack(side='left')

    def exit(self):
        self.frame.destroy()
        admin_menu_page(self.root)


class stu_pfmn_mtnc_page(stu_mtnc_page):
    def __init__(self, master):
        super(stu_pfmn_mtnc_page, self).__init__(master)
        self.root.title('学生成绩维护')
        self.root.geometry('450x400')

        spacey(self.frame, 10)

        entry_frame, self.search_entry, self.cname_entry, self.grade_entry = self.entry_frame()
        entry_frame.pack()

        spacey(self.frame, 10)

        self.details_list = self.get_list()
        self.details_list.pack()

        self.load()

    def entry_frame(self):
        frame = tk.Frame(self.frame)
        frame.pack()

        sno_label = tk.Label(
            frame,
            text='学号')
        sno_label.pack(side='left')

        sno_entry = tk.Entry(
            frame,
            width=10)
        sno_entry.pack(side='left')

        spacex(frame, 10)

        cname_label = tk.Label(
            frame,
            text='课程名')
        cname_label.pack(side='left')

        cname_entry = tk.Entry(
            frame,
            width=10)
        cname_entry.pack(side='left')

        spacex(frame, 10)

        grade_label = tk.Label(
            frame,
            text='成绩')
        grade_label.pack(side='left')

        grade_entry = tk.Entry(
            frame,
            width=5)
        grade_entry.pack(side='left')

        return frame, sno_entry, cname_entry, grade_entry

    def get_area(self):
        return ('学号', '课程名', '成绩')

    def get_sql(self):
        return 'select * from xsdkcj2'

    def search(self):
        _id = self.search_entry.get()
        _cname = self.cname_entry.get()
        if len(_cname) == 0:
            self.search2()
        else:
            self.search1()

    def search1(self):
        _id = self.search_entry.get()
        _cname = self.cname_entry.get()
        self.load()
        if isnum(_id) == 1:
            result = sql(self.sql+' where sno=%s' % _id)
            if _id not in [item[0] for item in result]:
                message_box('学号不存在，请重新输入！')
            elif _cname not in [item[1] for item in result]:
                message_box('课程不存在，请重新输入！')
            else:
                t = []
                for i in result:
                    if i[0] == _id and i[1] == _cname:
                        t = i
                self.clear()
                self.details_list.insert('', 'end', values=t)
        elif _id == '':
            message_box('学号不能为空!')
        else:
            message_box('请输入数字！')

    def search2(self):
        _id = self.search_entry.get()
        self.load()
        if isnum(_id) == 1:
            result = sql(self.sql+' where sno=%s' % _id)
            if _id not in [item[0] for item in result]:
                message_box('学号不存在，请重新输入！')
            else:
                self.clear()
                for item in result:
                    self.details_list.insert('', 'end', values=item)
        elif _id == '':
            message_box('学号不能为空!')
        else:
            message_box('请输入数字！')

    def search_double_click(self, event):
        _id = self.details_list.item(self.details_list.focus(), 'values')[0]
        _cname = self.details_list.item(self.details_list.focus(), 'values')[1]
        _grade = self.details_list.item(self.details_list.focus(), 'values')[2]
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, _id)
        self.cname_entry.delete(0, 'end')
        self.cname_entry.insert(0, _cname)
        self.grade_entry.delete(0, 'end')
        self.grade_entry.insert(0, _grade)
        self.search2()

    def judge(self):
        _id = self.search_entry.get()
        _cname = self.cname_entry.get()
        _grade = self.grade_entry.get()
        if _id == '':
            message_box('学号不能为空！')
            return 0
        elif not _id.isdigit():
            message_box('学号请输入数字！')
            return 0
        elif _cname == '':
            message_box('课程名不能为空！')
            return 0
        elif _grade == '':
            message_box('成绩不能为空！')
            return 0
        elif not isnum(_grade):
            message_box('成绩必须是数字！')
            return 0
        elif isnum(_grade) == 2:
            message_box('成绩必须为0-100内的整数！')
            return 0
        elif not 0 <= int(_grade) <= 100:
            message_box('成绩范围为0-100！')
            return 0
        else:
            return 1

    def add(self):
        _id = self.search_entry.get()
        _cname = self.cname_entry.get()
        _grade = self.grade_entry.get()
        if self.judge():
            _cno = sql("select cno from kc where cname='%s'" % _cname)
            if len(_cno) == 0:
                message_box('课程不存在，请重新输入！')
            else:
                _cno = _cno[0][0]
                try:
                    sql("insert into xxxx values('%s','%s',%s)" %
                        (_id, _cno, _grade))
                except Exception as e:
                    print(str(e))
                    if 'duplicate key' in str(e):
                        message_box('该学生的课程成绩已存在，请尝试编辑操作！')
                    elif 'cno' in str(e):
                        message_box('课程不存在，请重新输入！')
                self.data = self.get_data()
                self.search()

    def edit(self):
        _id = self.search_entry.get()
        _cname = self.cname_entry.get()
        _grade = self.grade_entry.get()
        if self.judge():
            if len(sql("select sno from xsxx where sno='%s'" % _id)) == 0:
                message_box('学号不存在，请重新输入！')
            else:
                _cno = sql("select cno from kc where cname='%s'" % _cname)
                if len(_cno) == 0:
                    message_box('课程不存在，请重新输入！')
                else:
                    _cno = _cno[0][0]
                    if len(sql("select * from xxxx where sno='%s' and cno='%s'" % (_id, _cno))) == 0:
                        message_box('该学生的课程记录不存在，请尝试增加！')
                    else:
                        sql("update xxxx set grade=%s where sno='%s' and cno='%s'" % (
                            _grade, _id, _cno))
                        self.data = self.get_data()
                        self.search1()

    def delete(self):
        _id = self.search_entry.get()
        _cname = self.cname_entry.get()
        if self.judge():
            if len(sql("select sno from xsxx where sno='%s'" % _id)) == 0:
                message_box('学号不存在，请重新输入！')
            else:
                _cno = sql("select cno from kc where cname='%s'" % _cname)
                if len(_cno) == 0:
                    message_box('课程不存在，请重新输入！')
                else:
                    _cno = _cno[0][0]
                    if len(sql("select * from xxxx where sno='%s' and cno='%s'" % (_id, _cno))) == 0:
                        message_box('该学生的课程记录不存在')
                    else:
                        sql("delete from xxxx where sno='%s' and cno='%s'" %
                            (_id, _cno))
                        self.data = self.get_data()
                        self.search2()


class stu_rcd_mtnc_page(stu_mtnc_page):
    def __init__(self, master):
        super(stu_rcd_mtnc_page, self).__init__(master)
        self.root.geometry('590x400')
        self.root.title('学生信息维护')

        spacey(self.frame, 10)

        entry_frame, self.search_entry, self.sname_entry, self.sex_combobox, self.class_entry, self.age_entry = self.entry_frame()
        entry_frame.pack()

        spacey(self.frame, 10)

        self.details_list = self.get_list()
        self.details_list.pack()

        self.load()

    def get_sql(self):
        return 'select * from xsxx'

    def get_area(self):
        return ('学号', '姓名', '性别', '班级', '年龄')

    def search(self):
        _id = self.search_entry.get()
        self.load()
        if isnum(_id) == 1:
            result = sql(self.sql+' where sno=%s' % _id)
            if _id not in [item[0] for item in result]:
                message_box('学号不存在，请重新输入！')
            else:
                t = []
                for i in self.data:
                    if i[0] == _id:
                        t = i
                self.clear()
                for item in result:
                    self.details_list.insert('', 'end', values=item)

                _sname = t[1]
                _sex = t[2]
                _class = t[3]
                _age = t[4]

                self.sname_entry.delete(0, 'end')
                self.sname_entry.insert(0, _sname)

                if _sex == '男':
                    self.sex_combobox.current(0)
                else:
                    self.sex_combobox.current(1)

                self.class_entry.delete(0, 'end')
                self.class_entry.insert(0, _class)

                self.age_entry.delete(0, 'end')
                self.age_entry.insert(0, _age)
        elif _id == '':
            message_box('学号不能为空!')
        else:
            message_box('请输入数字！')

    def entry_frame(self):
        frame = tk.Frame(self.frame)
        frame.pack()

        sno_label = tk.Label(
            frame,
            text='学号')
        sno_label.pack(side='left')

        sno_entry = tk.Entry(
            frame,
            width=10)
        sno_entry.pack(side='left')

        spacex(frame, 10)

        sname_label = tk.Label(
            frame,
            text='姓名')
        sname_label.pack(side='left')

        sname_entry = tk.Entry(
            frame,
            width=5)
        sname_entry.pack(side='left')

        spacex(frame, 10)

        sex_label = tk.Label(
            frame,
            text='性别')
        sex_label.pack(side='left')

        sex_combobox = ttk.Combobox(
            frame,
            width=5)
        sex_combobox['value'] = ('男', '女')
        sex_combobox.pack(side='left')

        spacex(frame, 10)

        class_label = tk.Label(
            frame,
            text='班级')
        class_label.pack(side='left')

        class_entry = tk.Entry(
            frame,
            width=5)
        class_entry.pack(side='left')

        spacex(frame, 10)

        age_label = tk.Label(
            frame,
            text='年龄')
        age_label.pack(side='left')

        age_entry = tk.Entry(
            frame,
            width=5)
        age_entry.pack(side='left')

        return frame, sno_entry, sname_entry, sex_combobox, class_entry, age_entry

    def judge(self):
        _sname = self.sname_entry.get()
        _sex = self.sex_combobox.get()
        _class = self.class_entry.get()
        _age = self.age_entry.get()
        if _sname == '':
            message_box('姓名不能为空！')
            return 0
        elif _sex == '':
            message_box('请选择性别！')
            return 0
        elif _class == '':
            message_box('请输入班级')
            return 0
        elif isnum(_class) != 1:
            message_box('请输入正确的班级')
            return 0
        elif _age == '':
            message_box('请输入年龄！')
            return 0
        elif isnum(_age) == 0:
            message_box('年龄请输入数字！')
            return 0
        elif isnum(_age) == 2:
            message_box('年龄请输入整数！')
            return 0
        else:
            return 1

    def add(self):
        _id = self.search_entry.get()
        _sname = self.sname_entry.get()
        _sex = self.sex_combobox.get()
        _class = self.class_entry.get()
        _age = self.age_entry.get()
        if self.judge():
            try:
                sql("insert into xsxx values('%s','%s','%s',%s,%s)" %
                    (_id, _sname, _sex, _class, _age))
            except Exception:
                message_box('学号已存在，请尝试修改操作！')
            self.data = self.get_data()
            self.search()

    def edit(self):
        _id = self.search_entry.get()
        _sname = self.sname_entry.get()
        _sex = self.sex_combobox.get()
        _class = self.class_entry.get()
        _age = self.age_entry.get()
        self.search()
        if self.judge():
            sql("update xsxx set sname='%s',sex='%s',class=%s,age=%s where sno='%s'" % (
                _sname, _sex, _class, _age, _id))
            self.data = self.get_data()
            self.search()

    def delete(self):
        _id = self.search_entry.get()
        self.search()
        if self.judge():
            sql("delete from xsxx where sno='%s'" % _id)
            self.data = self.get_data()
            self.load()


class admin_menu_page:
    def __init__(self, master):
        self.root = master
        self.root.title('管理员操作菜单')
        self.root.geometry('200x210')

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        spacey(self.frame, 10)

        top_sub_frame = tk.Frame(self.frame)
        top_sub_frame.pack()

        help = tk.Button(
            top_sub_frame,
            text='帮助',
            command=self.help)
        help.pack(side='left')

        spacex(top_sub_frame, 10)

        exit = tk.Button(
            top_sub_frame,
            text='退出',
            command=self.exit)
        exit.pack(side='right')

        spacey(self.frame, 10)

        bottom_sub_frame = tk.Frame(self.frame)
        bottom_sub_frame.pack()

        course_details = tk.Button(
            bottom_sub_frame,
            text='开课情况查询',
            command=self.course_details)
        course_details.pack()

        spacey(bottom_sub_frame, 10)

        grade_query = tk.Button(
            bottom_sub_frame,
            text='学生成绩查询',
            command=self.grade_query)
        grade_query.pack()

        spacey(bottom_sub_frame, 10)

        stu_info_query = tk.Button(
            bottom_sub_frame,
            text='学生信息查询',
            command=self.stu_info_query)
        stu_info_query.pack()

        spacey(bottom_sub_frame, 10)

        stu_pfmn_mtnc = tk.Button(
            bottom_sub_frame,
            text='学生成绩维护',
            command=self.stu_pfmn_mtnc)
        stu_pfmn_mtnc.pack()

        spacey(bottom_sub_frame, 10)

        stu_rcd_mtnc = tk.Button(
            bottom_sub_frame,
            text='学生记录维护',
            command=self.stu_rcd_mtnc)
        stu_rcd_mtnc.pack()

        spacey(self.frame, 10)

    def help(self):
        help_page()

    def exit(self):
        self.frame.destroy()
        mode_choosing_page(self.root)

    def course_details(self):
        self.frame.destroy()
        course_details_admin_page(self.root)

    def grade_query(self):
        self.frame.destroy()
        grade_query_admin_page(self.root)

    def stu_info_query(self):
        self.frame.destroy()
        stu_info_query_admin_page(self.root)

    def stu_pfmn_mtnc(self):
        self.frame.destroy()
        stu_pfmn_mtnc_page(self.root)

    def stu_rcd_mtnc(self):
        self.frame.destroy()
        stu_rcd_mtnc_page(self.root)


class admin_login_page:
    def __init__(self, master):
        self.root = master
        self.root.title('管理员登录')
        self.root.geometry('200x110')

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        spacey(self.frame, 10)

        top_sub_frame = tk.Frame(self.frame)
        top_sub_frame.pack()

        help = tk.Button(
            top_sub_frame,
            text='帮助',
            command=self.help)
        help.pack(side='left')

        spacex(top_sub_frame, 10, side='left')

        exit = tk.Button(
            top_sub_frame,
            text='退出',
            command=self.exit)
        exit.pack(side='left')

        spacey(self.frame, 10)

        password_sub_frame = tk.Frame(self.frame)
        password_sub_frame.pack()

        student_pwd = tk.Label(
            password_sub_frame,
            text='密码')
        student_pwd.pack(side='left')

        spacex(password_sub_frame, 10)

        self.pwd_entry = tk.Entry(
            password_sub_frame,
            show='*',
            width=10)
        self.pwd_entry.pack(side='left')

        spacey(self.frame, 10)

        confirm = tk.Button(
            self.frame,
            text='登录',
            command=self.confirm)
        confirm.pack()

        spacey(self.frame, 10)

    def confirm(self):
        _pwd = self.pwd_entry.get()
        global pwd_admin
        if _pwd == pwd_admin:
            self.frame.destroy()
            admin_menu_page(self.root)
        else:
            message_box('密码错误')
            self.pwd_entry.delete(0, 'end')

    def help(self):
        help_page()

    def exit(self):
        self.frame.destroy()
        mode_choosing_page(self.root)


class mode_choosing_page():
    def __init__(self, master):
        self.root = master
        self.root.title('登录')
        self.root.geometry('200x110')

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        spacey(self.frame, 10)

        title = tk.Label(
            self.frame,
            text='登录模式')
        title.pack()

        spacey(self.frame, 10)

        student = tk.Button(
            self.frame,
            text='学生',
            command=self.student_mode)
        student.pack()

        spacey(self.frame, 10)

        admin = tk.Button(
            self.frame,
            text='管理员',
            command=self.admin_mode)
        admin.pack()

        spacey(self.frame, 10)

    def student_mode(self):
        self.frame.destroy()
        student_menu_page(self.root)

    def admin_mode(self):
        self.frame.destroy()
        admin_login_page(self.root)


root = tk.Tk()
root.resizable(0, 0)
sw = root.winfo_screenwidth()//2
sh = root.winfo_screenheight()//2
root.geometry('+{}+{}'.format(sw-270, sh-210))
mode_choosing_page(root)
root.mainloop()
