import { motion } from "framer-motion";

const PostActionButton = ({ className, children, handleClick, ...props }) => {
  return (
    <motion.div
      onClick={handleClick}
      whileHover={{ scale: 1.4 }}
      whileTap={{ scale: 0.9 }}
      className={className}
      {...props}
    >
      {children}
    </motion.div>
  );
};

export default PostActionButton;
