import { useState } from "react";
import { getFormData, getCookie } from "../../utils";
import axios from "axios";

import Spinner from "../spinner/Spinner";

const PostForm = ({ parentPostId, isReply, newPostCallback }) => {
  const csrfToken = getCookie("csrftoken");

  const [isPostUploading, setIsPostUploading] = useState(false);

  const textAreaPlaceholder = isReply ? "Reply..." : "What's on your mind?";
  const buttonText = isReply ? "Reply" : "Post";

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsPostUploading(true);
    const values = getFormData(e);

    axios
      .post("/api/v1/posts/", values, {
        headers: {
          "Content-Type": "multipart/form-data",
          "X-CSRFToken": csrfToken,
        },
      })
      .then(function (response) {
        newPostCallback(response.data);
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => setIsPostUploading(false));

    e.currentTarget.reset();
  };

  return (
    <div className="card-body">
      <form
        onSubmit={handleSubmit}
        id="post-form"
        method="POST"
        enctype="multipart/form-data"
      >
        <input type="hidden" name="parent_post" value={parentPostId} />
        <div id="div_id_body" className="mb-3">
          <textarea
            name="body"
            cols="40"
            rows="4"
            maxlength="240"
            placeholder={textAreaPlaceholder}
            className="textarea form-control"
            required={true}
            id="id_body"
            disabled={isPostUploading}
          ></textarea>
        </div>
        <div className="row">
          <div className="col-lg-9">
            <div id="div_id_picture" className="mb-3">
              <div className=" mb-2">
                <div id="div_id_picture" className="mb-3">
                  <div className=" mb-2">
                    <div>
                      <input
                        type="file"
                        name="picture_url"
                        className="form-control"
                        accept="image/*"
                        required={false}
                        id="id_picture"
                        disabled={isPostUploading}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="col-md ">
            <div className="ms-lg-3 pe-lg-3 w-100">
              <button
                id="post-submit-btn"
                type="submit"
                className="btn btn-primary w-100"
                disabled={isPostUploading}
              >
                {buttonText}
              </button>
            </div>
          </div>
        </div>
      </form>
      {isPostUploading && <Spinner />}
    </div>
  );
};

export default PostForm;
