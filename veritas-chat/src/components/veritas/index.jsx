"use client";

import { useEffect, useState } from "react";

import { Conversation } from "..";
import { SendIcon, SparklesIcon, TerminalIcon, RobotIcon } from "./icons";
import {
  ASK_VERITAS,
  INTRO_MESSAGE,
  SUGGESTED_QUERIES,
  fetchStreamedResponse,
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
          console.error("Request timed out after 60 seconds");
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
        <div className="flex h-screen w-screen flex-col items-center justify-center gap-3">
          <img
            src="/assets/loader.svg"
            alt="Loader"
            width={60}
            height={60}
            className="animate-spin"
          />
          <p className="text-lg font-bold tracking-wide text-primary">
            Loading Veritas AI...
          </p>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center px-4 pt-5 pb-32 text-center">
          <div className="flex w-full items-center justify-between px-2 md:px-4 lg:px-8">
            <div className="flex items-center justify-center gap-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-brand-strong shadow-card">
                <RobotIcon />
              </div>
              <div className="flex flex-col justify-center gap-0">
                <h1 className="cursor-default text-lg font-bold leading-tight tracking-wide text-primary">
                  Veritas
                </h1>
                <div className="flex items-center gap-1">
                  <span
                    className={`h-3 w-3 rounded-full ${
                      isActive ? "bg-emerald-400" : "bg-rose-400"
                    }`}
                  />
                  <span className="text-xs font-bold uppercase text-muted">
                    {isActive ? "Active" : "Inactive"}
                  </span>
                </div>
              </div>
            </div>
            <a
              href={process.env.NEXT_PUBLIC_PORTFOLIO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="group relative inline-flex items-center justify-center rounded-full px-3 py-1.5 text-[15px] font-semibold text-secondary
                transition-[color,background,transform] duration-200 hover:z-1 hover:-translate-y-px hover:text-primary before:absolute before:inset-0 before:-z-10
                before:rounded-full before:border before:border-border-strong before:bg-panel-soft before:opacity-0 before:transition-opacity before:duration-200
                hover:before:opacity-100"
            >
              Portfolio
              <img
                src="/assets/redirect-icon.png"
                alt="Redirect Icon"
                className="ml-1 h-3.5 w-3.5 [filter:brightness(0)_saturate(100%)_invert(79%)_sepia(43%)_saturate(746%)_hue-rotate(123deg)_brightness(96%)_contrast(91%)]"
              />
            </a>
          </div>
          {chats.length === 0 ? (
            <div className="mt-16 flex flex-col items-center justify-center px-4 md:px-2">
              <div
                className="flex h-20 w-20 rotate-3 transform items-center justify-center rounded-3xl border border-border bg-surface shadow-shell transition-transform
                  hover:-rotate-5"
              >
                <TerminalIcon />
              </div>
              <h2 className="mt-4 text-3xl font-extrabold text-primary">
                {ASK_VERITAS}
              </h2>
              <p className="mt-2 mb-6 w-full text-lg font-semibold text-secondary">
                {INTRO_MESSAGE}
              </p>
              <div className="grid w-full grid-cols-1 gap-x-8 gap-y-3 md:gap-y-6 sm:grid-cols-2">
                {SUGGESTED_QUERIES.map((query, idx) => (
                  <button
                    key={idx}
                    className="group flex w-full cursor-pointer items-center justify-between rounded-xl border border-border bg-surface px-4 py-4 text-left font-semibold
                      text-text shadow-card transition-all duration-200 hover:border-border-strong hover:text-primary hover:shadow-glow disabled:cursor-not-allowed
                      disabled:opacity-50 disabled:hover:border-border disabled:hover:shadow-card disabled:hover:text-text md:min-w-72"
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
          <div className="fixed bottom-0 w-full px-8 py-8 md:px-4">
            <div className="mx-auto max-w-2xl rounded-3xl border border-border bg-surface/90 p-3 shadow-shell backdrop-blur-xl">
              <form onSubmit={handleSubmit} className="mx-auto flex gap-2">
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
                  className="w-full rounded-lg border border-border bg-panel px-4 py-2 text-[16px] font-medium text-primary placeholder:text-muted transition-colors
                    duration-100 ease-in-out focus:border-border-strong focus:outline-none focus:ring-1 focus:ring-border-strong disabled:cursor-not-allowed"
                  disabled={!isActive}
                />
                {isActive && (
                  <button
                    type="submit"
                    className={`inline-flex items-center justify-center gap-1 rounded-lg border border-border-strong bg-brand px-4 py-3 font-medium text-app-bg
                      transition-colors duration-100 hover:border-amber-400/80 hover:shadow-glow ${
                        isLoading ? "cursor-progress" : "cursor-pointer"
                      }`}
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
        </div>
      )}
    </>
  );
};
