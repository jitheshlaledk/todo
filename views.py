from todosapp.model import users,todos
session={}
def signinrequired(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("u must login")
    return wrapper
def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user=[user for user in users if user["username"]==username and user["password"]==password]
    return user
class SignInView:
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            session["user"]=user[0]
            print(username,"sucessfully logged in")
        else:
            print("you entered invalid credentials , please enter valid credentials")

class TodoView:
    @signinrequired
    def get(self,*args,**kwargs):
        return todos
    #for adding a specific todos
    @signinrequired
    def post(self,*args,**kwargs):
        usreId=session["user"]["id"]
        kwargs["userId"]=usreId
        todos.append(kwargs)
        print("todo added")
        print(todos)
class MyTodoListView:     #todos of logged in user
    @signinrequired
    def get(self,*args,**kwargs):
        userId=session["user"]["id"]
        mytodos=[todo for todo in todos if todo["userId"]==userId]
        return mytodos
class TodoDetailsView:
    def gettodo(self,id):
        todo=[todo for todo in todos if todo["todoId"]==id]
        return todo
    @signinrequired
    def get(self,*args,**kwargs):
        todo_id=kwargs.get("todo_id")
        todo=self.gettodo(todo_id)
        return todo
    @signinrequired
    def delete(self,*args,**kwargs):
        todo_id=kwargs.get("todo_id")
        data=self.gettodo(todo_id)
        if data:
            todo=data[0]
            todos.remove(todo)
            print(len(todos))
    @signinrequired
    def put(self,*args,**kwargs):
        todo_id=kwargs.get("todo_id")
        instance=self.gettodo(todo_id)
        data=kwargs.get("data")
        if data:
            todo_obj=instance[0]
            todo_obj.update(data)
            print("post updated sucessfully")
            return todo_obj
@signinrequired
def logout(*args,**kwargs):
    session.pop("user")
    print("sucessfully logged out")
    print(session)



data={"task_name":"hello there"}
user=SignInView()
user.post(username="nikil",password="Password@123")
# logout()




data1=TodoView()
print(data1.get())
data1.post(todoId=9,
          task_name="new todod",
          completed=False)
d=TodoDetailsView()
print(d.get(todo_id=4))
d.delete(todo_id=2)
d.put(todo_id=5,data=data)
print(todos)


#view for fetching a specific todo

#update a to do
#delete a todo
#log out

