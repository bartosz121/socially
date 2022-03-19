import { useEffect, useState } from "react";

import Spinner from "../spinner/Spinner";
import PostListItem from "../PostListItem/PostListItem";
import InfiniteScroll from "react-infinite-scroll-component";
import axios from "axios";

import "./PostList.scss";

function PostList({ newestPost, sourceUrl, endMessage, userId, userIsStaff }) {
  userId = parseInt(userId);
  userIsStaff = userIsStaff === "True" ? true : false;

  const defaultPostSourceUrl = "/api/v1/posts/";
  const [posts, setPosts] = useState([]);
  const [postsCount, setPostsCount] = useState(0);
  const [error, setError] = useState(false);
  const [nextUrl, setNextUrl] = useState(
    sourceUrl ? sourceUrl : defaultPostSourceUrl
  );

  useEffect(() => {
    if (newestPost !== null) {
      setPosts([newestPost, ...posts]);
    }
  }, [newestPost]);

  useEffect(() => {
    getPosts();
  }, []);

  const getPosts = async () => {
    setError(false);

    try {
      const result = await axios.get(nextUrl);
      setPosts([...posts, ...result.data.results]);
      setPostsCount(result.data.count);
      setNextUrl(result.data.next);
    } catch (error) {
      setError(true);
    }
  };

  return (
    <InfiniteScroll
      dataLength={posts.length}
      next={getPosts}
      hasMore={posts.length < postsCount}
      loader={<Spinner />}
      endMessage={endMessage ? endMessage : <hr />}
      scrollThreshold={0.9}
    >
      {posts.map((post, i) => (
        <div key={i}>
          <PostListItem post={post} userId={userId} userIsStaff={userIsStaff} />
        </div>
      ))}
    </InfiniteScroll>
  );
}

export default PostList;
