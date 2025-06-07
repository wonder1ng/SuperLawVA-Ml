"use client";

import React from "react";

interface Props {
  width?: number | string;
  fontWeight?: number | string;
  fontSize?: number | string;
  type?: string;
  className?: string;
  placeholder?: string;
  value?: string | number;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function TailwindInput({
  width = "32rem",
  fontWeight = 400,
  fontSize = "1.4rem",
  type = "text",
  className,
  placeholder,
  value,
  onChange,
}: Props) {
  return (
    <div className={`flex flex-col justify-start ${className}`}>
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="bg-transparent border-none px-4 outline-none placeholder:text-gray-400"
        style={{
          width: typeof width === "number" ? `${width}rem` : width,
          fontWeight: fontWeight,
          fontSize: typeof fontSize === "number" ? `${fontSize}rem` : fontSize,
          lineHeight: "2rem",
        }}
      />
      <div
        className="mt-[0.6rem] border-[0.15rem] border-[#bbb6]"
        style={{
          width: typeof width === "number" ? `${width}rem` : width,
        }}
      />
    </div>
  );
}
