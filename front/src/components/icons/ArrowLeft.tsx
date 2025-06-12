"use client";

import { useRouter } from "next/navigation";
import type { MouseEventHandler } from "react";
import IconOptions, { LinkIconProps } from "@/app/types/IconOptions";

const ArrowLeftIcon = ({
  width = 1.5,
  height = 1.5,
  color = "#000000",
  className,
  to,
  onClick,
}: LinkIconProps) => {
  const router = useRouter();

  const handleClick: MouseEventHandler<SVGSVGElement> = (e) => {
    if (onClick) {
      onClick(e); // 외부 핸들러 실행
    } else {
      if (!e.defaultPrevented) {
        if (to) {
          router.push(to); // 지정된 경로로 이동
        } else {
          router.back(); // 경로가 없으면 뒤로가기
        }
      }
    }
  };

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 10 15"
      width={typeof width == "number" ? width + "rem" : width}
      height={typeof height == "number" ? height + "rem" : height}
      color={color}
      fill="none"
      className={className}
      onClick={handleClick}
      role="button"
      style={{ cursor: "pointer" }}
    >
      <path
        d="M8.5 12.5018L1 6.75092L8.5 1"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
};

export default ArrowLeftIcon;
