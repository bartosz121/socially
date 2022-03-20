import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import PostHead from "../PostHead/PostHead";
import PostBody from "../PostBody/PostBody";
import PostBottom from "../PostBottom/PostBottom";

import "./PostListItem.scss";

const PostListItem = ({ post, requestUserId, requestUserIsStaff }) => {
  const {
    id: postId,
    parent_post: parentPost,
    body,
    comment_count: commentCount,
    like_count: likeCount,
    url: postDetailUrl,
    picture_url: pictureUrl,
    post_author: postAuthor,
    created,
    updated,
    edit_url: editUrl,
  } = post;

  const userCanEdit =
    requestUserId === postAuthor.user_id || requestUserIsStaff;

  const [postVisible, setPostVisible] = useState(true);

  return (
    <AnimatePresence exitBeforeEnter={true} onExitComplete={() => null}>
      {postVisible && (
        <motion.div
          key={`post-${postId}`}
          initial={{ y: "20vh", opacity: 0 }}
          animate={{ y: "0", opacity: 1 }}
          exit={{ y: "-20vh", opacity: 0 }}
          transition={{ duration: 0.4 }}
        >
          <div className="post my-4 p-5 bg-light border rounded-3">
            <PostHead
              userCanEdit={userCanEdit}
              postId={postId}
              postAuthor={postAuthor}
              postDetailUrl={postDetailUrl}
              editUrl={editUrl}
              created={created}
              updated={updated}
              deleteCallback={() => setPostVisible(false)}
            />
            <PostBody
              body={body}
              pictureUrl={pictureUrl}
              parentData={parentPost}
            />
            <hr />
            <PostBottom
              requestUserId={requestUserId}
              postId={postId}
              postDetailUrl={postDetailUrl}
              postLikeCount={likeCount}
              postCommentCount={commentCount}
            />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default PostListItem;
