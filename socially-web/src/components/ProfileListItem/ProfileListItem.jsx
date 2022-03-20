const ProfileListItem = ({ profileData }) => {
  const {
    username,
    profile_picture: pictureUrl,
    profile_url: profileUrl,
  } = profileData;

  return (
    <div
      role="button"
      class="d-flex my-2"
      onClick={() => (window.location.href = profileUrl)}
    >
      <img
        class="profile-picture-medium rounded"
        src={pictureUrl}
        alt="Profile picture"
      />
      <p class="pointer-hover-underline text-break ms-2 mt-3">{username}</p>
    </div>
  );
};

export default ProfileListItem;
