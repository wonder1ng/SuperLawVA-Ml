"use client";

import CustomStyledProps from "@/app/types/CustomStyledProps";

export default function StyledDiv({
  width = 20,
  height = 5.5,
  fontColor = "#ffffff",
  fontWeight = 700,
  fontSize = 2.2,
  gap = 0.8,
  background = "#6000ff",
  borderRadius = 50,
  borderColor,
  children,
  icon,
  className,
}: CustomStyledProps) {
  const border = borderColor ? "0.15rem solid " + borderColor : "none";

  return (
    <button
      className={`flex justify-center items-center transition-all duration-200 ${className}`}
      style={{
        width: typeof width === "number" ? `${width}rem` : width,
        height: typeof height === "number" ? `${height}rem` : height,
        background: background,
        border: border,
        color: fontColor,
        fontWeight: fontWeight,
        fontSize: typeof fontSize === "number" ? `${fontSize}rem` : fontSize,
        borderRadius:
          typeof borderRadius === "number" ? `${borderRadius}px` : borderRadius,
        lineHeight: "2.6rem",
        gap: typeof gap === "number" ? `${gap}rem` : gap,
      }}
    >
      {icon && <span>{icon}</span>}
      {children}
    </button>
  );
}
