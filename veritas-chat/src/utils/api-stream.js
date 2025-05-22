import { STREAM_ERROR } from "./constants";

export const fetchStreamedResponse = (query, onData, onDone, onError) => {
  const controller = new AbortController();

  (async () => {
    try {
      const response = await fetch(process.env.NEXT_PUBLIC_VERTITAS_ASK_API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
        signal: controller.signal,
      });

      if (!response.ok) {
        onError?.("Server responded with an error");
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let partial = "";
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        partial += decoder.decode(value, { stream: true });

        const events = partial.split("\n\n");
        partial = events.pop() || "";

        for (const event of events) {
          if (event.startsWith("event: done")) {
            onDone?.();
            return;
          } else if (event.startsWith("event: error")) {
            const message = event.split("data: ")[1];
            onError?.(message);
            return;
          } else if (event.startsWith("data: ")) {
            const data = event.replace("data: ", "");
            onData?.(data);
          }
        }
      }
    } catch (err) {
      onError?.(STREAM_ERROR);
    }
  })();

  return () => controller.abort();
};
