import axios from "axios";
import { useState, useEffect } from "react";

import { formatNumberToDisplay, copyTextToClipboard } from "../../utils";

import PostActionButton from "../post-action-button/PostActionButton";

const PostBottom = ({
  postId,
  postDetailUrl,
  postLikeCount,
  postCommentCount,
}) => {
  const csrfToken = getCookie("csrftoken");
  const [likeCount, setLikeCount] = useState(postLikeCount);
  const [userLiked, setUserLiked] = useState(false);

  useEffect(() => {
    axios
      .get(`/api/v1/posts/${postId}/is-liked/`)
      .then((res) => {
        setUserLiked(res.data.is_liked);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  const goToDetailPage = () => (window.location.href = postDetailUrl);

  const likePost = () => {
    const action = userLiked ? "dislike" : "like";
    axios
      .post(
        `/api/v1/posts/${postId}/like/`,
        {
          action: action,
        },
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
        }
      )
      .then((res) => {
        setLikeCount(res.data.like_count);
        setUserLiked(!userLiked);
      });
  };

  return (
    <div className="post-bottom user-select-none d-flex flex-row">
      <PostActionButton
        className="comments d-flex flex-row justify-content-center align-items-center bd-highlight"
        handleClick={goToDetailPage}
      >
        <i className="bi bi-chat"></i>
        <span className="p-2">
          {postCommentCount > 0 ? (
            formatNumberToDisplay(postCommentCount)
          ) : (
            <span>&nbsp;</span>
          )}
        </span>
      </PostActionButton>
      <PostActionButton
        className={`likes ${
          userLiked && "liked"
        } d-flex flex-row justify-content-center align-items-center bd-highlight`}
        handleClick={likePost}
      >
        <i className={`bi ${userLiked ? "bi-heart-fill" : "bi-heart"}`}></i>
        <span className="p-2">
          {likeCount > 0 ? (
            formatNumberToDisplay(likeCount)
          ) : (
            <span>&nbsp;</span>
          )}
        </span>
      </PostActionButton>
      <PostActionButton
        className="share d-flex flex-row justify-content-center align-items-center bd-highlight"
        title="Copy URL"
        handleClick={async () => {
          await copyTextToClipboard(postDetailUrl);
        }}
      >
        <i className="bi bi-box-arrow-up"></i>
      </PostActionButton>
    </div>
  );
};

export default PostBottom;