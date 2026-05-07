const TypingIndicator = () => (
  <div
    className="inline-flex items-center gap-1.5 text-primary"
    aria-label="Veritas is typing"
  >
    <span className="h-2 w-2 rounded-full bg-current animate-[blink_1s_infinite]" />
    <span className="h-2 w-2 rounded-full bg-current animate-[blink_1s_infinite] [animation-delay:250ms]" />
    <span className="h-2 w-2 rounded-full bg-current animate-[blink_1s_infinite] [animation-delay:500ms]" />
  </div>
);

export default TypingIndicator;
