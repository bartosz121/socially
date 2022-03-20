import axios from "axios";
import { useState, useEffect } from "react";
import { formatNumberToDisplay } from "../../utils";
import { Modal, Button } from "react-bootstrap";

import "./ProfileDetailHead.scss";
import ProfileList from "../ProfileList/ProfileList";

const ProfileDetailHead = ({
  profileId,
  username,
  bio,
  followersCount,
  followingCount,
  pictureUrl,
  backgroundUrl,
  requestUserId,
}) => {
  const csrfToken = getCookie("csrftoken");
  const followersUrl = `/api/v1/profiles/${profileId}/followers/`;
  const followingUrl = `/api/v1/profiles/${profileId}/following/`;

  const [followersCounter, setFollowersCounter] = useState(followersCount);
  const [requestUserIsFollowing, setRequestUserIsFollowing] = useState(false);

  const [showModal, setShowModal] = useState(false);
  const [modalSourceUrl, setModalSourceUrl] = useState(followersUrl);

  useEffect(() => {
    if (requestUserId) {
      axios
        .get(`/api/v1/profiles/${profileId}/is-following/${requestUserId}/`)
        .then((res) => {
          setRequestUserIsFollowing(res.data.is_following);
        })
        .catch((err) => {
          console.error(err);
        });
    }
  }, []);

  const followProfile = () => {
    const action = requestUserIsFollowing ? "unfollow" : "follow";
    axios
      .post(
        `/api/v1/profiles/${profileId}/follow/`,
        {
          action: action,
        },
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
        }
      )
      .then((res) => {
        setFollowersCounter(res.data.followers_count);
        setRequestUserIsFollowing(!requestUserIsFollowing);
      })
      .catch((err) => {
        if (err.response) {
          if (err.response.status === 403) {
            window.location.pathname = "/accounts/login/";
          }
        }
        console.error(err);
      });
  };

  const openModal = (sourceUrl) => {
    setModalSourceUrl(sourceUrl);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
  };

  return (
    <div>
      <div className="profile-background" id="profile-background">
        <img
          className="w-100 rounded-3 modal-img"
          src={backgroundUrl}
          alt="Profile background"
        />
      </div>
      <div className="profile-header d-flex flex-column flex-md-row align-items-center justify-content-center justify-content-md-evenly flex-wrap rounded-3">
        <img
          className="img-thumbnail modal-img"
          id="profile-picture"
          src={pictureUrl}
          alt="Profile picture"
        />
        <p className="display-6 profile-header-username text-break text-center">
          {username}
        </p>
        <div className="follow-info d-flex flex-row align-items-center justify-content-around user-select-none">
          <div
            role="button"
            className="pointer-hover-underline"
            onClick={() => {
              if (followingCount > 0) {
                openModal(followingUrl);
              }
            }}
          >
            {formatNumberToDisplay(followingCount)}
            <small className="text-muted">Following</small>
          </div>
          <div
            role="button"
            className="pointer-hover-underline"
            onClick={() => {
              if (followersCounter > 0) {
                openModal(followersUrl);
              }
            }}
          >
            {formatNumberToDisplay(followersCounter)}
            <small className="text-muted">Followers</small>
          </div>
        </div>
        <div className="profile-bio w-100 mt-2 text-muted">
          <p className="text-center">{bio}</p>
        </div>
        <Button
          className="px-4"
          onClick={followProfile}
          variant={requestUserIsFollowing ? "danger" : "primary"}
        >
          {requestUserIsFollowing ? "Unfollow" : "Follow"}
        </Button>
      </div>
      <Modal show={showModal} onHide={closeModal} size="sm" centered>
        <Modal.Body>
          <ProfileList sourceUrl={modalSourceUrl} />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={closeModal}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default ProfileDetailHead;
