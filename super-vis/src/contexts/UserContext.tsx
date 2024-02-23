import React, { createContext } from "react";
import { UserData } from "../utils/backend";

const UserContext = createContext<UserData>({
  name: '',
  surname: '',
  patronymic: '',
  email: '',
  _id: '',
});

export default UserContext;