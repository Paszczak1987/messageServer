from tools.password import hash_password, generate_salt
from database.sql_tools import execute_query
from datetime import datetime


class User:
    def __init__(self, username="", password=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, generate_salt())
        
    def save(self):
        query = f"""
            INSERT INTO users(username, password) VALUES (
            '{self.username}',
            '{self._hashed_password}'
            ) RETURNING user_id"""
        result = execute_query(query)
        self._id = result[0][0]
        
    def update(self, username=None, password=None):
        set_statement = ""
        hashed_pass = hash_password(password, generate_salt()) if password else None
        if username is not None and password is not None:
            set_statement += f"SET username = '{username}', password = '{hashed_pass}'"
        elif username is None and password is not None:
            set_statement += f"SET password = '{hashed_pass}'"
        elif username is not None and password is None:
            set_statement += f"SET username = '{username}'"
        else:
            return
        query = f"""
            UPDATE users
            {set_statement}
            WHERE user_id = {self._id}
        """
        execute_query(query)
        
    def remove(self):
        query = f"DELETE FROM users WHERE user_id = {self._id}"
        execute_query(query)
        
    def __str__(self):
        return f"{self.username} id: {self._id}"
    
    def __repr__(self):
        return self.__str__()
        
    @classmethod
    def _create(cls, user_id, username, password):
        u = User(username)
        u._hashed_password = password
        u._id = user_id
        return u
        
    @classmethod
    def get_user_by_id(cls, user_id):
        query = f"SELECT * FROM users WHERE user_id = '{str(user_id)}';"
        result = execute_query(query)[0]
        return cls._create(result[0], result[1], result[2])
    
    @classmethod
    def get_user_by_name(cls, username):
        query = f"SELECT * FROM users WHERE username = '{username}'"
        result = execute_query(query)[0]
        return cls._create(result[0], result[1], result[2])
    
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users ORDER BY user_id ASC;"
        results = execute_query(query)
        return [cls._create(res[0], res[1], res[2]) for res in results]
    
    @classmethod
    def get_ids(cls):
        query = "SELECT user_id FROM users;"
        results = execute_query(query)
        return [int(res[0]) for res in results]
    
    @classmethod
    def get_names(cls):
        query = "SELECT username FROM users;"
        results = execute_query(query)
        return [res[0] for res in results]
    
class Message:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.from_username = User.get_user_by_id(from_id).username
        self.to_id = to_id
        self.to_username = User.get_user_by_id(to_id).username
        self.text = text
        self.time = None
        self.get_as_sent = None
    
    def send(self):
        self.time = datetime.now()
        query = f"""
            INSERT INTO messages(from_id, to_id, message, creation_date) VALUES (
                {self.from_id},
                {self.to_id},
                '{self.text}',
                '{self.time}'
            ) RETURNING id;
        """
        result = execute_query(query)
        self._id = result[0][0]
        
    def remove(self):
        query = f"DELETE FROM messages WHERE id = {self._id};"
        execute_query(query)
        
    def __str__(self):
        time = self.time.strftime("%d/%m/%Y %H:%M:%S")
        part = f"Otrzymane od: {self.from_username}"
        if self.get_as_sent: part = f"Wysłane do: {self.to_username}"
        parts = [
            f"{time}",
            part,
            f"{self.text}",
            f"id: {self._id}"
        ]
        frame = "=" * (max([len(el) for el in parts]) + 2)
        return frame + "\n| " + "\n| ".join(parts) + "\n" + frame
    
      
    @classmethod
    def _create(cls, id, from_id, to_id, text, time):
        u = Message(from_id, to_id, text)
        u._id = id
        u.time = time
        return u
    
    @classmethod
    def _create_args(cls, msg_data):
        m = Message(msg_data[1], msg_data[2], msg_data[3])
        m._id = msg_data[0]
        m.time = msg_data[4]
        return m
    
    @classmethod
    def get_message(cls, id):
        query = f"""
           SELECT * FROM messages WHERE id = {id};
        """
        result = execute_query(query)
        return cls._create_args(result[0])
    
    @classmethod
    def get_all_to_user_msgs(cls, user_id):
        query = f"""
            SELECT * FROM messages WHERE to_id = {user_id};
        """
        result = execute_query(query)
        msgs = [cls._create_args(msg) for msg in result]
        for msg in msgs: msg.get_as_sent = False
        return msgs
    
    @classmethod
    def get_all_from_user_msgs(cls, user_id):
        query = f"""
            SELECT * FROM messages WHERE from_id = {user_id};
        """
        result = execute_query(query)
        msgs = [cls._create_args(msg) for msg in result]
        for msg in msgs:
            msg.get_as_sent = True
        return msgs
    
    @classmethod
    def get_all_user_msgs(cls, user_id):
        received = cls.get_all_to_user_msgs(user_id)
        sent = cls.get_all_from_user_msgs(user_id)
        return received + sent
        
        
if __name__ == '__main__':
    # user = User.get_user_by_name("Koles")
    # messages = Message.get_all_user_messages(user._id)
    # for msg in messages:
    #     print(msg)
    # u1 = User.get_user_by_id(22)
    # u2 = User.get_user_by_id(33)
    # txt = "Widziałem Cię niedawno na mieście."
    # m = Message(u1._id,u2._id, txt)
    # m.send()
    koles = User.get_user_by_name('Koles')
    # messages_sent = Message.get_all_from_user_msgs(koles._id)
    # messages_received = Message.get_all_to_user_msgs(koles._id)
    messages = Message.get_all_user_msgs(koles._id)
    # for msg in messages_sent:
    #     print(msg)
    # for msg in messages_received:
    #     print(msg)
    for msg in messages:
        print(msg)