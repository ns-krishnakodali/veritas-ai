import "./typing-indicator.css";

const TypingIndicator = () => (
  <svg height="40" width="40" className="loader">
    <circle className="dot" cx="10" cy="20" r="3" />
    <circle className="dot" cx="20" cy="20" r="3" />
    <circle className="dot" cx="30" cy="20" r="3" />
  </svg>
);

export default TypingIndicator;
