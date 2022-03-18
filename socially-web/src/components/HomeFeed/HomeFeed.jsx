import PostList from "../post-list/PostList";

const HomeFeed = ({ userId, userIsStaff }) => {
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
    <PostList
      sourceUrl={isLoggedIn && userFeedUrl}
      endMessage={endMessage}
      userId={userId}
      userIsStaff={userIsStaff}
    />
  );
};

export default HomeFeed;
