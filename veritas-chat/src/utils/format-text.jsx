const URL_PATTERN = /https?:\/\/[^\s]+/;
const EMAIL_PATTERN = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/;
const BOLD_REGEX = /(\*\*[^*]+\*\*)/g;
const TRAILING_PUNCTUATION_REGEX = /[.,!?)]$/;

export const formatText = (text, { enableEmail = true } = {}) => {
  if (!text) return;

  const combinedRegex = enableEmail
    ? new RegExp(`(${URL_PATTERN.source}|${EMAIL_PATTERN.source})`, "g")
    : new RegExp(`(${URL_PATTERN.source})`, "g");

  const renderLinks = (value, keyPrefix = "") =>
    value
      .split(combinedRegex)
      .filter(Boolean)
      .map((part, index) => {
        const key = `${keyPrefix}-${index}`;

        if (URL_PATTERN.test(part)) {
          const trimmed = part.replace(TRAILING_PUNCTUATION_REGEX, "");
          const trailing = part.slice(trimmed.length);

          return (
            <span key={key}>
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

        if (enableEmail && EMAIL_PATTERN.test(part)) {
          const trimmed = part.replace(TRAILING_PUNCTUATION_REGEX, "");
          const trailing = part.slice(trimmed.length);

          return (
            <span key={key}>
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

        return <span key={key}>{part}</span>;
      });

  return text
    .split(BOLD_REGEX)
    .filter(Boolean)
    .map((part, index) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={index} className="font-bold">
            {renderLinks(part.slice(2, -2), `bold-${index}`)}
          </strong>
        );
      }

      return renderLinks(part, `text-${index}`);
    });
};
