import psycopg2


class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="127.0.0.1",
            port="5432",
            database="example3",
            user="postgres",
            password="mustafa",
        )
        self.cur = self.conn.cursor()

        self.create_documents_table()
        self.create_users_table()

    def get_connection(self):
        return self.conn

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()

    def create_documents_table(self):
        create_documents_table_query = """
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            content TEXT,
            documentation_number TEXT,
            commits TEXT
        );
        """
        self.cur.execute(create_documents_table_query)
        self.conn.commit()

    def create_users_table(self):
        create_users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            permission TEXT
        );
        """
        self.cur.execute(create_users_table_query)
        self.conn.commit()

    def insert_document(self, content, documentation_number, commits):
        documentation_text = str(documentation_number)
        insert_query = """
        INSERT INTO documents (content, documentation_number, commits)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        try:
            self.cur.execute(insert_query, (content, documentation_text, commits))
            document_row = self.cur.fetchone()

            if document_row is not None and len(document_row) > 0:
                document_id = document_row[0]
                self.conn.commit()
                return document_id
            else:
                self.conn.rollback()
                print("Belge eklenirken bir hata oluştu.")
                return None
        except Exception as e:
            self.conn.rollback()
            print("Belge eklenirken bir hata oluştu:", e)
            return None

    def delete_document(self, document_id):
        delete_query = """
        DELETE FROM documents
        WHERE id = %s;
        """

        self.cur.execute(delete_query, (document_id,))
        if self.cur.rowcount > 0:
            self.conn.commit()
            print(f"Döküman ID: {document_id} silindi.")
        else:
            self.conn.rollback()
            print(f"Döküman ID: {document_id} bulunamadı.")

    def list_documents(self):
        select_query = """
        SELECT id, content, documentation_number, commits
        FROM documents;
        """

        self.cur.execute(select_query)
        documents = self.cur.fetchall()

        print("Dökümanlar:")
        for document in documents:
            print(
                f"ID: {document[0]}, İçerik: {document[1]}, Dökümantasyon No: {document[2]}, Commits: {document[3]}"
            )

    def update_document(self, document_id, new_content, new_commits):
        update_query = """
        UPDATE documents
        SET content = %s, commits = %s
        WHERE id = %s
        RETURNING id;
        """

        self.cur.execute(update_query, (new_content, new_commits, document_id))
        self.conn.commit()

    def insert_new_user(self, username, password, permission):
        insert_query = """
        INSERT INTO users (username, password, permission)
        VALUES (%s, %s, %s)
        RETURNING id;
        """

        try:
            self.cur.execute(insert_query, (username, password, permission))
            user_row = self.cur.fetchone()

            if user_row is not None:  # fetchone() sonucunu kontrol edin
                user_id = user_row[0]
                self.conn.commit()
                return user_id
            else:
                self.conn.rollback()
                print(
                    "Kullanıcı oluşturulurken bir hata oluştu: Kullanıcı ID alınamadı."
                )
                return None
        except Exception as e:
            self.conn.rollback()
            print("Kullanıcı oluşturulurken bir hata oluştu:", e)
            return None

    def delete_user(self, user_id):
        delete_query = """
        DELETE FROM users
        WHERE id = %s;
        """
        try:
            self.cur.execute(delete_query, (user_id,))
            if self.cur.rowcount > 0:
                self.conn.commit()
                print(f"Kullanıcı ID: {user_id} silindi.")
            else:
                self.conn.rollback()
                print(f"Kullanıcı ID: {user_id} bulunamadı.")
        except Exception as e:
            self.conn.rollback()
            print("Kullanıcı silinirken bir hata oluştu:", e)

    def list_users(self):
        select_query = """
        SELECT id, username, permission
        FROM users;
        """

        self.cur.execute(select_query)
        users = self.cur.fetchall()

        print("Kullanıcılar:")
        for user in users:
            print(f"ID: {user[0]}, Kullanıcı Adı: {user[1]}, İzin Seviyesi: {user[2]}")

    def __del__(self):
        self.close_connection()


if __name__ == "__main__":
    db_manager = DatabaseManager()
    # İşlemleri burada gerçekleştirin
