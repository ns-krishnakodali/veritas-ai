const URL_REGEX = /https?:\/\/[^\s]+/g;
const EMAIL_REGEX = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;

const TRAILING_PUNCTUATION_REGEX = /[.,!?)]$/;
export const highlightLinks = (text, { enableEmail = true } = {}) => {
  if (!text) return;

  const combinedRegex = enableEmail
    ? new RegExp(`(${URL_REGEX.source}|${EMAIL_REGEX.source})`, "g")
    : new RegExp(`(${URL_REGEX.source})`, "g");

  return text
    .split(combinedRegex)
    .filter(Boolean)
    .map((part, index) => {
      if (URL_REGEX.test(part)) {
        const trimmed = part.replace(TRAILING_PUNCTUATION_REGEX, "");
        const trailing = part.slice(trimmed.length);

        return (
          <span key={index}>
            <a
              href={trimmed}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 underline hover:text-blue-700"
            >
              {trimmed}
            </a>
            {trailing}
          </span>
        );
      }

      if (enableEmail && EMAIL_REGEX.test(part)) {
        const trimmed = part.replace(TRAILING_PUNCTUATION_REGEX, "");
        const trailing = part.slice(trimmed.length);

        return (
          <span key={index}>
            <a
              href={`mailto:${trimmed}`}
              className="text-blue-500 underline hover:text-blue-700"
            >
              {trimmed}
            </a>
            {trailing}
          </span>
        );
      }

      return <span key={index}>{part}</span>;
    });
};
