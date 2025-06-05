"use client";

import { useRouter } from "next/navigation";
import type { MouseEventHandler } from "react";
import IconOptions, { LinkIconProps } from "@/app/types/IconOptions";

const ArrowLeftIcon = ({
  width = 30,
  height = 30,
  color = "#000000",
  className,
  to,
  onClick,
}: LinkIconProps) => {
  const router = useRouter();

  const handleClick: MouseEventHandler<SVGSVGElement> = (e) => {
    if (onClick) {
      onClick(e); // 외부 핸들러 실행
    }

    if (!e.defaultPrevented) {
      if (to) {
        router.push(to); // 지정된 경로로 이동
      } else {
        router.back(); // 경로가 없으면 뒤로가기
      }
    }
  };

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      width={width}
      height={height}
      color={color}
      fill="none"
      className={className}
      onClick={handleClick}
      role="button"
      style={{ cursor: "pointer" }}
    >
      <path
        d="M15 6C15 6 9.00001 10.4189 9 12C8.99999 13.5812 15 18 15 18"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
};

export default ArrowLeftIcon;
