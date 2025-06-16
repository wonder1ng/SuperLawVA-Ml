// components/ProgressRing.tsx
import { useId } from "react";

interface ProgressRingProps {
  size?: number;
  stroke?: number;
  progress: number;           
  trackColor?: string;        
  from?: string;              
  to?: string;   
  runningLabel?: string;
  doneLabel?: string;             
}

function ProgressRing({
  size = 200,
  stroke = 5,
  progress,
  trackColor = "#E5E7EB",
  from = "#E100FF",        
  to = "#6000FF",
  runningLabel = "진행 중",
  doneLabel = "완료",         
}: ProgressRingProps) {
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - progress / 100);
  const gradId = useId();

  const statusLabel = progress >= 100 ? doneLabel : runningLabel;

  return (
    <svg width={size} height={size} className="block mx-auto">
      {/* 회색 트랙 */}
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={trackColor}
        strokeWidth={stroke}
      />

      {/* 진행선 ─ 그라데이션 */}
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={`url(#${gradId})`}
        strokeWidth={stroke}
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        style={{ transition: "stroke-dashoffset 0.3s ease" }}
      />

      {/* % 숫자 */}
      <text
        x="36%"
        y="50%"
        textAnchor="middle"
        className="font-bold"
        fontSize={size * 0.10}
        fill={from}   
        dominantBaseline="middle"                   
      >
        {progress.toFixed(0)}%
      </text>

      <text
        x="64%"
        y="50%"
        textAnchor="middle"
        fontSize={size * 0.10}
        className="font-bold"
        dominantBaseline={"middle"}
        >
        {statusLabel}
      </text>
      {/* 그라데이션 정의 */}
      <defs>
        <linearGradient id={gradId} x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor={from} />
          <stop offset="100%" stopColor={to} />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default ProgressRing;