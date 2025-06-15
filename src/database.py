import ydb
from config import YD_ENDPOINT, YD_PATH

class Database:
    def __init__(self):
        """Инициализация подключения к YDB"""
        self.driver = ydb.Driver(
            endpoint=YD_ENDPOINT,
            database=YD_PATH
        )
        self.driver.wait(timeout=5)
        self.session = self.driver.table_client.session().create()

    def __del__(self):
        """Закрытие подключения к YDB"""
        if hasattr(self, 'driver'):
            self.driver.stop()

    def get_user_state(self, user_id: int) -> dict:
        """Получение состояния пользователя"""
        try:
            result = self.session.transaction().execute(
                f"""
                SELECT * FROM user_states
                WHERE user_id = {user_id}
                """,
                commit_tx=True
            )
            return result.rows[0] if result.rows else {}
        except Exception as e:
            print(f"Error getting user state: {str(e)}")
            return {}

    def set_user_state(self, user_id: int, state: dict) -> bool:
        """Установка состояния пользователя"""
        try:
            self.session.transaction().execute(
                f"""
                UPSERT INTO user_states (user_id, state)
                VALUES ({user_id}, '{state}')
                """,
                commit_tx=True
            )
            return True
        except Exception as e:
            print(f"Error setting user state: {str(e)}")
            return False

    def clear_user_state(self, user_id: int) -> bool:
        """Очистка состояния пользователя"""
        try:
            self.session.transaction().execute(
                f"""
                DELETE FROM user_states
                WHERE user_id = {user_id}
                """,
                commit_tx=True
            )
            return True
        except Exception as e:
            print(f"Error clearing user state: {str(e)}")
            return False

    def get_user_role(self, user_id: int) -> str:
        """Получение роли пользователя"""
        try:
            result = self.session.transaction().execute(
                f"""
                SELECT role FROM user_roles
                WHERE user_id = {user_id}
                """,
                commit_tx=True
            )
            return result.rows[0]['role'] if result.rows else None
        except Exception as e:
            print(f"Error getting user role: {str(e)}")
            return None

    def set_user_role(self, user_id: int, role: str) -> bool:
        """Установка роли пользователя"""
        try:
            self.session.transaction().execute(
                f"""
                UPSERT INTO user_roles (user_id, role)
                VALUES ({user_id}, '{role}')
                """,
                commit_tx=True
            )
            return True
        except Exception as e:
            print(f"Error setting user role: {str(e)}")
            return False

    def check_user_permission(self, user_id: int, permission: str) -> bool:
        """Проверка прав пользователя"""
        try:
            role = self.get_user_role(user_id)
            if not role:
                return False

            # Проверяем права для роли
            if role == 'ADMIN':
                return True

            # Получаем список разрешений для роли
            result = self.session.transaction().execute(
                f"""
                SELECT permissions FROM role_permissions
                WHERE role = '{role}'
                """,
                commit_tx=True
            )
            
            if not result.rows:
                return False

            permissions = result.rows[0]['permissions']
            return permission in permissions
        except Exception as e:
            print(f"Error checking user permission: {str(e)}")
            return False 