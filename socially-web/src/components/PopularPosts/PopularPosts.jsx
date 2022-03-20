import useFetch from "../../useFetchData";
import Spinner from "../spinner/Spinner";

const PopularPosts = () => {
  const { data, loading, error } = useFetch(`/api/v1/posts/most-commented/`);

  const trimBody = (body) => {
    return body.substring(0, 20) + "...";
  };

  return (
    <div>
      {loading && <Spinner />}
      {data && (
        <div class="follow-suggestions my-4">
          <h4>Popular posts</h4>
          <ul class="list-group my-4">
            {data.map((post, i) => (
              <li
                class="list-group-item d-flex justify-content-between align-items-start"
                key={i}
              >
                <div class="ms-2 me-auto">
                  <a href={post.url}>
                    <div class="pointer-hover-underline fw-bold text-wrap text-break">
                      {post.body.length > 20 ? trimBody(post.body) : post.body}
                    </div>
                  </a>
                  <a href={post.post_author.profile_url}>
                    <span class="pointer-hover-underline text-muted text-break text-wrap">
                      by {post.post_author.username}
                    </span>
                  </a>
                </div>
                <span class="badge bg-primary rounded-pill" title="Replies">
                  {post.comment_count > 99 ? "+99" : post.comment_count}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default PopularPosts;
