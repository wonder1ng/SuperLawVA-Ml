// page.tsx
"use client";

import { useState } from "react";
import ResumeIcon from "@/components/icons/Resume";
import StyledInput from "@/components/StyledInput";
import SubmitButton from "@/components/SubmitButton";

function Greet() {
  const [inputValue, setInputValue] = useState("");
  const [inputValue2, setInputValue2] = useState("");

  const isValid = inputValue.trim().length > 0;

  return (
    <div style={{ position: "relative", padding: "5rem" }}>
      {/* input1 스타일 */}
      <StyledInput
        type="text"
        width={300}
        height={3}
        placeholder="이메일을 입력하세요"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />

      {/* input2 스타일 */}
      <StyledInput
        type="text"
        width={500}
        height={10}
        placeholder="이메일을 입력하세요"
        value={inputValue2}
        onChange={(e) => setInputValue2(e.target.value)}
      />

      <SubmitButton disabled={!isValid}>로그인</SubmitButton>
      <SubmitButton width={40} disabled={!isValid}>
        로그인
      </SubmitButton>

      <SubmitButton icon={<ResumeIcon color="#5046e5" />} disabled={true}>
        확인
      </SubmitButton>
    </div>
  );
}

export default Greet;
