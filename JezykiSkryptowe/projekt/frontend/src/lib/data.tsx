export const userData = [
  {
    id: 1,
    avatar: "/User1.png",
    messages: [],
    title: "Mr. Studendix",
  },
];

export type UserData = (typeof userData)[number];

export const loggedInUserData = {
  id: 5,
  avatar: "/LoggedInUser.jpg",
  name: "Bartosz Gotowski",
};

export type LoggedInUserData = typeof loggedInUserData;

export interface Message {
  id: number | string;
  avatar: string;
  name: string;
  message: string;
}

export interface User {
  id: number;
  avatar: string;
  messages: Message[];
  name: string;
}
