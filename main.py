from time import sleep


class Books:
    def __init__(self, title, author, state=0):  # 初始化
        self.title = title
        self.author = author
        self.state = state

    def __str__(self):  # 打印书籍基本信息
        bookstatus = "未借阅"  # 初始默认未借阅状态，即state = 0
        if self.state == 1:
            bookstatus = "已借阅"
        return "书名: 《{0}》   作者: {1}   状态: {2}".format(self.title, self.author, bookstatus)


class BookManager:
    titles = []

    def __init__(self):  # 初始化现存书籍
        with open("booksData.txt", 'r', encoding='utf-8') as f:
            books = f.readlines()
            for book in books:
                book = book.split(",")  # 文本处理
                title = book[0]
                author = book[1]
                state = int(book[2])
                self.titles.append(Books(title, author, state))

    def Login(self):  # 用户登录，用于借阅时的身份核实
        datas = {}  # 定义字典，用于存放信息

        with open("user_data.txt", 'r', encoding='utf-8') as f:
            infos = f.readlines()  # 逐行读取文本信息
            for i in range(len(infos)):
                res = infos[i].split("；")
                info1 = res[0].split("：")[1]
                info2 = res[1].split("：")[1].replace("\n","")  # 采用切片去除换行符，小了小了，通用性差
                datas[info1] = info2
                print(datas)

            flag = False  # 设置标记值，判断是否进入密码输入状态
            for i in range(3):  # 用户名判断不超过三次
                username = input("Please enter your username: ")
                if username not in datas:
                    if i != 2:
                        print("Username does not exist. You only have %d chance!" % (2 - i))
                        print("")
                    else:
                        print("Sorry,this platform does not belong to you.")
                        return False
                else:
                    flag = True
                    break

            if flag:
                password = input("Please enter you password: ")
                while 1:  # 密码直到输入正确才结束循环
                    if password != datas[username]:
                        print("wrong password!")
                        password = input("Please enter you password: ")
                    else:
                        print("Successfully login!")
                        print("")
                        break
                return True

    def DisplayAllBooks(self):
        print("馆藏书籍收录及借阅情况".center(45, '-'))
        for book in self.titles:
            print(book)

    def BorrowBooks(self):
        flag = 0  # 设置一个标记值
        for j in range(3):
            print("")
            print("您需要借阅哪本书籍？")
            title = input("")
            for book in self.titles:  # 遍历所有书籍
                if book.title == title:  # 将现有书籍的名称和待借书籍名对比，相等则修改标记值以及借阅状态
                    if book.state == 0:  # 选择判断，如果该书没有借走，则借出；否则标记值变为2
                        flag = 1
                        book.state = 1
                    else:
                        flag = 2
            if flag == 1:
                print("借阅成功！")
                break
            elif flag == 0:
                if j != 2:
                    print("不好意思呀，没有您需要的书籍!")
                    print("请重新输入~")
                else:
                    print("目前本馆还没有收录这本书哦，您可以通过功能[1]查询已收录的书籍~~")
                    return 0
            else:
                print("啊呀呀，来晚了一步，这本书已经被其他人借走了哦")
                break

    def ReturnBooks(self):
        flag = 1  # 同样设置标记值，区分不存在书籍、已归还书籍、未归还书籍
        title = input("请输入归还的书籍: ")
        for book in self.titles:
            if book.title == title:
                if book.state == 1:
                    flag = 0
                    book.state = 0
                else:
                    flag = 2
        if flag == 0:
            print("该书已成功归还!")
        elif flag == 1:
            print("这本书我们还没有收录哦~")
        else:
            print("该书没有被借走哦~")

    def AddBooks(self):
        title = input("请输入书籍的名称: ")
        author = input("作者: ")
        book = Books(title, author)
        self.titles.append(book)
        print("书籍添加成功!")

    def Deletebooks(self):
        flag = 1
        title = input("请输入书籍的名称: ")
        for i in range(len(self.titles)):
            if title == self.titles[i].title:
                del self.titles[i]
                print("该书已成功删除!")
                flag = 0
                break

        if flag:
            print("本馆并没有这本书哦~")

    def Save(self):
        with open("booksData.txt", 'w', encoding='utf-8') as f:
            ls = []
            t = []
            for book in self.titles:
                title = book.title
                author = book.author
                state = book.state
                ls.append(title)
                ls.append(author)
                ls.append(str(state))
                t.append(ls)
                ls = []

            for i in range(len(t)):
                s = ",".join(t[i])  # 存储书籍信息用“,”连接
                if i == 0:
                    f.write(s)
                else:
                    s = '\n' + s  # 从第二行开始换行存储书籍信息
                    f.write(s)

    def menu(self):  # 用户菜单栏
        sleep(1)
        print("以下是我们提供的服务~~")
        sleep(1)
        while True:
            print("")
            print("[1]:查询书籍\n[2]:借阅书籍\n[3]:归还书籍\n[4]:添加书籍\n[5]:删除书籍\n[0]:退出系统\n")
            sleep(1)
            print("请输入您的选择: (0-5)")
            choice = eval(input())
            if choice == 1:
                self.DisplayAllBooks()
            elif choice == 2:
                self.BorrowBooks()
            elif choice == 3:
                self.ReturnBooks()
            elif choice == 4:
                self.AddBooks()
            elif choice == 5:
                self.Deletebooks()
            elif choice == 0:
                self.Save()
                print("感谢您的使用，祝您生活愉快！^-^")
                break
            else:
                print("您的输入有误，请重新输入!")


if __name__ == '__main__':
    print("欢迎光临图书管理体统！")
    print("请验证登陆信息".center(40, '*'))

    manager = BookManager()
    verification = manager.Login()
    if verification:
        manager.menu()
