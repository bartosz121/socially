import React from "react";
import ReactDOM from "react-dom";
import HomeSection from "./components/HomeSection/HomeSection";
import ProfileDetailPage from "./pages/ProfileDetailPage/ProfileDetailPage";
import PostDetailPage from "./components/PostDetail/PostDetail";
import PostList from "./components/PostList/PostList";

import "./index.css";
import FollowSuggestions from "./components/FollowSuggestions/FollowSuggestions";
import PopularPosts from "./components/PopularPosts/PopularPosts";

// Home section feed
const homeSectionElement = document.getElementById("home-section");

if (homeSectionElement) {
  ReactDOM.render(
    <HomeSection {...homeSectionElement.dataset} />,
    homeSectionElement
  );
}

// Explore page feed
const exploreFeedElement = document.getElementById("explore-feed");

if (exploreFeedElement) {
  ReactDOM.render(
    <PostList newestPost={null} {...exploreFeedElement.dataset} />,
    exploreFeedElement
  );
}

// Follow Suggestions
const followSuggestionsElement = document.getElementById("follow-suggestions");

if (followSuggestionsElement) {
  ReactDOM.render(
    <FollowSuggestions {...followSuggestionsElement.dataset} />,
    followSuggestionsElement
  );
}

// Popular Posts
const popularPostsElement = document.getElementById("popular-posts");

if (popularPostsElement) {
  ReactDOM.render(<PopularPosts />, popularPostsElement);
}

// Post Detail
const postDetailElement = document.getElementById("post-detail");
if (postDetailElement) {
  ReactDOM.render(
    <PostDetailPage {...postDetailElement.dataset} />,
    postDetailElement
  );
}

// Profile Detail
const profileDetailElement = document.getElementById("profile-detail");
if (profileDetailElement) {
  ReactDOM.render(
    <ProfileDetailPage {...profileDetailElement.dataset} />,
    profileDetailElement
  );
}
