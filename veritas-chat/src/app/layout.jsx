import "./globals.css";
import { Nunito, Open_Sans } from "next/font/google";

const nunito = Nunito({
  variable: "--font-nunito",
  subsets: ["latin"],
  weight: ["500", "600", "700", "800"],
});

const openSans = Open_Sans({
  variable: "--font-open-sans",
  subsets: ["latin"],
  weight: ["500", "600", "700", "800"],
});

export const metadata = {
  title: "Vertias AI",
  description: "A RAG model as a personal assistant",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${nunito.variable} ${openSans.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
