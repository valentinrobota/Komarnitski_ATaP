import streamlit as st
import sqlite3

# --- Ініціалізація бази даних ---
def init_db():
    conn = sqlite3.connect('rrr.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- Реєстрація користувача (для тесту) ---
def register_user(username, password):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        st.success(f"Користувач '{username}' зареєстрований!")
    except sqlite3.IntegrityError:
        st.warning("Цей користувач вже існує.")
    except Exception as e:
        st.error(f"Помилка при реєстрації: {e}")
    finally:
        conn.close()

# --- Вхід у систему ---
def login(username, password):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        st.error(f"Помилка при вході: {e}")
        return False
    finally:
        conn.close()

# --- Основний інтерфейс ---
def main():
    st.set_page_config(page_title="Сторінка входу", page_icon="🔐")
    st.title("🔐 Сторінка входу")

    st.markdown("Введіть ваші облікові дані:")

    username = st.text_input("Ім’я користувача")
    password = st.text_input("Пароль", type="password")

    if st.button("Увійти"):
        if login(username, password):
            st.success(f"Ласкаво просимо, {username}!")
        else:
            st.error("Неправильне ім’я або пароль.")

    st.markdown("---")
    st.markdown("### 📝 Зареєструвати нового користувача (для тесту)")
    new_user = st.text_input("Нове ім’я користувача")
    new_pass = st.text_input("Новий пароль", type="password")
    if st.button("Зареєструвати"):
        if new_user and new_pass:
            register_user(new_user, new_pass)
        else:
            st.warning("Заповніть обидва поля!")

if __name__ == "__main__":
    init_db()
    main()
