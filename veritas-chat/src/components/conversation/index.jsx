"use client";

import { useEffect, useRef } from "react";

import TypingIndicator from "../typing-indicator";

import { formatText } from "../../utils";

export const Conversation = ({ chats, showVeritasTyping }) => {
  const conversationEndRef = useRef(null);

  useEffect(() => {
    if (conversationEndRef.current) {
      requestAnimationFrame(() => {
        conversationEndRef.current?.scrollIntoView({
          behavior: showVeritasTyping ? "auto" : "smooth",
          block: "end",
          inline: "nearest",
        });
      });
    }
  }, [chats, showVeritasTyping]);

  return (
    <div
      className="mt-8 mb-20 flex w-full max-w-6xl flex-col items-center justify-center px-2 sm:px-4"
      aria-live="polite"
    >
      {chats.map((chat, index) => {
        const isUserMessage = chat.role === "user";
        const isTypingMessage =
          showVeritasTyping && chat.role === "veritas" && chat.message === "";

        return (
          <div
            key={index}
            className={`mb-3 flex w-full items-end gap-2 ${
              isUserMessage
                ? "justify-end animate-[slide-up_0.5s_ease-out_forwards]"
                : "justify-start"
            }`}
          >
            {chat.role === "veritas" && (
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-border bg-panel shadow-card">
                <img
                  src="/assets/llm-icon.svg"
                  alt="LLM Icon"
                  className="h-4 w-4 filter-[brightness(0)_saturate(100%)_invert(79%)_sepia(43%)_saturate(746%)_hue-rotate(123deg)_brightness(96%)_contrast(91%)]"
                  width={16}
                  height={16}
                />
              </span>
            )}
            <div
              id={`chat-${index}`}
              className={`w-fit max-w-full whitespace-normal wrap-break-word rounded-lg px-3 py-2 text-left text-[15px] font-semibold tracking-wide text-primary
                sm:text-base ${
                  isUserMessage
                    ? "border border-amber-400/25 bg-user-bg shadow-card"
                    : ""
                }`}
            >
              {isTypingMessage ? <TypingIndicator /> : formatText(chat.message)}
            </div>
            {isUserMessage && (
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-amber-400/25 bg-user-bg shadow-card">
                <img
                  src="/assets/user-icon.svg"
                  alt="User Icon"
                  className="h-3.5 w-3.5 invert opacity-90"
                  width={14}
                  height={14}
                />
              </span>
            )}
          </div>
        );
      })}
      <div
        ref={conversationEndRef}
        className="scroll-mb-28 sm:scroll-mb-36"
        aria-hidden="true"
      />
    </div>
  );
};
