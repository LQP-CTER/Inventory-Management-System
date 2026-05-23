from sqlalchemy import text
import re

class SQLAlchemyCursor:
    def __init__(self, session):
        self.session = session
        self.last_result = None

    def execute(self, query, params=None):
        if params is None:
            params = []
        
        param_dict = {}
        # Convert ? to :p0, :p1, etc.
        def repl(match):
            idx = len(param_dict)
            p_name = f"p{idx}"
            param_dict[p_name] = params[idx]
            return f":{p_name}"
        
        converted_query = re.sub(r'\?', repl, query)
        
        if isinstance(params, dict):
            converted_query = query
            param_dict = params
            
        try:
            self.last_result = self.session.execute(text(converted_query), param_dict)
        except Exception as e:
            self.last_result = None
            raise e
            
        return self

    def fetchone(self):
        if self.last_result:
            row = self.last_result.fetchone()
            if row:
                return tuple(row)
        return None

    def fetchall(self):
        if self.last_result:
            return [tuple(row) for row in self.last_result.fetchall()]
        return []
        
    def fetchmany(self, size=1):
        if self.last_result:
            return [tuple(row) for row in self.last_result.fetchmany(size)]
        return []

    def close(self):
        pass

class SQLAlchemyConnection:
    def __init__(self, session):
        self.session = session
        
    def cursor(self):
        return SQLAlchemyCursor(self.session)
        
    def commit(self):
        self.session.commit()
        
    def close(self):
        self.session.close()

def get_connection(session):
    return SQLAlchemyConnection(session)
