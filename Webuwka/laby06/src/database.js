import Database from "better-sqlite3";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import axios from "axios";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const db = new Database(join(__dirname, "../data.sqlite"), {
  verbose: console.log,
});

function initializeDatabase() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      email TEXT NOT NULL,
      login TEXT NOT NULL
    )
  `);

  db.exec(`
    CREATE TABLE IF NOT EXISTS todos (
      id INTEGER PRIMARY KEY,
      title TEXT NOT NULL,
      completed BOOLEAN NOT NULL DEFAULT 0,
      user_id INTEGER,
      FOREIGN KEY (user_id) REFERENCES users (id)
    )
  `);

  const userCount = db.prepare("SELECT COUNT(*) as count FROM users").get();

  if (userCount.count === 0) {
    const initialUsers = [
      {
        id: 1,
        name: "Jan Konieczny",
        email: "jan.konieczny@wonet.pl",
        login: "jkonieczny",
      },
      {
        id: 2,
        name: "Anna Wesołowska",
        email: "anna.w@sad.gov.pl",
        login: "anna.wesolowska",
      },
      {
        id: 3,
        name: "Piotr Waleczny",
        email: "piotr.waleczny@gp.pl",
        login: "p.waleczny",
      },
    ];

    const insertUser = db.prepare(
      "INSERT INTO users (id, name, email, login) VALUES (?, ?, ?, ?)"
    );
    initialUsers.forEach((user) => {
      insertUser.run(user.id, user.name, user.email, user.login);
    });

    const initialTodos = [
      { id: 1, title: "Naprawić samochód", completed: 0, user_id: 3 },
      { id: 2, title: "Posprzątać garaż", completed: 1, user_id: 3 },
      { id: 3, title: "Napisać e-mail", completed: 0, user_id: 3 },
      { id: 4, title: "Odebrać buty", completed: 0, user_id: 2 },
      { id: 5, title: "Wysłać paczkę", completed: 1, user_id: 2 },
      { id: 6, title: "Zamówic kuriera", completed: 0, user_id: 3 },
    ];

    const insertTodo = db.prepare(
      "INSERT INTO todos (id, title, completed, user_id) VALUES (?, ?, ?, ?)"
    );
    initialTodos.forEach((todo) => {
      insertTodo.run(todo.id, todo.title, todo.completed, todo.user_id);
    });
  }
}

initializeDatabase();

export const userOperations = {
  getAllUsers: () => {
    return db.prepare("SELECT * FROM users").all();
  },

  getUserById: (id) => {
    return db.prepare("SELECT * FROM users WHERE id = ?").get(id);
  },

  createUser: (name, email, login) => {
    const stmt = db.prepare(
      "INSERT INTO users (name, email, login) VALUES (?, ?, ?) RETURNING *"
    );
    return stmt.get(name, email, login);
  },

  updateUser: (id, name, email, login) => {
    const stmt = db.prepare(
      "UPDATE users SET name = ?, email = ?, login = ? WHERE id = ? RETURNING *"
    );
    return stmt.get(name, email, login, id);
  },

  deleteUser: (id) => {
    const user = db.prepare("SELECT * FROM users WHERE id = ?").get(id);
    if (!user) return null;

    db.prepare("DELETE FROM todos WHERE user_id = ?").run(id);

    db.prepare("DELETE FROM users WHERE id = ?").run(id);
    return user;
  },

  getUserTodos: (userId) => {
    return db.prepare("SELECT * FROM todos WHERE user_id = ?").all(userId);
  },
};

export const todoOperations = {
  getAllTodos: () => {
    return db.prepare("SELECT * FROM todos").all();
  },

  getTodoById: (id) => {
    return db.prepare("SELECT * FROM todos WHERE id = ?").get(id);
  },

  createTodo: (title, completed, userId) => {
    if (userId) {
      const userExists = db
        .prepare("SELECT 1 FROM users WHERE id = ?")
        .get(userId);
      if (!userExists) {
        return null;
      }
    }

    const stmt = db.prepare(
      "INSERT INTO todos (title, completed, user_id) VALUES (?, ?, ?) RETURNING *"
    );
    return stmt.get(title, completed ? 1 : 0, userId);
  },

  updateTodo: (id, title, completed, userId) => {
    if (userId) {
      const userExists = db
        .prepare("SELECT 1 FROM users WHERE id = ?")
        .get(userId);
      if (!userExists) {
        return null;
      }
    }

    const stmt = db.prepare(
      "UPDATE todos SET title = ?, completed = ?, user_id = ? WHERE id = ? RETURNING *"
    );
    return stmt.get(title, completed ? 1 : 0, userId, id);
  },

  deleteTodo: (id) => {
    const todo = db.prepare("SELECT * FROM todos WHERE id = ?").get(id);
    if (!todo) return null;

    db.prepare("DELETE FROM todos WHERE id = ?").run(id);
    return todo;
  },
};

export async function fetchTodosFromAPI() {
  try {
    const response = await axios.get(
      "https://jsonplaceholder.typicode.com/todos"
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching todos from API:", error);
    throw error;
  }
}

export async function fetchUsersFromAPI() {
  try {
    const response = await axios.get(
      "https://jsonplaceholder.typicode.com/users"
    );
    return response.data.map(({ id, name, email, username }) => ({
      id,
      name,
      email,
      login: username,
    }));
  } catch (error) {
    console.error("Error fetching users from API:", error);
    throw error;
  }
}
