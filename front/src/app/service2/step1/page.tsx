"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ProgressRing from "@/components/ProgressRing";
import SubmitButton from "@/components/submitButton";
import Image from "next/image";

export default function LoadingPage() {
  const router = useRouter();
  const [progress, setProgress] = useState(0);

  /* 데모용 진행률 (2 → 100 %) */
  useEffect(() => {
    const id = setInterval(() => {
      setProgress((p) => Math.min(p + 2, 100));
    }, 120);
    return () => clearInterval(id);
  }, []);

  const goNext = () => router.push("/service2/step2");

  return (
    <main className="min-h-screen flex flex-col items-center px-6 text-center">
      <div>
        {progress < 100 ? (
          <>
            <h1 className="mt-70 text-[2rem] font-bold mb-2">
              AI가 계약서를 분석 중 입니다
            </h1>
            <p className="text-[1.4rem] font-medium">
              계약서가 안전한지 AI가 꼼꼼히 검토해 드릴게요!
            </p>
          </>
        ) : (
          <>
            <h1 className="mt-70 text-[2rem] font-bold mb-2">
              계약서 분석 완료!
            </h1>
            <p className="text-[1.4rem] font-medium">
              AI가 꼼꼼하게 분석한 계약서 보러 가실까요?
            </p>
          </>
        )}
      </div>

      <div className="mt-25 flex flex-col items-center">
        <ProgressRing
          size={200}
          stroke={5}
          progress={progress}
          from="#6040FF"
          to="#E100FF"
          runningLabel="진행 중"
          doneLabel="완료"
        />

        {/* 진행 중 상태에서만 표시 */}
        {progress < 100 && (
          <p className="mt-4 text-[1.1rem] text-[#555]">특약 분석 중...</p>
        )}
      </div>

      {progress >= 100 && (
        <div className="mt-45">
          <SubmitButton
            width={30}
            height={5.5}
            fontSize={1.7}
            onClick={goNext}
          >
            결과 보기
          </SubmitButton>
        </div>
      )}

      {/* ───── 경고 배너 ───── */}
      <div className="fixed bottom-1 mb-20 w-[90%] font-bold h-20 bg-[#fefce8] rounded-[20px] pl-5 pt-3 gap-2 text-sm flex items-start">
        <Image
          src="/warning.png"
          alt="warningIcon"
          width={27}
          height={26}
          className="flex-shrink-0 mt-2"
        />
        <div>
          <p className="text-[1.2rem] text-start">경고</p>
          <span className="text-subText font-normal">
            본 결과는 법령·사례 기반 학습된 AI로, 잘못된 답변을 낼 수도 있습니다.
          </span>
        </div>
      </div>
    </main>
  );
}