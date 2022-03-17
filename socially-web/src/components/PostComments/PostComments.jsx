import PostList from "../post-list/PostList";

const PostComments = ({ parentId, userId, userIsStaff }) => {
  const commentsUrl = `http://localhost:8000/api/v1/posts/${parentId}/comments/`;
  return (
    <div className="comments my-4">
      <h2>Comments</h2>
      <div className="comments-content">
        <PostList
          sourceUrl={commentsUrl}
          userId={userId}
          userIsStaff={userIsStaff}
        />
      </div>
    </div>
  );
};

export default PostComments;
