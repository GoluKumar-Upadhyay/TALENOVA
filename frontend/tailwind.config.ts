import type { Config } from "tailwindcss";
export default { content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"], theme: { extend: { colors: { brand: "#1D4ED8", ink: "#102047", mint: "#DFF7E8", peach: "#FFF4E5" }, boxShadow: { soft: "0 14px 38px rgba(25, 78, 216, .10)" } } }, plugins: [] } satisfies Config;

