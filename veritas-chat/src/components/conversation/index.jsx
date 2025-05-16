"use client";

import "./component.css";

export const Conversation = ({ chats }) => {
  return (
    <div className="flex flex-col w-3/5 mx-auto items-center justify-center mt-8 mb-12">
      {chats.map((chat, index) => (
        <div
          key={index}
          className={`flex justify-center w-4/5 mb-2 ${chat.role === "user" ? "justify-end slide-up" : "justify-start"}`}
        >
          {chat.role === "ai" && (
            <img
              src="assets/ai-icon.svg"
              alt="Waving Hand"
              className="mr-2"
              width={20}
              height={20}
            />
          )}
          <p
            id={`chat-${index}`}
            className="max-w-full text-left text-lg text-primary font-semibold
              break-words whitespace-normal rounded-lg px-2 py-1 bg-chat-bg tracking-wide"
          >
            {chat.message}
          </p>

          {chat.role === "user" && (
            <img
              src="assets/user-icon.svg"
              alt="Waving Hand"
              className="ml-2"
              width={16}
              height={16}
            />
          )}
        </div>
      ))}
    </div>
  );
};
