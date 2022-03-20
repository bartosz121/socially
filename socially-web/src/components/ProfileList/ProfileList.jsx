import { useEffect, useState } from "react";

import axios from "axios";
import Spinner from "../spinner/Spinner";
import InfiniteScroll from "react-infinite-scroll-component";
import ProfileListItem from "../ProfileListItem/ProfileListItem";

const ProfileList = ({ sourceUrl }) => {
  const [profiles, setProfiles] = useState([]);
  const [profilesCount, setProfilesCount] = useState(0);
  const [error, setError] = useState(false);
  const [nextUrl, setNextUrl] = useState(sourceUrl);

  useEffect(() => {
    getProfiles();
  }, []);

  const getProfiles = async () => {
    setError(false);

    try {
      const result = await axios.get(nextUrl);
      setProfiles([...profiles, ...result.data.results]);
      setProfilesCount(result.data.count);
      setNextUrl(result.data.next);
    } catch (error) {
      setError(true);
    }
  };

  return (
    <div
      id="scrollableDiv"
      className="overflow-auto"
      style={{ maxHeight: "50vh" }}
    >
      <InfiniteScroll
        dataLength={profiles.length}
        next={getProfiles}
        hasMore={profiles.length < profilesCount}
        loader={<Spinner />}
        scrollableTarget="scrollableDiv"
      >
        {profiles.map((profile, i) => (
          <div key={i}>
            <ProfileListItem profileData={profile} />
          </div>
        ))}
      </InfiniteScroll>
    </div>
  );
};

export default ProfileList;
