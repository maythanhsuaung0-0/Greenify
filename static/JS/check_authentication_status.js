import React, { useState } from "react";
import axios from "axios";

function check_authentication_status() {
const App = () => {
  const [email, set_email] = useState("");
  const [password, set_password] = useState("");
  const [user, set_email] = useState();

  useEffect(() => {
    const loggedInUser = localStorage.getItem("user");
    if (loggedInUser) {
      const foundUser = JSON.parse(loggedInUser);
      setUser(foundUser);
    }
  }, []);

  // logout the user
  const handleLogout = () => {
    setUser({});
    set_email("");
    set_password("");
    localStorage.clear();
  };

  // login the user
  const handleSubmit = async e => {
    e.preventDefault();
    const user = { email, password };
    // send the username and password to the server
    const response = await axios.post(
      "http://127.0.0.1:5000/login",
      user
    );
    // set the state of the user
    setUser(response.data);
    // store the user in localStorage
    localStorage.setItem("user", JSON.stringify(response.data));
  };

  // if there's a user show the message below
  if (user) {
    return (
      <div>
        {user.name} is loggged in
        <button onClick={handleLogout}>logout</button>
      </div>
    );
  }
}

export default check_authentication_status;