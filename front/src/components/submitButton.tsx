"use client";

import React from "react";

interface SubmitButtonProps {
  width?: number | string;
  height?: number | string;
  fontColor?: string;
  fontSize?: number;
  fontWeight?: number;
  gap?: number;
  background?: string;
  children?: React.ReactNode;
  disabled?: boolean;
  icon?: React.ReactNode;
  className?: string;
  subStyle?: boolean;
}

export default function SubmitButton({
  width = 20,
  height = 5.5,
  fontColor = "#ffffff",
  fontWeight = 700,
  fontSize = 2.2,
  gap = 0.8,
  background,
  disabled = false,
  children,
  icon,
  className,
  subStyle = false,
}: SubmitButtonProps) {
  const baseColor = background || "#5046E5";
  const buttonBg = disabled
    ? "rgba(128, 128, 128, 0.55)"
    : subStyle
    ? "#F7F9FB"
    : baseColor;

  const border = subStyle && !disabled ? "0.14rem solid #5046E5" : "none";
  const color = disabled
    ? "#ffffff"
    : subStyle
    ? "#5046E5"
    : fontColor || "#ffffff";

  return (
    <button
      className={`flex justify-center items-center rounded-full transition-all duration-200 ${className}`}
      disabled={disabled}
      style={{
        width: typeof width === "number" ? `${width}rem` : width,
        height: typeof height === "number" ? `${height}rem` : height,
        background: buttonBg,
        border: border,
        color: color,
        fontWeight: fontWeight,
        fontSize: typeof fontSize === "number" ? `${fontSize}rem` : fontSize,
        lineHeight: "2.6rem",
        gap: typeof gap === "number" ? `${gap}rem` : gap,
        cursor: disabled ? "not-allowed" : "pointer",
        pointerEvents: disabled ? "none" : "auto",
        opacity: disabled ? 0.6 : 1,
      }}
    >
      {icon && <span>{icon}</span>}
      {children}
    </button>
  );
}
