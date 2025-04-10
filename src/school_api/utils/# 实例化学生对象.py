# 实例化学生对象
student = Student('202301001', '123456')

# 获取2024学年第二学期教材
result = student.textbook.get_textbooks(2024, 12)

# 获取当前学期教材
result = student.textbook.get_textbooks()

# 处理返回结果
if result['code'] == 1:
    books = result['data']
    for book in books:
        print(f"课程: {book['course_name']}")
        print(f"教材: {book['book_name']}")
        print(f"作者: {book['author']}")
        print(f"出版社: {book['publisher']}")
        print(f"价格: {book['price']}")
        print("-------------------")
else:
    print(f"获取失败: {result['msg']}")