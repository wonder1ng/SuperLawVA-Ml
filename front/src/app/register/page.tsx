// page.tsx
"use client";

import { useState, useEffect } from "react";         
import { useRouter } from "next/navigation";
import SubmitButton from "@/components/submitButton";
import StatusIcon from "@/components/icons/Status";
import StyledInput from "@/components/StyledInput";
import BackHeader from "@/components/BackHeader";

function StartPage() {
  const router = useRouter();
  const [emailValue, setEmailValue] = useState("");

  /* ──────────  약관 체크박스  ────────── */
  const [allAgree,       setAllAgree]       = useState(false);  // 전체 동의
  const [termsAgree,     setTermsAgree]     = useState(false);  // 이용 약관
  const [privacyAgree,   setPrivacyAgree]   = useState(false);  // 개인정보
  const [marketingAgree, setMarketingAgree] = useState(false);  // 선택(마케팅)

  /** 전체 동의 토글 */
  const toggleAll = () => {
    const next = !allAgree;
    setAllAgree(next);
    setTermsAgree(next);
    setPrivacyAgree(next);
    setMarketingAgree(next);
  };

  /** 개별 체크 변화 → 전체 동의 상태 자동 보정 */
  useEffect(() => {
    setAllAgree(termsAgree && privacyAgree && marketingAgree);
  }, [termsAgree, privacyAgree, marketingAgree]);

  
  const handleClick = () => {
    router.push("/main");
  };

  return (
    <>
      <div className="h-20 w-full flex flex-col justify-center items-center">
        <StatusIcon className="mt-[1.4rem]" />
      </div>

      <BackHeader to="login">회원가입</BackHeader>

      <main className="flex flex-col items-center mt-[5rem] mx-8 h-auto">

        {/* ──────────  입력 파트  ────────── */}
        <div className="mt-12 flex flex-col gap-8">
          <div className="flex gap-4">
            <StyledInput
              type="email"
              width="25rem"
              fontSize={1.6}
              placeholder="이메일 입력"
              onChange={(e) => setEmailValue(e.target.value)}
            />
            <SubmitButton
              width={8}
              height={3}
              fontSize={1.2}
              fontWeight={600}
              disabled={true}
            >
              인증하기
            </SubmitButton>
          </div>

          <StyledInput
            type="text"
            width="34rem"
            fontSize={1.6}
            placeholder="인증 코드 입력"
            onChange={(e) => setEmailValue(e.target.value)}
          />
          <StyledInput
            type="password"
            width="34rem"
            fontSize={1.6}
            placeholder="대소문자, 숫자, 특수문자 포함 8-14글자 입력"
            onChange={(e) => setEmailValue(e.target.value)}
          />
          <StyledInput
            type="password"
            width="34rem"
            fontSize={1.6}
            placeholder="비밀번호 확인"
            onChange={(e) => setEmailValue(e.target.value)}
          />
          <StyledInput
            type="text"
            width="34rem"
            fontSize={1.6}
            placeholder="이름 입력"
            onChange={(e) => setEmailValue(e.target.value)}
          />
        </div>

        {/* ──────────  약관 파트  ────────── */}
        <div className="bg-mainL mt-16 p-12 w-[36rem] justify-center rounded-[50px] flex flex-col gap-4">
          {/* 전체 동의 */}
          <div className="flex mb-4 gap-4 items-center">
            <input
              type="checkbox"
              className="w-6 h-6"
              checked={allAgree}
              onChange={toggleAll}
            />
            <label className="text-[1.8rem] font-bold">약관 전체 동의</label>
          </div>

          {/* 이용 약관 */}
          <div className="flex gap-4 items-center">
            <input
              type="checkbox"
              className="w-6 h-6"
              checked={termsAgree}
              onChange={(e) => setTermsAgree(e.target.checked)}
            />
            <label className="text-[1.6rem]">
              이용 약관 동의&nbsp;
              <span className="text-main text-[1.2rem]">본문 보기</span>
            </label>
          </div>

          {/* 개인정보 */}
          <div className="flex gap-4 items-center">
            <input
              type="checkbox"
              className="w-6 h-6"
              checked={privacyAgree}
              onChange={(e) => setPrivacyAgree(e.target.checked)}
            />
            <label className="text-[1.6rem]">
              개인정보 수집 및 이용 동의&nbsp;
              <span className="text-main text-[1.2rem]">본문 보기</span>
            </label>
          </div>

          {/* 선택 마케팅 */}
          <div className="flex gap-4 items-center">
            <input
              type="checkbox"
              className="w-6 h-6"
              checked={marketingAgree}
              onChange={(e) => setMarketingAgree(e.target.checked)}
            />
            <label className="text-[1.6rem]">
              마케팅 정보 수신 동의 (선택)&nbsp;
              <span className="text-main text-[1.2rem]">본문 보기</span>
            </label>
          </div>
        </div>

        {/* ──────────  가입 버튼  ────────── */}
        <div className="flex flex-1 items-end mt-28 mb-8">
          <SubmitButton
            disabled={!(termsAgree && privacyAgree)}   // 필수 항목 동의해야 활성화
            onClick={handleClick}
          >
            가입하기
          </SubmitButton>
        </div>
      </main>
    </>
  );
}

export default StartPage;