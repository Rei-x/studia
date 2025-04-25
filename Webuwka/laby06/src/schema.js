import { createSchema } from "graphql-yoga";
import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { userOperations, todoOperations } from "./database.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const typeDefs = readFileSync(join(__dirname, "schema.graphql"), "utf8");

const resolvers = {
  Query: {
    users: () => {
      return userOperations.getAllUsers();
    },
    user: (_, args) => {
      return userOperations.getUserById(args.id);
    },
    todos: () => {
      return todoOperations.getAllTodos();
    },
    todo: (_, args) => {
      return todoOperations.getTodoById(args.id);
    },
  },
  User: {
    todos: (parent) => {
      console.log(parent);
      return userOperations.getUserTodos(parent.id);
    },
  },
  ToDoItem: {
    user: (parent) => {
      return userOperations.getUserById(parent.user_id);
    },
  },
  Mutation: {
    createUser: (_, { name, email, login }) => {
      return userOperations.createUser(name, email, login);
    },
    updateUser: (_, { id, name, email, login }) => {
      return userOperations.updateUser(id, name, email, login);
    },
    deleteUser: (_, { id }) => {
      return userOperations.deleteUser(id);
    },

    createTodo: (_, { title, completed, userId }) => {
      return todoOperations.createTodo(title, completed, userId);
    },
    updateTodo: (_, { id, title, completed, userId }) => {
      return todoOperations.updateTodo(id, title, completed, userId);
    },
    deleteTodo: (_, { id }) => {
      return todoOperations.deleteTodo(id);
    },
  },
};

export const schema = createSchema({
  typeDefs,
  resolvers,
});
