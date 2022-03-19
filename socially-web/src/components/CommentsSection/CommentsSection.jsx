import { useState } from "react";
import PostList from "../post-list/PostList";
import PostForm from "../PostForm/PostForm";

const CommentsSection = ({ parentId, anyComments, userId, userIsStaff }) => {
  const commentsUrl = `http://localhost:8000/api/v1/posts/${parentId}/comments/`;
  const isLoggedIn = userId === "None" ? false : true;

  const [createdComment, setCreatedComment] = useState(null);

  return (
    <div>
      {isLoggedIn && (
        <PostForm
          parentPostId={parentId}
          isReply={true}
          newPostCallback={(newComment) => setCreatedComment(newComment)}
        />
      )}
      {(anyComments || createdComment !== null) && (
        <div className="comments my-4">
          <h2>Comments</h2>
          <div className="comments-content">
            <PostList
              newestPost={createdComment}
              sourceUrl={commentsUrl}
              userId={userId}
              userIsStaff={userIsStaff}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default CommentsSection;
