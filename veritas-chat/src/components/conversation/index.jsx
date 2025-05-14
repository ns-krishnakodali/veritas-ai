"use client";

export const Conversation = ({ chats }) => {
  return (
    <div className="flex flex-col w-3/5 mx-auto items-center justify-center mt-4">
      {chats.map((chat, index) => (
        <div key={index} className="flex justify-center border w-4/5 mb-2">
          {chat.role === "ai" && (
            <img
              src="assets/ai-icon.svg"
              alt="Waving Hand"
              width={20}
              height={20}
            />
          )}
          <p
            id={`chat-${index}`}
            className={`w-full text-lg text-primary ${chat.role === "user" ? "text-right self-end" : "text-left self-start"} `}
          >
            {chat.message}
          </p>
          {chat.role === "user" && (
            <img
              src="assets/ai-icon.svg"
              alt="Waving Hand"
              className="ml-2"
              width={24}
              height={24}
            />
          )}
        </div>
      ))}
    </div>
  );
};
