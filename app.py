#导入flask对象
from flask import Flask,render_template,request,redirect
#后面的模块是可以返回模块的
#使用flask对象创建一个app对象
#request对象可以拿到前段传递过来的所有数据
app = Flask(__name__)

students = [
    {'name':'张三','chinese':'65','math':'65','english':'65'},
    {'name':'李四','chinese':'65','math':'65','english':'65'},
    {'name':'王五','chinese':'65','math':'65','english':'65'},
    {'name':'赵六','chinese':'65','math':'65','english':'65'},
]

# @是装饰器的意思，就是路由，当启用APP对象的时候就可以根据地址去访问下面的函数，‘/’就是访问路径
# 可以有多个@，即通过逻辑设计返回不同地址
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
#写一些新的功能
@app.route('/login',methods=['POST','GET'])
def login():
    #登录的功能
    #全栈项目，前后端不分离
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #登陆成功之后连接数据库，校验账号密码
        print('从服务器接收到的数据',username,password)
        #如果是post请求，登陆成功之后应该跳转到admin管理页面，需要用到网页重定向
        return  redirect('/admin')
    return render_template('login.html')
@app.route('/admin')
def admin():
    return render_template('admin.html',students=students)
#新增学员信息
@app.route('/add', methods=['GET','POST'])
def add():
    if request.method =='POST':
        username=request.form.get('username')
        chinese = request.form.get('chinese')
        math = request.form.get('math')
        english = request.form.get('english')
        print('获取的学员信息',username,chinese,math,english)
        students.append({'name':username,'chinese':chinese,'math':math,'english':english})
        return redirect('/admin')
    return render_template('add.html')
#修改学员信息
@app.route('/delete')
def delete_student():
    #在后台需要拿到学员的标识，再进一步进行删除操作
    print(request.method)
    username=request.args.get('name') #得到操作对应的姓名信息
    #找到学员并删除信息，从列表中删除信息，再重定向到admin页面，就成功了
    for stu in students:
        if stu['name'] == username:
            students.remove(stu)
    return redirect('/admin')

@app.route('/change',methods=['POST','GET'])
#修改应该在一个新的页面中进行修改操作，然后拿到数据，拿到新的修改后的数据就要用post接收数据了，与新增数据同理
#如果是post则进行修改操作，如果是get则进行判断
#先显示学员原来的信息，在浏览器修改，提交到服务器保存
def change_student():
    username = request.args.get('name')  # 得到操作对应的姓名信息

    if request.method=='POST':
        username = request.form.get('username')
        chinese = request.form.get('chinese')
        math = request.form.get('math')
        english = request.form.get('english')
        for stu in students:
            if stu['name'] == username:
                stu['chinese'] = chinese
                stu['math'] = math
                stu['english'] = english

        return redirect('/admin')
    for stu in students:
        if stu['name'] == username:    #找到学员信息后，在新的页面中展示（渲染）学生的成绩数据
            return render_template('change.html', student=stu)


#定义好这个视图之后重启一下，就是左下框的绿圆箭头
#需要实现其他功能（例如退出、查看学生信息）等
if __name__ == '__main__':
    app.run()
