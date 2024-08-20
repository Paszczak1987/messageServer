from tools.password import hash_password, generate_salt
from database.sql_tools import execute_query
from datetime import datetime


class User:
    def __init__(self, username="", password=""):
        self._id = None
        self.username = username
        self._hashed_password = hash_password(password, generate_salt())
        
    def save(self):
        query = f"""
            INSERT INTO users(username, password) VALUES (
            '{self.username}',
            '{self._hashed_password}'
            ) RETURNING user_id;
        """
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
            WHERE user_id = {self._id};
        """
        execute_query(query)
        
    def remove(self):
        query = f"DELETE FROM users WHERE user_id = {self._id}"
        execute_query(query)
        
    def id(self):
        return self._id
    
    def get_password(self):
        return self._hashed_password
        
    def __str__(self):
        return f"{self.username} (id: {self._id})"
    
    def __repr__(self):
        return self.__str__()
        
    @classmethod
    def _create(cls, user_id, username, password):
        u = User(username)
        u._hashed_password = password
        u._id = user_id
        return u
        
    @classmethod
    def get_by_id(cls, user_id):
        query = f"SELECT * FROM users WHERE user_id = '{str(user_id)}';"
        result = execute_query(query)[0]
        return cls._create(result[0], result[1], result[2])
    
    @classmethod
    def get_by_name(cls, username):
        query = f"SELECT * FROM users WHERE username = '{username}'"
        result = execute_query(query)[0]
        return cls._create(result[0], result[1], result[2])
    
    @classmethod
    def get_all(cls):
        """
        :return: all users from data base
        """
        query = "SELECT * FROM users ORDER BY user_id ASC;"
        results = execute_query(query)
        return [cls._create(res[0], res[1], res[2]) for res in results]
    
    @classmethod
    def get_ids(cls):
        """
        :return: id list of all users from data base
        """
        query = "SELECT user_id FROM users;"
        results = execute_query(query)
        return [int(res[0]) for res in results]
    
    @classmethod
    def get_names(cls):
        query = "SELECT username FROM users;"
        results = execute_query(query)
        return [res[0] for res in results]
    
    @classmethod
    def get_user_name(cls, u_id):
        query = f"SELECT username FROM users WHERE user_id = {u_id};"
        return execute_query(query)[0][0]
    
class Message:
    def __init__(self, from_id=None, to_id=None, text=None):
        self._id = None
        self.from_id = from_id
        self.to_id = to_id
        self.from_username = User.get_user_name(from_id) if from_id else "N.N."
        self.to_username = User.get_user_name(to_id) if to_id else "N.N."
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
        who = self.to_username if self.get_as_sent else self.from_username
        part = f"{"Wysłane do:" if self.get_as_sent else "Otrzymane od:"} {who}"
        parts = [
            f"{time}",
            part,
            f"{self.text}",
            f"id: {self._id}"
        ]
        frame = "=" * (max([len(el) for el in parts]) + 2)
        return frame + "\n| " + "\n| ".join(parts) + "\n" + frame
    
    def __repr__(self):
        who = self.to_id if self.get_as_sent else self.from_id
        part = f"{"do:" if self.get_as_sent else "od:"}{who}"
        return f"id:{self._id} {part} : {self.text}"
    
    @classmethod
    def _create(cls, msg_data):
        m = Message(msg_data[1], msg_data[2], msg_data[3])
        m._id = msg_data[0]
        m.time = msg_data[4]
        return m
    
    @classmethod
    def _create_without_user(cls, msg_data):
        m = Message()
        m._id = msg_data[0]
        m.from_id = msg_data[1]
        m.to_id = msg_data[2]
        m.text = msg_data[3]
        m.time = msg_data[4]
        return m
    
    @classmethod
    def get_message(cls, m_id):
        query = f"""
           SELECT * FROM messages WHERE id = {m_id};
        """
        result = execute_query(query)
        return cls._create(result[0])
    
    @classmethod
    def get_raw_message(cls, m_id):
        query = f"""
           SELECT * FROM messages WHERE id = {m_id};
        """
        result = execute_query(query)
        return cls._create_without_user(result[0])
    
    @classmethod
    def get_all_to_user_msgs(cls, user_id, _from_user=False):
        query = f"""
            SELECT * FROM messages WHERE {"from_id" if _from_user else "to_id"} = {user_id};
        """
        result = execute_query(query)
        messages = [cls._create(m) for m in result]
        for m in messages:
            m.get_as_sent = _from_user
        return messages
    
    @classmethod
    def get_all_from_user_msgs(cls, user_id):
        return cls.get_all_to_user_msgs(user_id, _from_user=True)
    
    @classmethod
    def get_all_user_msgs(cls, user_id):
        received = cls.get_all_to_user_msgs(user_id)
        sent = cls.get_all_from_user_msgs(user_id)
        return received + sent
    
    @classmethod
    def user_msgs_count(cls, user_id):
        query = f"""
            SELECT id FROM messages WHERE from_id = {user_id} OR to_id = {user_id};
        """
        return len(execute_query(query))
        
        
        
if __name__ == '__main__':
    # msg = []
    # msg.append(Message.get_message_raw(13))
    # msg.append(Message.get_message_raw(14))
    # msg.append(Message.get_message_raw(15))
    #
    # for m in msg:
    #     m.remove()
    # print(User.get_user_name(50))
    msgs = Message.get_all_user_msgs(35)
    msgs_count = Message.user_msgs_count(35)
    print(msgs)
    # for msg in msgs:
    #     print(msg)
        
    pass

    