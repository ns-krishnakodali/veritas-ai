"use client";

import { useEffect, useRef } from "react";

import TypingIndicator from "../typing-indicator";

import { highlightUrl } from "../../utils";

export const Conversation = ({ chats, showVeritasTyping }) => {
  const lastMessageRef = useRef(null);

  useEffect(() => {
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chats]);

  return (
    <div className="flex flex-col w-[95%] sm:w-4/5 md:w-3/5 mx-auto items-center justify-center mt-8 mb-12">
      {chats.map((chat, index) => (
        <div
          key={index}
          className={`flex w-full sm:w-4/5 justify-center mb-3 ${
            chat.role === "user" ? "justify-end slide-up" : "justify-start"
          }`}
        >
          {chat.role === "veritas" && (
            <img
              src="/assets/llm-icon.svg"
              alt="LLM Icon"
              className="mr-2 mt-[2px]"
              width={20}
              height={20}
            />
          )}
          {showVeritasTyping &&
            chat.role === "veritas" &&
            chat.message === "" && <TypingIndicator />}
          <p
            id={`chat-${index}`}
            ref={index === chats?.length - 1 ? lastMessageRef : null}
            className={`max-w-[85%] sm:max-w-full text-left text-base sm:text-lg text-primary font-semibold break-words whitespace-normal
              rounded-lg px-3 py-2 ${chat.role === "user" && "bg-chat-bg"} tracking-wide`}
          >
            {highlightUrl(chat.message)}
          </p>

          {chat.role === "user" && (
            <img
              src="/assets/user-icon.svg"
              alt="User Icon"
              className="ml-2 mt-[2px]"
              width={16}
              height={16}
            />
          )}
        </div>
      ))}
    </div>
  );
};
