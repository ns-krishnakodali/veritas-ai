module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "var(--color-primary)",
        "primary-light": "var(--color-primary-light)",
        placeholder: "var(--color-placeholder)",
        border: "var(--color-border)",
        "chat-bg": "var(--color-chat-bg)",
      },
    },
  },
  plugins: [],
};
