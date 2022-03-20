import { useState } from "react";
import PostList from "../PostList/PostList";
import PostForm from "../PostForm/PostForm";

const CommentsSection = ({
  parentId,
  anyComments,
  requestUserId,
  requestUserIsStaff,
}) => {
  const commentsUrl = `http://localhost:8000/api/v1/posts/${parentId}/comments/`;
  const isLoggedIn = isNaN(requestUserId) ? false : true;

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
              requestUserId={requestUserId}
              requestUserIsStaff={requestUserIsStaff}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default CommentsSection;
