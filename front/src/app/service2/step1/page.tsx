"use client";

import React from "react";

export default function Step1Page() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white">
      <div className="mt-32 flex flex-col items-center w-full">
        <div className="text-[2.2rem] font-bold text-black text-center leading-tight">
          AI가 계약서를 분석 중 입니다
        </div>
        <div className="mt-4 text-[1.15rem] text-[#555] text-center font-normal">
          계약서가 안전한지 AI가 꼼꼼히 검토해 드릴게요!
        </div>
        <div className="mt-16 flex flex-col items-center">
          <svg width="280" height="280" viewBox="0 0 280 280" className="block">
            <circle
              cx="140"
              cy="140"
              r="130"
              fill="none"
              stroke="#e0e0e0"
              strokeWidth="6"
            />
            <circle
              cx="140"
              cy="140"
              r="130"
              fill="none"
              stroke="url(#gradient)"
              strokeWidth="6"
              strokeDasharray={2 * Math.PI * 130}
              strokeDashoffset={(2 * Math.PI * 130) * (1 - 0.14)}
              strokeLinecap="round"
              transform="rotate(-90 140 140)"
            />
            <defs>
              <linearGradient id="gradient" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#5046e5" />
                <stop offset="100%" stopColor="#9134eb" />
              </linearGradient>
            </defs>
            <text
              x="50%"
              y="50%"
              textAnchor="middle"
              dominantBaseline="middle"
              fontSize="2.2rem"
              fontWeight="bold"
              fill="url(#gradient)"
            >
              14%
            </text>
            <text
              x="50%"
              y="58%"
              textAnchor="middle"
              fontSize="1.35rem"
              fontWeight="bold"
              fill="#222"
            >
              진행 중
            </text>
          </svg>
          <div className="mt-6 text-[1.1rem] text-[#555]">특약 분석 중....</div>
        </div>
      </div>
    </div>
  );
}
