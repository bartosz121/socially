import useFetchData from "../../useFetchData";
import Spinner from "../../components/spinner/Spinner";
import ProfileDetailHead from "../../components/ProfileDetailHead/ProfileDetailHead";
import PostList from "../../components/PostList/PostList";

const ProfileDetailPage = ({
  profileId,
  requestUserId,
  requestUserIsStaff,
}) => {
  profileId = parseInt(profileId);
  requestUserId = parseInt(requestUserId);

  const userPostsUrl = `/api/v1/users/${profileId}/posts`;

  const { data, loading, error } = useFetchData(
    `/api/v1/profiles/${profileId}/`
  );
  return (
    <div>
      {loading && <Spinner />}
      {data && (
        <div>
          <ProfileDetailHead
            profileId={profileId}
            username={data.username}
            bio={data.bio}
            followersCount={data.followers_count}
            followingCount={data.following_count}
            pictureUrl={data.profile_picture}
            backgroundUrl={data.profile_background}
            requestUserId={requestUserId}
          />
          {data.posts_count > 0 ? (
            <PostList
              newestPost={null}
              sourceUrl={userPostsUrl}
              requestUserId={requestUserId}
              requestUserIsStaff={requestUserIsStaff}
            />
          ) : (
            <div className="mt-4 d-flex flex-row justify-content-center">
              <h3>No posts yet.</h3>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ProfileDetailPage;
