import useFetch from "../../useFetchData";
import PostHead from "../PostHead/PostHead";
import PostBody from "../PostBody/PostBody";
import PostBottom from "../PostBottom/PostBottom";
import CommentsSection from "../CommentsSection/CommentsSection";
import Spinner from "../spinner/Spinner";

const PostDetail = ({ postId, requestUserId, requestUserIsStaff }) => {
  requestUserId = parseInt(requestUserId);
  requestUserIsStaff = requestUserIsStaff === "True" ? true : false;

  const { data, loading, error } = useFetch(`/api/v1/posts/${postId}/`);

  return (
    <div>
      {loading && <Spinner />}
      {data && (
        <div className="post my-4 p-5 bg-light border rounded-3">
          <PostHead
            userCanEdit={
              requestUserId === data.post_author.user_id || requestUserIsStaff
            }
            postId={postId}
            postAuthor={data.post_author}
            editUrl={data.editUrl}
            created={data.created}
            updated={data.updated}
            deleteCallback={() => (window.location.pathname = "/")}
          />
          <PostBody
            body={data.body}
            pictureUrl={data.picture_url}
            parentData={data.parent_post}
          />
          <hr />
          <PostBottom
            requestUserId={requestUserId}
            postId={postId}
            postLikeCount={data.like_count}
            postDetailUrl={data.url}
          />
          <hr />
          <CommentsSection
            parentId={postId}
            anyComments={data.comment_count > 0}
            requestUserId={requestUserId}
            requestUserIsStaff={requestUserIsStaff}
          />
        </div>
      )}
    </div>
  );
};

export default PostDetail;
