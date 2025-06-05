// page.tsx
"use client";

import SubmitButton from "@/components/SubmitButton";
import { useRouter } from "next/navigation";
import styled from "styled-components";

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

  const handleClick = () => {
    router.push("/login");
  };
  return (
    <>
      <div className="h-20" />
      <main className="flex flex-col items-center w-full mt-52">
        <div className="flex flex-col">
          <span className="font-bold text-[2rem] text-center">
            <GradientTitle>나</GradientTitle>만의{" "}
            <GradientTitle>작</GradientTitle>은{" "}
            <GradientTitle>변</GradientTitle>
            호사
          </span>
          <SubText className="text-center">
            임대차 계약, <span className="text-red-600">분쟁</span> 대신{" "}
            <span className="text-main">분석</span>을.
          </SubText>
        </div>
        <img
          src="img.png"
          alt="Main Icon"
          className="h-[22.5rem] my-[0.6rem]"
        />
        <div className="mt-[8.8rem]" onClick={handleClick}>
          <SubmitButton>시작하기</SubmitButton>
        </div>
      </main>
    </>
  );
}

export default StartPage;
