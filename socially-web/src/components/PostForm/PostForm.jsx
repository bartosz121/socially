import axios from "axios";
import { getFormData, getCookie } from "../../utils";

const PostForm = ({ parentPostId, isReply, newPostCallback }) => {
  const csrfToken = getCookie("csrftoken");

  const textAreaPlaceholder = isReply ? "Reply..." : "What's on your mind?";
  const buttonText = isReply ? "Reply" : "Post";

  const handleSubmit = (e) => {
    e.preventDefault();
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
      });

    e.currentTarget.reset();
  };

  return (
    <div class="card-body">
      <form
        onSubmit={handleSubmit}
        id="post-form"
        method="POST"
        enctype="multipart/form-data"
      >
        <input type="hidden" name="parent_post" value={parentPostId} />
        <div id="div_id_body" class="mb-3">
          <textarea
            name="body"
            cols="40"
            rows="4"
            maxlength="240"
            placeholder={textAreaPlaceholder}
            class="textarea form-control"
            required={true}
            id="id_body"
          ></textarea>
        </div>
        <div class="row">
          <div class="col-lg-9">
            <div id="div_id_picture" class="mb-3">
              <div class=" mb-2">
                <div id="div_id_picture" class="mb-3">
                  <div class=" mb-2">
                    <div>
                      <input
                        type="file"
                        name="picture_url"
                        class="form-control"
                        accept="image/*"
                        required={false}
                        id="id_picture"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md ">
            <div class="ms-lg-3 pe-lg-3 w-100">
              <button
                id="post-submit-btn"
                type="submit"
                class="btn btn-primary w-100"
              >
                {buttonText}
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
};

export default PostForm;
