import useFetch from "../../useFetchData";
import PostHead from "../PostHead/PostHead";
import PostBody from "../post-body/PostBody";
import PostBottom from "../PostBottom/PostBottom";
import PostComments from "../PostComments/PostComments";
import Spinner from "../spinner/Spinner";

const PostDetail = ({ postId, userId, userIsStaff }) => {
  const { data, loading, error } = useFetch(
    `http://localhost:8000/api/v1/posts/${postId}/`
  );

  return (
    <div>
      {loading && <Spinner />}
      {data && (
        <div className="post my-4 p-5 bg-light border rounded-3">
          <PostHead
            userCanEdit={userId === data.post_author.id || userIsStaff}
            postId={data.id}
            postAuthor={data.post_author}
            editUrl={data.editUrl}
            created={data.created}
            updated={data.updated}
            setPostVisible={console.log}
          />
          <PostBody
            body={data.body}
            pictureUrl={data.picture_url}
            parentData={data.parent_post}
          />
          <hr />
          <PostBottom
            postId={data.id}
            postLikeCount={data.like_count}
            postDetailUrl={data.url}
          />
          <hr />
          {data.comment_count > 0 && (
            <PostComments
              parentId={data.id}
              userId={userId}
              userIsStaff={userIsStaff}
            />
          )}
        </div>
      )}
    </div>
  );
};

export default PostDetail;
