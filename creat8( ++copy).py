import sqlite3
from itertools import chain, repeat # repeat عند الخطا في الادخال 
from threading import Event #  خاصة بعملية الانتظار 

print("\n""\n")
i=0
while i<200:
    print("\n""\n")
    print("   الرجاء اختيار العملية التي تريد اجراىها                       ")
    print("\n")
    print("                           ++++++++++++++++++++++++++++++++++++++")
    print("      لاضافة طالب اضغط على حرف       a                       ")
    print("    لحذف طالب اضغط على حرف        d                         ")
    print("     لتعديل معلومات طالب اضغط على حرف   u                        ")
    print("    لعرض معلومات طالب اضغط على الحرف   s                         ")
    print("                           +++++++++++++++++++++++++++++++++++++++")
    letters=["a","d","u","s"]
    print("\n")
    letters=input("                            Enter a letter:")
#  الاتصال بقاعدة البيانات
    conn = sqlite3.connect('school8888.db') 
    cur = conn.cursor()
# انشاء الجداول
    cur.execute('''CREATE TABLE IF NOT EXISTS students 
                (studentId INTEGER PRIMARY KEY,
                firstName TEXT not null,
                lastName TEXT not null, 
                age INTEGER not null, 
                grade TEXT not null,
                date INTEGER not null);''')
    cur.execute("DROP table if exists lessons")
    cur.execute('''CREATE TABLE IF NOT EXISTS lessons 
                (lessonId INTEGER PRIMARY KEY,
                lesson TEXT not null);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS registless(
                operaId  INTEGER PRIMARY KEY AUTOINCREMENT, 
                lessonId integer not null,
                studentId integer not null,
                foreign key (studentId) references students (studentId));''')

# نقوم باضافة الطالب مع التسجيل في الدروس المختارة
    if "a" in letters:
# ادخال رفم الطالب ولا بمكن ادخال الاحرف 
        prompts = chain(["Enter studentId: "], repeat("ليس رقما! حاول ثانية:    "))
        replies = map(input, prompts)
        studentId= next(filter(str.isdigit, replies))
# ادخال اسم الطالب ولا بمكن ادخال الارقام
        prompts = chain(["Enter firstName: "], repeat("ليست كلمة! حاول ثانية:    "))
        replies = map(input, prompts)
        firstName= next(filter(str.isalpha, replies))
# ادخال كنية الطالب ولا بمكن ادخال الارقام
        prompts = chain(["Enter lastName: "], repeat("ليست كلمة! حاول ثانية:    "))
        replies = map(input, prompts)
        lastName = next(filter(str.isalpha, replies))
# ادخال عمر الطالب ولا بمكن ادخال الاحرف
        prompts = chain(["Enter age: "], repeat("ليس رقما! حاول ثانية:     "))
        replies = map(input, prompts)
        age = next(filter(str.isdigit, replies))
# ادخال صف الطالب ولا بمكن ادخال الارقام 
        prompts = chain(["Enter the grade: "], repeat("ليست كلمة! حاول ثانية:    "))
        replies = map(input, prompts)
        grade = next(filter(str.isalpha, replies))
# ادخال التاريخ ولا بمكن ادخال الاحرف
        prompts = chain(["Enter date: "], repeat("ليس رقما! حاول ثانية:    "))
        replies = map(input, prompts)
        date = next(filter(str.isdigit, replies))
        try:
            with conn:
                cur.execute("INSERT INTO students (`studentId` , `firstName` , `lastName` , `age` , `grade` , `date`) VALUES (?, ?, ?, ?, ?, ?)",(studentId, firstName , lastName , age , grade , date))
        except sqlite3.IntegrityError:
            print("................Record Already Exists...........")
            break

        finally:
            print(".................tasks completed.................")

# ظهور ادخال الخط          
        print(cur.rowcount, "تم إدخال الخط .....................    ")

        cur.execute("INSERT INTO lessons (lessonId, lesson) VALUES (1, 'php')")
        cur.execute("INSERT INTO lessons (lessonId, lesson) VALUES (2, 'javascript')")
        cur.execute("INSERT INTO lessons (lessonId, lesson) VALUES (3, 'python')")
        cur.execute("INSERT INTO lessons (lessonId, lesson) VALUES (4, 'ruby')")

  #عدد الدروس المسجل فيها الطالب      
        print("الرجاء اختيار الدروس التي تريدها                         ")
        print("المكون php        اضغط على        1                      ")
        print("المكون javascript اضغط على        2                      ")
        print("المكون python     اضغط على        3                      ")
        print("المكون ruby       اضغط على        4                      ")


        number=int(input("كم من مكون تريد التسجيل فيه  :                    "))
        
        y=1
        while y<=number :
            lessonId=input("ادخل رقم المكون :             ")
            cur.execute("insert into registless ('lessonId', 'studentId') VALUES (?, ?)",(lessonId, studentId))
            y+=1
# عملية حفظ المعلومات
        conn.commit()
        print("")
        print("...................تمت العملية بنجاح....................... ")
        Event().wait(4)
# نقوم بحذف الطالب من الجدولين students and registless
    elif "d" in letters:

        prompts = chain(["Enter studentId: "], repeat("ليس رقما! حاول ثانية:           "))
        replies = map(input, prompts)
        studentId = next(filter(str.isdigit, replies))

        row=cur.execute("SELECT * from students WHERE studentId = ?",(studentId,)).fetchall()
        print(row)

        row = cur.execute("SELECT * from registless WHERE studentId = ?", (studentId,)).fetchall()
        print(row)
        Event().wait(5)
        print("\n""\n")
        reponse=  input(" تريد اتمام عملية الحذف ؟ [y/n]  :                   ")
        reponse= reponse.strip().lower()
        if reponse.startswith('y'):
            cur.execute("delete  FROM students WHERE studentId = ?", (studentId,))
            cur.execute("delete  FROM registless WHERE studentId = ?", (studentId,))
            conn.commit()
        elif reponse.startswith('n') or reponse =='':
            print("الى اللقاء")
        else:
            print("اجب ب 'y' ou 'n'")

        Event().wait(4)
        print("")
        print("...................تمت العملية بنجاح.................... ")
        Event().wait(4)
# نقوم بالتعديلات كلها او البعض منها
    elif "u" in letters:

        prompts = chain(["Enter studentId: "], repeat("ليس رقما! حاول ثانية:   "))
        replies = map(input, prompts)
        studentId = next(filter(str.isdigit, replies))

        row = cur.execute("SELECT * from students WHERE studentId = ?", (studentId,)).fetchall()
        print(row)
        print("\n")

        reponse = input(" تريد تغيير الاسم ؟ [y/n] :               ")
        reponse = reponse.strip().lower()
        if reponse.startswith('y'):
            prompts = chain(["Enter firstName: "], repeat("ليست كلمة! حاول ثانية:    "))
            replies = map(input, prompts)
            newfirstName = next(filter(str.isalpha, replies))

            cur.execute("UPDATE students set firstName= ? WHERE studentId=? ", (newfirstName, studentId))
            conn.commit()
        elif reponse.startswith('n') or reponse == '':
            print("ok")
        else:
            print("اجب ب 'y' ou 'n'")
        print("\n")

        reponse = input(" تريد تغيير الكنية ؟ [y/n] :                ")
        reponse = reponse.strip().lower()
        if reponse.startswith('y'):
            prompts = chain(["Enter lastName: "], repeat("ليست كلمة! حاول ثانية:    "))
            replies = map(input, prompts)
            newlastName = next(filter(str.isalpha, replies))

            cur.execute("UPDATE students set lastName= ? WHERE studentId=? ", (newlastName, studentId))
            conn.commit()
        elif reponse.startswith('n') or reponse == '':
            print("ok")
        else:
            print("اجب ب 'y' ou 'n'")
        print("\n")

        reponse = input(" تريد تغيير العمر ؟ [y/n] :                 ")
        reponse = reponse.strip().lower()
        if reponse.startswith('y'):
            prompts = chain(["Enter newage: "], repeat("ليس رقما! حاول ثانية:   "))
            replies = map(input, prompts)
            newage = next(filter(str.isdigit, replies))

            cur.execute("UPDATE students set age= ? WHERE studentId=? ", (newage, studentId))
            conn.commit()
        elif reponse.startswith('n') or reponse == '':
            print("ok")
        else:
            print("اجب ب 'y' ou 'n'")
        print("\n")

        reponse = input(" تريد تغيير الصف ؟ [y/n] :                   ")
        reponse = reponse.strip().lower()
        if reponse.startswith('y'):
            prompts = chain(["Enter the grade: "], repeat("ليست كلمة! حاول ثانية:    "))
            replies = map(input, prompts)
            newgrade = next(filter(str.isalpha, replies))

            cur.execute("UPDATE students set grade= ? WHERE studentId=? ", (newgrade, studentId))
            conn.commit()
        elif reponse.startswith('n') or reponse == '':
            print("ok")
        else:
            print("اجب ب 'y' ou 'n'")
        print("\n")

        reponse = input(" تريد تغيير التاريخ ؟ [y/n] :                 ")
        reponse = reponse.strip().lower()
        if reponse.startswith('y'):
            prompts = chain(["Enter newdate: "], repeat(" ليس رقما! حاول ثانية:    "))
            replies = map(input, prompts)
            newdate = next(filter(str.isdigit, replies))

            cur.execute("UPDATE students set date= ? WHERE studentId=? ", (newdate, studentId))
            conn.commit()
        elif reponse.startswith('n') or reponse == '':
            print("ok")
        else:
            print("اجب ب 'y' ou 'n'")

        print("")
        print("..................تمت العملية بنجاح .................  ")
        Event().wait(3)
# نقوم بالاستعلام        
    elif "s" in letters:

        prompts = chain(["Enter studentId: "], repeat("ليس رقما! حاول ثانية:     "))
        replies = map(input, prompts)
        studentId = next(filter(str.isdigit, replies))

        row=cur.execute("SELECT * from students WHERE studentId = ?",(studentId,)).fetchall()
        print(row)
            
        print("")
        print(" .................. تمت العملية بنجاح ......................  ")
        Event().wait(4)
        
    else:
        print("\n")
        print ("+++++++++++++++++  ERROR : خطا ++++++++++++++++++")
        Event().wait(4)

    conn.close()
i+=1   
