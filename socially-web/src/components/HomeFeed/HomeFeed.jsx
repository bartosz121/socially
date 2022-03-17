import PostList from "../post-list/PostList";

const HomeFeed = ({ userId, userIsStaff }) => {
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
      endMessage={endMessage}
      userId={userId}
      userIsStaff={userIsStaff}
    />
  );
};

export default HomeFeed;
