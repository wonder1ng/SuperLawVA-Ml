// page.tsx
"use client";

import { useRouter } from "next/navigation";
import SubmitButton from "@/components/SubmitButton";
import styled from "styled-components";
import ArrowLeftIcon from "@/components/icons/ArrowLeft";
import StatusIcon from "@/components/icons/Status";
import KakaoIcon from "@/components/icons/sns/Kakao";
import StyledInput from "@/components/StyledInput";
import { useState } from "react";
import GoogleIcon from "@/components/icons/sns/Google";
import NaverIcon from "@/components/icons/sns/Naver";
import AppleIcon from "@/components/icons/sns/Apple";

// 큰 제목 - 그라데이션 텍스트
const GradientTitle = styled.span`
  font-weight: 700;
  font-size: 3rem;
  line-height: 120%;

  background: linear-gradient(180deg, #5046e5 50%, #9134eb 143.75%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
`;

const SubText = styled.p`
  font-weight: 500;
  font-size: 1.6rem;
  line-height: 120%;
  color: #0f0f0f;
`;

function StartPage() {
  const router = useRouter();
  const [emailValue, setemailValue] = useState("");

  const handleClick = () => {
    router.push("/login");
  };
  return (
    <>
      <div className="flex flex-col justify-center items-center h-20">
        <StatusIcon className="mt-[1.4rem]" />
      </div>
      <div className="mx-8 h-24 flex justify-center items-end relative">
        <ArrowLeftIcon
          width={"3rem"}
          height={"3rem"}
          className="relative -left-[16.8rem]"
        />
      </div>
      <main className="flex flex-col items-center mt-[3.6rem] mx-8">
        <div className="flex flex-col text-center text-main font-sans">
          <div className="font-bold text-[4rem] leading-[120%] ">Super</div>
          <div className="font-black text-[5rem] leading-[120%]">LAWVA</div>
        </div>
        <div className="mt-12 flex flex-col gap-8">
          <div className="flex flex-col gap-4 text-[1.4rem]">
            <span className="font-medium">이메일 주소</span>
            <StyledInput
              type="email"
              placeholder="super@lvw.com"
              onChange={(e) => setemailValue(e.target.value)}
            />
          </div>
          <div className="flex flex-col gap-4 text-[1.4rem]">
            <span className="font-medium">비밀번호</span>
            <StyledInput
              type="password"
              placeholder="대소문자, 숫자, 특수문자 포함하여 8글자 이상"
              onChange={(e) => setemailValue(e.target.value)}
            />
          </div>
          <div className="flex items-center gap-10">
            <div className="flex gap-4">
              <input type="checkbox" name="" id="" className="w-6 h-6" />
              <label htmlFor="" className="text-[1.2rem]">
                아이디 저장
              </label>
            </div>
            {/* checkbox 커스텀 코드 */}
            {/* <div className="grid items-center justify-center">
              <input
                type="checkbox"
                className="peer col-start-1 row-start-1 w-8 h-8 appearance-none rounded border-2 border-gray-300 checked:border-main checked:bg-main dark:border-gray-600 dark:checked:border-main forced-colors:appearance-auto"
              />
              <svg
                viewBox="0 0 14 14"
                fill="none"
                className="invisible col-start-1 row-start-1 stroke-black peer-checked:visible dark:text-violet-300 forced-colors:hidden pointer-events-none"
              >
                <path
                  d="M3 8L6 11L11 3.5"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  stroke="#ffffff"
                ></path>
              </svg>
            </div> */}

            <div className="flex gap-4">
              <input type="checkbox" name="" id="" className="w-6 h-6" />
              <label htmlFor="" className="text-[1.2rem]">
                자동 로그인
              </label>
            </div>
          </div>
          <div className="mt-8 flex justify-center" onClick={handleClick}>
            <SubmitButton>로그인</SubmitButton>
          </div>
          <div className="flex justify-center gap-4 text-l font-medium">
            <span>아이디 찾기</span>|<span>비밀번호 찾기</span>|
            <span>회원가입</span>
          </div>
        </div>
        <div className="flex flex-col justify-center items-center gap-8">
          <div className="mt-16 flex items-center gap-4 text-xl">
            <hr className="w-44 border-[#797979]" />
            <span>SNS 계정으로 로그인</span>
            <hr className="w-44 border-[#797979]" />
          </div>
          <div className="flex flex-row gap-12">
            <KakaoIcon />
            <GoogleIcon />
            <NaverIcon />
            <AppleIcon />
          </div>
        </div>
      </main>
    </>
  );
}

export default StartPage;
