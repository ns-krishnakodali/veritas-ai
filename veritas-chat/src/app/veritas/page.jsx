"use client";

import "./veritas.css";

import { useState } from "react";

import { Conversation } from "../../components";
import { INTRO_MESSAGE } from "../../constants";

export const VeritasPage = () => {
  const [chats, setChats] = useState([]);
  const [message, setMessage] = useState("");

  const handleSubmit = (event) => {
    event?.preventDefault();

    if (!message.trim()) return;

    setChats((prevChats) => [
      ...prevChats,
      {
        role: "user",
        message,
      },
    ]);

    setMessage("");
  };

  return (
    <div className="flex flex-col items-center justify-center text-center py-10 appear">
      <h1 className="text-4xl text-primary font-bold cursor-default">
        Veritas AI
      </h1>
      {chats.length === 0 ? (
        <div className="flex flex-col items-center justify-center mt-8">
          <img
            src="assets/waving-hand.svg"
            alt="Waving Hand"
            width={90}
            height={90}
          />
          <p className="w-2/3 mt-2 text-lg font-semibold text-primary-light">
            {INTRO_MESSAGE}
          </p>
        </div>
      ) : (
        <Conversation chats={chats} />
      )}
      <div className="w-full px-4 py-8 shadow-md fixed bottom-0">
        <form onSubmit={handleSubmit} className="max-w-2xl mx-auto flex gap-2">
          <input
            id="message"
            name="message"
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask Veritas..."
            className="w-full px-4 py-2 bg-white rounded-md border border-border focus:outline-none focus:ring-1 focus:ring-border 
             text-[16px] font-medium font-nunito text-[var(--color-gray)] 
             placeholder:text-slate-400 transition-colors duration-100 ease-in-out"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-primary text-white rounded-md font-medium hover:bg-primary-light transition-colors duration-100"
          >
            Ask
          </button>
        </form>
      </div>
    </div>
  );
};
