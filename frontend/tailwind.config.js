module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: { extend: {
    colors: { ink: "#3b9eff", paper: "#04101f", flag: "#f5b942", panel: "#08142a", line: "#1c3a68", night: "#050b18" },
    fontFamily: { mono: ['"IBM Plex Mono"', "ui-monospace", "monospace"] },
  } },
  plugins: [],
};
