"use client";

import "./veritas.css";

import { useEffect, useState } from "react";

import { Conversation } from "..";
import { TerminalIcon, SendIcon, SparklesIcon, RobotIcon } from "./icons";
import {
  ASK_VERITAS,
  fetchStreamedResponse,
  INTRO_MESSAGE,
  SUGGESTED_QUERIES,
} from "../../utils";

export const VeritasPage = () => {
  const [isActive, setIsActive] = useState(null);
  const [chats, setChats] = useState([]);
  const [userMessage, setUserMessage] = useState("");
  const [isLoadingScreen, setIsLoadingScreen] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const checkStatus = async () => {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000);

      try {
        const response = await fetch(
          process.env.NEXT_PUBLIC_VERTITAS_HEALTH_API,
          { signal: controller.signal },
        );
        setIsActive(response.status === 200);
      } catch (error) {
        setIsActive(false);

        if (error.name === "AbortError") {
          console.error("Request timed out after 5 seconds");
        }
      } finally {
        clearTimeout(timeoutId);
        setIsLoadingScreen(false);
      }
    };

    checkStatus();
  }, []);

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

  const handleSubmit = async (event, message = userMessage) => {
    event?.preventDefault();

    if (!message.trim()) return;

    setChats((prevChats) => [
      ...prevChats,
      {
        role: "user",
        message,
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
      message,
      (chunk) => appendToChat(chunk),
      () => setIsLoading(false),
      (error) => {
        appendToChat(`${error}`);
        setIsLoading(false);
      },
    );
  };

  const handleSelectedQuery = (queryIdx) => {
    const selectedQuery = SUGGESTED_QUERIES[queryIdx];
    setUserMessage(selectedQuery);
    handleSubmit(null, selectedQuery);
  };

  return (
    <>
      {isLoadingScreen ? (
        <div className="flex flex-col items-center justify-center w-screen h-screen gap-3">
          <img
            src="/assets/loader.svg"
            alt="Loader"
            width={60}
            height={60}
            className="animate-spin"
          />
          <p className="text-lg font-bold text-primary tracking-wide">
            Loading Veritas AI...
          </p>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center text-center px-4 pt-5 pb-10 appear">
          {/* Header */}
          <div className="flex items-center justify-between w-full px-2 md:px-4 lg:px-8">
            <div className="flex items-center justify-center gap-2">
              <div
                className="w-10 h-10 bg-linear-to-tr from-primary to-primary-light rounded-xl
          flex items-center justify-center shadow-inner border border-white/10"
              >
                <RobotIcon />
              </div>
              <div className="flex flex-col justify-center gap-0">
                <h1 className="text-primary text-lg font-bold leading-tight tracking-wide cursor-default">
                  Veritas
                </h1>
                <div className="flex items-center gap-1">
                  <span
                    className={`w-3 h-3 rounded-full ${
                      isActive ? "bg-green-500" : "bg-red-500"
                    }`}
                  />
                  <span className="text-xs font-bold text-slate-700 uppercase">
                    {isActive ? "Active" : "Inactive"}
                  </span>
                </div>
              </div>
            </div>
            <a
              href={process.env.NEXT_PUBLIC_PORTFOLIO_URL}
              target="_blank"
              className="portfolio__link"
            >
              Portfolio
              <img
                src="assets/redirect-icon.png"
                alt="Redirect Icon"
                className="w-3 h-3 ml-1"
              />
            </a>
          </div>
          {chats.length === 0 ? (
            <div className="flex flex-col items-center justify-center mt-16 slide-up px-4 md:px-2">
              <div
                className="w-20 h-20 bg-white rounded-3xl flex items-center justify-center shadow-xl
            border border-indigo-100 rotate-3 transform transition-transform hover:rotate-6"
              >
                <TerminalIcon />
              </div>
              <h2 className="text-3xl font-extrabold text-primary mt-4">
                {ASK_VERITAS}
              </h2>
              <p className="w-full mt-2 mb-6 text-lg font-semibold text-primary-light">
                {INTRO_MESSAGE}
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-3 w-full md:gap-y-6">
                {SUGGESTED_QUERIES.map((query, idx) => (
                  <button
                    key={idx}
                    className="group flex w-full md:min-w-72 items-center justify-between px-4 py-4
                    bg-white border border-indigo-50 rounded-xl text-left text-slate-700
                    font-semibold shadow-sm transition-all duration-200 hover:border-indigo-300
                    hover:shadow-md hover:text-indigo-700 cursor-pointer
                    disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:border-indigo-50
                    disabled:hover:shadow-none disabled:hover:text-slate-700"
                    disabled={!isActive}
                    onClick={() => handleSelectedQuery(idx)}
                  >
                    {query}
                    <SparklesIcon />
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <Conversation chats={chats} showVeritasTyping={isLoading} />
          )}
          <div className="w-full px-8 py-8 shadow-md fixed bottom-0 md:px-4">
            <form
              onSubmit={handleSubmit}
              className="max-w-2xl mx-auto flex gap-2"
            >
              <input
                id="message"
                name="message"
                type="text"
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                placeholder={
                  isActive
                    ? "Ask Veritas..."
                    : "Veritas is currently offline. Please try again later."
                }
                className="w-full px-4 py-2 bg-white rounded-lg border border-border focus:outline-none focus:ring-1
                focus:ring-border text-[16px] font-medium font-nunito text-(--color-gray) placeholder:text-slate-400
                transition-colors duration-100 ease-in-out disabled:cursor-not-allowed"
                disabled={!isActive}
              />
              {isActive && (
                <button
                  type="submit"
                  className={`px-4 py-3 flex items-center justify-center gap-1 bg-primary text-white rounded-lg
                  font-mediumhover:bg-primary-light transition-colors duration-100
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
                    <SendIcon />
                  )}
                </button>
              )}
            </form>
          </div>
        </div>
      )}
    </>
  );
};
