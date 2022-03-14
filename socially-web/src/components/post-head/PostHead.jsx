import axios from "axios";
import { formatDistanceToNow, format, compareAsc } from "date-fns";
import { getCookie } from "../../utils";

const PostHead = ({
  postId,
  postAuthor,
  postDetailUrl,
  editUrl,
  created,
  updated,
  setPostVisible,
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
          setPostVisible(false);
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
      <div className="post-dots ms-auto text-muted">
        <i
          className="bi bi-three-dots-vertical"
          type="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        ></i>
        <ul
          className="dropdown-menu"
          aria-labelledby="postDetailDropdownMenuButton{{ post.pk }}"
        >
          <li>
            <a className="dropdown-item" href={postDetailUrl}>
              <i className="bi bi-box-arrow-right me-2"></i>
              <span>Check post page</span>
            </a>
          </li>
          <li>
            <a className="dropdown-item" href={postDetailUrl}>
              <i className="bi bi-person-circle me-2"></i>
              <span>Check author profile</span>
            </a>
          </li>
          {editUrl && (
            <div>
              <li>
                <a className="dropdown-item" href={editUrl}>
                  <i className="bi bi-pencil me-2"></i>
                  <span>Edit post</span>
                </a>
              </li>
              <li onClick={() => deletePost(postId)}>
                <a className="dropdown-item">
                  <i className="bi bi-trash me-2"></i>
                  <span>Delete post</span>
                </a>
              </li>
            </div>
          )}
        </ul>
      </div>
    </div>
  );
};

export default PostHead;
