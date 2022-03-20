import useFetch from "../../useFetchData";
import Spinner from "../spinner/Spinner";

const FollowSuggestions = ({ requestUserId }) => {
  requestUserId = parseInt(requestUserId);

  const { data, loading, error } = useFetch(
    `/api/v1/profiles/${requestUserId}/follow-suggestions/`
  );

  return (
    <div>
      {loading && <Spinner />}
      {data && (
        <div class="follow-suggestions my-4">
          <h4>People you might know</h4>
          <ul class="list-group">
            {data.map((profile, i) => (
              <li class="list-group-item d-flex flex-column">
                <div class="w-100 p-2 d-flex align-items-center justify-content-center flex-wrap">
                  <div class="follow-suggestion-img">
                    <a href={profile.profile_url}>
                      <img
                        class="profile-picture-medium rounded"
                        src={profile.profile_picture}
                        alt="Profile picture"
                      />
                    </a>
                  </div>
                  <div class="w-100 text-center mt-1">
                    <a href={profile.profile_url}>
                      <span class="pointer-hover-underline text-break">
                        {profile.username}
                      </span>
                    </a>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FollowSuggestions;
