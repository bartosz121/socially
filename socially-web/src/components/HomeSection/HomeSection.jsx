import { useState } from "react";
import PostList from "../post-list/PostList";
import PostForm from "../PostForm/PostForm";

const HomeSection = ({ userId, userIsStaff }) => {
  const [createdPost, setCreatedPost] = useState(null);

  const isLoggedIn = userId === "None" ? false : true;
  const userFeedUrl = `http://localhost:8000/api/v1/users/${userId}/feed/`;

  const endMessage = (
    <div className="d-flex justify-content-center">
      <p>
        Check
        <span
          role="button"
          onClick={() => (window.location.pathname = "/explore")}
          className="mx-2 link-primary"
        >
          <strong>
            <u>Explore</u>
          </strong>
        </span>
        tab to see all posts
      </p>
    </div>
  );
  return (
    <div>
      {isLoggedIn && (
        <PostForm newPostCallback={(newPost) => setCreatedPost(newPost)} />
      )}
      <PostList
        newestPost={createdPost}
        sourceUrl={isLoggedIn && userFeedUrl}
        endMessage={endMessage}
        userId={userId}
        userIsStaff={userIsStaff}
      />
    </div>
  );
};

export default HomeSection;
