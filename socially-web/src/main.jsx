import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import PostList from "./components/post-list/PostList";

ReactDOM.render(
  <React.StrictMode>
    <PostList />
  </React.StrictMode>,
  document.getElementById("root")
);
