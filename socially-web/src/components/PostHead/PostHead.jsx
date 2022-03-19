import axios from "axios";
import { formatDistanceToNow, format, compareAsc } from "date-fns";
import { getCookie } from "../../utils";
import { ButtonToolbar, ButtonGroup, Button } from "react-bootstrap";

const PostHead = ({
  userCanEdit,
  postId,
  postAuthor,
  editUrl,
  created,
  updated,
  deleteCallback,
}) => {
  const csrfToken = getCookie("csrftoken");

  const createdDate = new Date(Number(created));
  const updatedDate = new Date(Number(updated));

  const deletePost = () => {
    axios
      .delete(`/api/v1/posts/${postId}`, {
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
      .then((res) => {
        if (res.status === 204) {
          deleteCallback();
        }
      })
      .catch((err) => {
        console.error(err);
      });
  };

  return (
    <div className="post-head mb-2">
      <div className="author-picture">
        <a href={postAuthor.profile_url}>
          <img
            className="profile-picture-medium rounded"
            src={postAuthor.profile_picture}
            alt="profile picture"
          />
        </a>
      </div>
      <div className="post-info ms-2">
        <div className="post-author-username">
          <a href={postAuthor.profile_url}>
            <span className="pointer-hover-underline text-break">
              {postAuthor.username}
            </span>
          </a>
        </div>
        <div className="post-time text-muted">
          {compareAsc(updatedDate, createdDate) === 1 ? (
            <small
              className="updated"
              title={`Created: ${format(
                createdDate,
                "yyyy/MM/dd' 'HH:mm:ss.sss"
              )} | Updated: ${format(
                updatedDate,
                "yyyy/MM/dd' 'HH:mm:ss.sss"
              )}`}
            >
              {formatDistanceToNow(updatedDate, { addSuffix: true })}
              <i className="bi bi-pencil ms-2"></i>
            </small>
          ) : (
            <small
              className="created"
              title={format(createdDate, "yyyy/MM/dd' 'HH:mm:ss.sss")}
            >
              {formatDistanceToNow(createdDate, { addSuffix: true })}
            </small>
          )}
        </div>
      </div>
      {userCanEdit && (
        <ButtonToolbar className="ms-auto h-75">
          <ButtonGroup>
            <Button
              variant="outline-secondary"
              onClick={() => (window.location.href = editUrl)}
              title="Edit post"
            >
              <i className="bi bi-pencil"></i>
            </Button>
            <Button
              variant="outline-secondary"
              onClick={() => deletePost(postId)}
              title="Delete post"
            >
              <i className="bi bi-trash"></i>
            </Button>
          </ButtonGroup>
        </ButtonToolbar>
      )}
    </div>
  );
};

export default PostHead;
