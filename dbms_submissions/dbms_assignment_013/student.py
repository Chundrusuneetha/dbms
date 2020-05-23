class DoesNotExist(Exception):
	pass

class MultipleObjectsReturned(Exception):
	pass

class InvalidField(Exception):
	pass

class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.student_id = None
        self.age = age
        self.score = score
    
    def __repr__(self):
        return "Student(student_id={0}, name={1}, age={2}, score={3})".format(
            self.student_id,
            self.name,
            self.age,
            self.score)
        
    @staticmethod
    def get(**kwargs):
        for key, value in kwargs.items():
            if key not in ("student_id", "name", "age", "score"):
                raise InvalidField
        sql_query = read_data(f"SELECT * FROM Student WHERE {key} = '{value}'")
        
        if len(sql_query) == 0:
            raise DoesNotExist
        elif len(sql_query) > 1:
            raise MultipleObjectsReturned
        else:
            ans = Student(sql_query[0][1], sql_query[0][2], sql_query[0][3])
            ans.student_id = sql_query[0][0]
            return ans
            
    def save(self):
        import sqlite3
        conn = sqlite3.connect("selected_students.sqlite3")
        c = conn.cursor() 
        c.execute("PRAGMA foreign_keys=on;")
        
        if self.student_id == None:
            c.execute(f"INSERT INTO Student (name, age, score) values ('{self.name}', {self.age}, {self.score})")        
            self.student_id = c.lastrowid
        
        elif c.execute(f"SELECT {self.student_id} not in (SELECT student_id FROM Student) FROM Student"):
            c.execute(f"REPLACE INTO Student (student_id, name, age, score) values ({self.student_id}, '{self.name}', {self.age}, {self.score})")        
            
        else:
            c.execute(f"UPDATE Student SET name = '{self.name}', age = {self.age}, score = {self.score} WHERE student_id = {self.student_id}")
        
        conn.commit() 
        conn.close()
        
    def delete(self):
        write_data(f"DELETE FROM Student WHERE student_id = {self.student_id}")
        
    @staticmethod    
    def filter(**kwargs):
        for key, value in kwargs.items():
            keys = key
            values = value
            
        x = keys.split("__")
        
        if x[0] not in ("student_id", "name", "age", "score"):
            raise InvalidField
            
        if keys in ("student_id", "name", "age", "score"):
            sql_query = read_data(f"SELECT * FROM Student WHERE {keys} = '{values}'")
        else:
                
            keys = keys.split("__")
                
            if keys[1] == "lt":
                sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} < '{values}'")
                    
            if keys[1] == "lte":
                sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} <= '{values}'")
                    
            if keys[1] == "gt":
                sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} > '{values}'")
                    
            if keys[1] == "gte":
                sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} >= '{values}'")
                    
            if keys[1] == "neq":
                sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} <> '{values}'")
                    
            if keys[1] == "in":
                values = tuple(values)
                sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} in {values}")
                
            if keys[1] == "contains":
                sql_query = read_data(f"SELECT * FROM Student WHERE {keys[0]} like '%{values}%'")
                
            
        if len(sql_query) == 0:
            return []
        else:
            x = []
                
            for i in sql_query:
                ans = Student(i[1], i[2], i[3])
                ans.student_id = i[0]
                x.append(ans)
            return x

def write_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("selected_students.sqlite3")
	crsr = connection.cursor() 
	crsr.execute("PRAGMA foreign_keys=on;") 
	crsr.execute(sql_query) 
	connection.commit() 
	connection.close()

def read_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("selected_students.sqlite3")
	crsr = connection.cursor()
	crsr.execute(sql_query)
	ans= crsr.fetchall()
	connection.close()
	return ans