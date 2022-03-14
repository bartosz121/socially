import { useState } from "react";
import { Button, Modal } from "react-bootstrap";

const PostBody = ({ body, pictureUrl, parentData }) => {
  const [modalOpen, setModalOpen] = useState(false);

  const openModal = () => setModalOpen(true);
  const closeModal = () => setModalOpen(false);

  return (
    <div>
      <div className="post-body">
        {parentData && (
          <div className="post-parent">
            <a href={parentData.parent_url}>
              <small className="parent-info text-muted text-break text-wrap">
                Replying to {parentData.parent_author.username}
              </small>
            </a>
          </div>
        )}
        <p>{body}</p>
      </div>
      {pictureUrl ? (
        <div>
          <div className="post-picture">
            <img
              className="post-img modal-img img-thumbnail mx-auto d-block"
              onClick={() => (modalOpen ? closeModal() : openModal())}
              src={pictureUrl}
              alt="post picture"
            />
          </div>
        </div>
      ) : null}
      <Modal show={modalOpen} onHide={closeModal} size="lg" centered>
        <Modal.Body>
          <img className="w-100" src={pictureUrl} alt="post picture" />
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

export default PostBody;
