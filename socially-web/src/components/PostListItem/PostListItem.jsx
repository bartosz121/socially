import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import PostHead from "../PostHead/PostHead";
import PostBody from "../post-body/PostBody";
import PostBottom from "../PostBottom/PostBottom";

import "./PostListItem.scss";

const PostListItem = ({ post, userId, userIsStaff }) => {
  userId = parseInt(userId);
  userIsStaff = userIsStaff === "True" ? true : false;

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

  const userCanEdit = userId === postAuthor.id || userIsStaff;

  const [postVisible, setPostVisible] = useState(true);

  return (
    <AnimatePresence>
      {postVisible && (
        <motion.div
          key={`post-${postId}`}
          initial={{ y: "20vh", opacity: 0 }}
          animate={{ y: "0", opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.6 }}
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
              setPostVisible={setPostVisible}
            />
            <PostBody
              body={body}
              pictureUrl={pictureUrl}
              parentData={parentPost}
            />
            <hr />
            <PostBottom
              userId={userId}
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
