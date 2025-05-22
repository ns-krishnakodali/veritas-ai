const URL_REGEX = /(https?:\/\/[^\s]+)/g;

export const highlightUrl = (text) => {
  if (!text || text.length === 0) {
    return;
  }

  return text
    .split(URL_REGEX)
    ?.filter(Boolean)
    .map((part, index) =>
      URL_REGEX.test(part) ? (
        <a
          key={index}
          href={part}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-500 underline hover:text-blue-700"
        >
          {part}
        </a>
      ) : (
        <span key={index}>{part}</span>
      ),
    );
};
