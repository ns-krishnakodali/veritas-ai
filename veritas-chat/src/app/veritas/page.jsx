"use client";

import "./veritas.css";

import { useState } from "react";

import { Conversation } from "../../components";
import { fetchStreamedResponse, INTRO_MESSAGE } from "../../utils";

export const VeritasPage = () => {
  const [chats, setChats] = useState([]);
  const [userMessage, setUserMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const appendToChat = (text) => {
    setChats((prevChats) => {
      const lastChat = prevChats[prevChats.length - 1];
      if (lastChat?.role === "veritas") {
        const updatedLast = {
          ...lastChat,
          message: lastChat.message + text,
        };
        return [...prevChats.slice(0, -1), updatedLast];
      }
      return prevChats;
    });
  };

  const handleSubmit = async (event) => {
    event?.preventDefault();

    if (!userMessage.trim()) return;

    setChats((prevChats) => [
      ...prevChats,
      {
        role: "user",
        message: userMessage,
      },
    ]);
    setUserMessage("");
    setIsLoading(true);

    setChats((prevChats) => [
      ...prevChats,
      {
        role: "veritas",
        message: "",
      },
    ]);

    fetchStreamedResponse(
      userMessage,
      (chunk) => appendToChat(chunk),
      () => setIsLoading(false),
      (error) => {
        appendToChat(`😞${error}`);
        setIsLoading(false);
      },
    );
  };

  return (
    <div className="flex flex-col items-center justify-center text-center py-10 appear">
      <h1 className="text-4xl text-primary font-bold cursor-default">
        Veritas AI
      </h1>
      {chats.length === 0 ? (
        <div className="flex flex-col items-center justify-center mt-8">
          <img
            src="/assets/waving-hand.svg"
            alt="Waving Hand"
            width={90}
            height={90}
          />
          <p className="w-2/3 mt-2 text-lg font-semibold text-primary-light">
            {INTRO_MESSAGE}
          </p>
        </div>
      ) : (
        <Conversation chats={chats} showVeritasTyping={isLoading} />
      )}
      <div className="w-full px-4 py-8 shadow-md fixed bottom-0">
        <form onSubmit={handleSubmit} className="max-w-2xl mx-auto flex gap-2">
          <input
            id="message"
            name="message"
            type="text"
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
            placeholder="Ask Veritas..."
            className="w-full px-4 py-2 bg-white rounded-md border border-border focus:outline-none focus:ring-1 focus:ring-border 
             text-[16px] font-medium font-nunito text-[var(--color-gray)] 
             placeholder:text-slate-400 transition-colors duration-100 ease-in-out"
          />
          <button
            type="submit"
            className={`px-4 py-2 flex items-center justify-center gap-1 bg-primary text-white rounded-md
              font-medium hover:bg-primary-light transition-colors duration-100 
              ${isLoading ? "cursor-progress" : "cursor-pointer"}`}
            disabled={isLoading}
          >
            {isLoading ? (
              <img
                src="/assets/loader.svg"
                alt="Loader"
                width={30}
                height={30}
              />
            ) : (
              "Ask"
            )}
          </button>
        </form>
      </div>
    </div>
  );
};
