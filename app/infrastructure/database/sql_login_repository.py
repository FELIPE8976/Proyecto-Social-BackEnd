import psycopg2
import uuid
from app.common.config import Config
from app.domain.entities.userLogin import UserLogin
from app.domain.repositories.login_repository import LoginRepository


class SqlLoginRepository(LoginRepository):

    def get_db_connection(self):
        return psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASS,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )

    def find_by_personal_id(self, personal_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM login.user_login WHERE personal_id = %s', (personal_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return UserLogin(
                login_id=user_data[1],
                personal_id=user_data[3],
                password=user_data[2],
                username=user_data[0],
            )
        return None

    def create_user(self, user):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT status_id FROM "user"."status" WHERE status_name = %s', ("active",))
            status_id = cursor.fetchone()
            query = 'INSERT INTO "user"."foundation_worker" (worker_id, name, personal_id, phone, position, email, status_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            values = (str(user.worker_id), user.name, user.personal_id, user.phone, user.position, user.email, str(status_id[0]))
            cursor.execute(query, values)
            query2 = 'INSERT INTO "login"."user_login" (login_id, personal_id, password, username) VALUES (%s, %s, %s, %s)'
            values2 = (str(user.login_id), user.personal_id, user.password, user.username)
            cursor.execute(query2, values2)
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
        return user

    def get_name_by_personal_id(self, personal_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM login.user_login WHERE personal_id = %s', (personal_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return user_data
        return None

