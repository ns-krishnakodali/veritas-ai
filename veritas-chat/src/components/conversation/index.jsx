"use client";

import { highlightUrl } from "../../utils";
import TypingIndicator from "../typing-indicator";
import "./component.css";

import { useEffect, useRef } from "react";

export const Conversation = ({ chats, showVeritasTyping }) => {
  const lastMessageRef = useRef(null);

  useEffect(() => {
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chats]);

  return (
    <div className="flex flex-col w-3/5 mx-auto items-center justify-center mt-8 mb-12">
      {chats.map((chat, index) => (
        <div
          key={index}
          className={`flex justify-center w-4/5 mb-3 ${chat.role === "user" ? "justify-end slide-up" : "justify-start"}`}
        >
          {chat.role === "veritas" && (
            <img
              src="/assets/llm-icon.svg"
              alt="LLM Icon"
              className="mr-2"
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
            className={`max-w-full text-left text-lg text-primary font-semibold
              break-words whitespace-normal rounded-lg px-2 py-1 ${chat.role === "user" && "bg-chat-bg"} tracking-wide`}
          >
            {highlightUrl(chat.message)}
          </p>

          {chat.role === "user" && (
            <img
              src="/assets/user-icon.svg"
              alt="User Icon"
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
