"use client";
import React from "react";

// 데이터 타입 정의
interface Law {
  law_id: number;
  law: string;
}
interface Case {
  case_id: number;
  case: string;
}
interface Article {
  result: boolean;
  content: string;
  reason?: string;
  suggested_revision?: string;
  negotiation_points?: string;
  legal_basis?: Law;
  case_basis?: Case[];
}
interface Agreement extends Article {}
interface RecommendedAgreement {
  reason?: string;
  suggested_revision: string;
  negotiation_points?: string;
  legal_basis?: Law;
  case_basis?: Case[];
}
interface AnalysisMeta {
  model: string;
  generation_time: number;
  user_agent: string;
  version: string;
}
interface ContractAnalysisData {
  _id: number;
  user_id: number;
  contract_id: number;
  created_date: string;
  articles: Article[];
  agreements: Agreement[];
  recommended_agreements: RecommendedAgreement[];
  analysis_metadata?: AnalysisMeta;
}

// 샘플 데이터 (없으면 안내)
const sampleData: ContractAnalysisData = {
  _id: 123,
  user_id: 123,
  contract_id: 123,
  created_date: "2026-06-30T00:00:00Z",
  articles: [
    {
      result: true,
      content: "계약 기간은 2024년 7월 1일부터 2026년 6월 30일까지이다.",
      reason: "임대인의 안정적 수익 보장.",
      suggested_revision: "계약 기간이 끝나기 전에 해지할 수 없음.",
      negotiation_points: "지연이자율을 명확히 하여 임차인의 예측 가능성 확보",
      legal_basis: { law_id: 123, law: "「주택임대차보호법 시행령」 제22조" },
      case_basis: [
        { case_id: 123, case: "대법원 2019다12345 판결" },
        { case_id: 124, case: "서울고등법원 2018나54321 판결" }
      ]
    }
  ],
  agreements: [
    {
      result: true,
      content: "계약 기간은 2024년 7월 1일부터 2026년 6월 30일까지이다.",
      reason: "임대인의 안정적 수익 보장.",
      suggested_revision: "계약 기간이 끝나기 전에 해지할 수 없음.",
      negotiation_points: "지연이자율을 명확히 하여 임차인의 예측 가능성 확보",
      legal_basis: { law_id: 123, law: "「주택임대차보호법 시행령」 제22조" },
      case_basis: [
        { case_id: 123, case: "대법원 2019다12345 판결" },
        { case_id: 124, case: "서울고등법원 2018나54321 판결" }
      ]
    }
  ],
  recommended_agreements: [
    {
      reason: "임대인의 안정적 수익 보장.",
      suggested_revision: "계약 기간이 끝나기 전에 해지할 수 없음.",
      negotiation_points: "지연이자율을 명확히 하여 임차인의 예측 가능성 확보",
      legal_basis: { law_id: 123, law: "「주택임대차보호법 시행령」 제22조" },
      case_basis: [
        { case_id: 123, case: "대법원 2019다12345 판결" },
        { case_id: 124, case: "서울고등법원 2018나54321 판결" }
      ]
    }
  ],
  analysis_metadata: {
    model: "Claude Sonnet 4",
    generation_time: 42.96,
    user_agent: "Mozila",
    version: "v1.2.3"
  }
};

const colorDot = (color: string) => (
  <span style={{ display: 'inline-block', width: 14, height: 14, borderRadius: '50%', background: color, marginRight: 12, flexShrink: 0, boxShadow: '0 1px 2px #0001' }} />
);

export default function DataCheckPage({ data }: { data?: ContractAnalysisData }) {
  const d = data || sampleData;
  return (
    <div className="w-full min-h-screen bg-[#f7f7fa] flex flex-col items-center py-8 px-2">
      {/* 실제 서비스 UI */}
      <div className="w-full max-w-[430px] flex flex-col gap-6 mb-8">
        {/* 계약 조항 전체 카드 */}
        <div className="rounded-[28px] bg-white shadow-sm border border-[#f3f4f6] px-2 py-2">
          <h2 className="text-[1.1rem] font-bold text-[#18181b] mb-3 pl-2 pt-2">계약 조항 전체</h2>
          {d.articles.map((item, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between px-3 py-3 rounded-[18px] mb-1 hover:bg-[#f5f5fa] transition"
              style={{ minHeight: 44 }}
            >
              <div className="flex items-center min-w-0">
                {colorDot(item.result ? '#32D74B' : '#FF3B30')}
                <span className="font-semibold text-[1.08rem] text-[#222] truncate" title={item.content}>{item.content}</span>
              </div>
              <button className="ml-2 p-1 rounded-full hover:bg-[#f2f2f7] transition" aria-label="상세보기">
                <span className="text-[1.25rem]" role="img" aria-label="메모">🗒️</span>
              </button>
            </div>
          ))}
        </div>
        {/* 특약사항 카드 */}
        <div className="rounded-[28px] bg-white shadow-sm border border-[#f3f4f6] px-2 py-2">
          <h2 className="text-[1.1rem] font-bold text-[#18181b] mb-3 pl-2 pt-2">특약사항</h2>
          {d.agreements.map((item, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between px-3 py-3 rounded-[18px] mb-1 hover:bg-[#f5f5fa] transition"
              style={{ minHeight: 44 }}
            >
              <div className="flex items-center min-w-0">
                {colorDot(item.result ? '#32D74B' : '#FF3B30')}
                <span className="font-semibold text-[1.08rem] text-[#222] truncate" title={item.content}>{item.content}</span>
              </div>
              <button className="ml-2 p-1 rounded-full hover:bg-[#f2f2f7] transition" aria-label="상세보기">
                <span className="text-[1.25rem]" role="img" aria-label="메모">🗒️</span>
              </button>
            </div>
          ))}
        </div>
        {/* 권고 특약 카드 */}
        <div className="rounded-[28px] bg-white shadow-sm border border-[#f3f4f6] px-2 py-2">
          <h2 className="text-[1.1rem] font-bold text-[#18181b] mb-3 pl-2 pt-2">권고 특약</h2>
          {d.recommended_agreements.map((item, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between px-3 py-3 rounded-[18px] mb-1 hover:bg-[#f5f5fa] transition"
              style={{ minHeight: 44 }}
            >
              <div className="flex items-center min-w-0">
                {colorDot('#FF3B30')}
                <span className="font-semibold text-[1.08rem] text-[#222] truncate" title={item.suggested_revision}>{item.suggested_revision}</span>
              </div>
              <button className="ml-2 p-1 rounded-full hover:bg-[#f2f2f7] transition" aria-label="상세보기">
                <span className="text-[1.25rem]" role="img" aria-label="메모">🗒️</span>
              </button>
            </div>
          ))}
        </div>
      </div>
      {/* 데이터 전체 프리뷰 */}
      <div className="w-full max-w-[430px] bg-white rounded-2xl shadow p-4 mb-8 border border-[#f3f4f6]">
        <h2 className="text-lg font-bold mb-2">데이터 통신 확인</h2>
        <div className="text-xs text-gray-500 mb-2">아래는 실제 전달받은 contractAnalysisData 전체입니다.</div>
        <pre className="bg-[#f5f5fa] rounded p-2 text-xs overflow-x-auto max-h-64 border border-[#eee]">
          {JSON.stringify(d, null, 2)}
        </pre>
        <div className="mt-4 space-y-2">
          <div>📝 <b>articles</b> : {Array.isArray(d.articles) ? d.articles.length : 0}개</div>
          <div>📝 <b>agreements</b> : {Array.isArray(d.agreements) ? d.agreements.length : 0}개</div>
          <div>📝 <b>recommended_agreements</b> : {Array.isArray(d.recommended_agreements) ? d.recommended_agreements.length : 0}개</div>
        </div>
        <div className="mt-4">
          <div className="font-semibold mb-1">articles 첫 항목 미리보기</div>
          <pre className="bg-[#f5f5fa] rounded p-2 text-xs overflow-x-auto border border-[#eee]">
            {d.articles && d.articles[0] ? JSON.stringify(d.articles[0], null, 2) : '없음'}
          </pre>
        </div>
      </div>
      <div className="text-xs text-gray-400">※ 실제 API 연동 시 props로 data만 넘기면 됩니다.</div>
    </div>
  );
}