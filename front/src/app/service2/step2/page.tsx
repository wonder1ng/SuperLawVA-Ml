"use client";
import React, { useState } from "react";
import Step2Popup, { Step2PopupData } from "@/components/step2popup";

const popupData: Step2PopupData[] = [
  {
    title: "제 1조(목적)",
    period: "계약 기간은 2024년 1월 1일부터 2025년 12월 31일까지이다.",
    reason: "계약 목적이 명확하지 않음.",
    result: "계약 목적을 구체적으로 명시함.",
    strategy: "계약 목적을 명확히 하여 분쟁 예방.",
    laws: ["민법 제103조"],
    precedents: ["대법원 2010다12345"]
  },
  {
    title: "제 2조(존속기간)",
    period: "계약 기간은 2024년 7월 1일부터 2026년 6월 30일까지이다.",
    reason: "계약기간이 2년이 넘어가요.",
    result: "계약 기간이 끝나기 전에 해지할 수 없음.",
    strategy: "지연이자율을 명확히 하여 임차인의 예측 가능성 확보.",
    laws: ["소득세법 시행령 제122조 제 1항"],
    precedents: ["서울중앙법 2029가합18", "부산지법 1818가합18"]
  },
  {
    title: "제 3조(용도 변경)",
    period: "계약 기간은 2024년 3월 1일부터 2025년 2월 28일까지이다.",
    reason: "용도 변경에 대한 제한이 없음.",
    result: "용도 변경 시 사전 동의 필요.",
    strategy: "용도 변경 조건을 명확히 하여 분쟁 예방.",
    laws: ["상가건물 임대차보호법 제10조"],
    precedents: ["대법원 2015다67890"]
  },
  // ... 필요시 더 추가
];

const StatusIndicator = ({ status }: { status: "ok" | "check" }) => {
  const color = status === "ok" ? "#32D74B" : "#FF9400";
  return (
    <span
      className="w-3 h-3 rounded-full"
      style={{ backgroundColor: color }}
    />
  );
};

const BackTopIcon = ({ className = "", style = {} }: { className?: string; style?: React.CSSProperties }) => (
  <img src="/back_top.svg" alt="back" className={className} style={style} draggable={false} />
);

const MoreDocIcon = ({ className = "", style = {} }: { className?: string; style?: React.CSSProperties }) => (
  <img src="/more_doc.svg" alt="more" className={className} style={style} draggable={false} />
);

const ArticleItem = ({ title, status, onClick }: { title: string; status: "ok" | "check"; onClick: () => void }) => (
  <div onClick={onClick} className="flex items-center w-[353px] h-[46px] bg-white/75 border border-[#f3f4f6] rounded-2xl px-5 mx-auto cursor-pointer">
    <StatusIndicator status={status} />
    <span className="ml-4 text-[14px] font-medium text-black/70">{title}</span>
    <span className="ml-auto flex items-center">
      <MoreDocIcon className="w-6 h-6 align-middle" />
    </span>
  </div>
);

export default function ContractAnalysisPage() {
    const [popupIndex, setPopupIndex] = useState<number|null>(null);

    const openPopup = (idx: number) => {
        setPopupIndex(idx);
    };
    const closePopup = () => {
        setPopupIndex(null);
    };
    const goPrev = () => {
        if (popupIndex !== null && popupIndex > 0) setPopupIndex(popupIndex - 1);
    };
    const goNext = () => {
        if (popupIndex !== null && popupIndex < popupData.length - 1) setPopupIndex(popupIndex + 1);
    };

  return (
    <div className="w-[393px] h-[852px] mx-auto bg-[#f2f1f6] font-['Pretendard'] flex flex-col relative overflow-hidden">
      {/* Header */}
      <header className="absolute top-0 left-0 right-0 h-[117px] z-20">
        <div className="absolute inset-0 bg-white/20 backdrop-blur-sm" />
        <div className="relative flex items-center h-full px-[24px] pb-[18px]" style={{gap:10}}>
          <BackTopIcon className="w-6 h-6 min-w-[24px] min-h-[24px]" />
          <h1 className="text-[16px] font-bold ml-3">계약서 분석 결과</h1>
        </div>
      </header>
      
      {/* Spacer for header */}
      <div className="h-[117px] flex-shrink-0"/>

      <main className="flex-grow flex flex-col">
        {/* Status Legend */}
        <div className="flex justify-center my-8">
            <div className="flex items-center gap-6 bg-white/90 rounded-full px-5 py-3 text-sm shadow-sm border border-gray-200/80">
                <div className="flex items-center gap-2">
                    <StatusIndicator status="ok" />
                    <span className="text-[#32D74B] text-[14px] font-medium tracking-tighter">-문제 없음</span>
                </div>
                <div className="flex items-center gap-2">
                    <StatusIndicator status="check" />
                    <span className="text-[#FF9400] text-[14px] font-medium tracking-tighter">-확인 필요</span>
                </div>
            </div>
        </div>

        {/* Article List */}
        <div className="flex-grow bg-white/70 rounded-t-[40px] border border-b-0 border-[#f3f4f6] pt-5 pb-24 overflow-hidden">
            <div className="flex items-center justify-center mb-7">
                <h2 className="text-[18px] font-semibold text-center">계약 조항 목록</h2>
            </div>
            <div className="h-full overflow-y-auto space-y-3 pb-8">
                {popupData.map((article, index) => (
                    <ArticleItem key={index} title={article.title} status={index % 2 === 0 ? "ok" : "check"} onClick={() => openPopup(index)} />
                ))}
            </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="absolute bottom-0 left-0 right-0 h-[96px] z-20">
        <div className="absolute inset-0 bg-white/20 backdrop-blur-sm" />
        <div className="relative flex justify-center items-center h-full">
            <div className="flex items-center justify-center w-[320px] h-[50px] bg-white border border-[#d6d6d6] rounded-full shadow-lg px-4">
               <span className="text-[18px] font-semibold text-[#0e0e0e]">
                    🔍 계약 조항 분석 결과
               </span>
            </div>
        </div>
      </footer>
      
      {/* Popup Modal */}
      {popupIndex !== null && (
          <div className="absolute inset-0 z-30 flex items-center justify-center">
              <div 
                  className="absolute inset-0 bg-black/30 backdrop-blur-sm"
                  onClick={closePopup}
              />
              <div className="relative w-[340px] h-[800px]">
                 <Step2Popup
                    data={popupData[popupIndex]}
                    onClose={closePopup}
                    onPrev={goPrev}
                    onNext={goNext}
                    showPrev={popupIndex > 0}
                    showNext={popupIndex < popupData.length - 1}
                 />
              </div>
          </div>
      )}

    </div>
  );
}