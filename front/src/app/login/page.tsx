// page.tsx
"use client";

import { useRouter } from "next/navigation";
import Image from "next/image";
import styled from "styled-components";
import StatusIcon from "@/components/icons/Status";
import KakaoIcon from "@/components/icons/sns/Kakao";
import StyledInput from "@/components/StyledInput";
import { useState } from "react";
import KakaoIcon from "@/components/icons/sns/Kakao";
import GoogleIcon from "@/components/icons/sns/Google";
import NaverIcon from "@/components/icons/sns/Naver";
import AppleIcon from "@/components/icons/sns/Apple";
import PasswordVisibilityIcon from "@/components/icons/PasswordVisibility";
import BackHeader from "@/components/BackHeader";
import SubmitButton from "@/components/SubmitButton";

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

export default function LoginPage() {
  const router = useRouter();
  const [emailValue, setemailValue] = useState("");
  const [passwordValue, setPasswordValue] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="w-full relative bg-white h-[852px] overflow-hidden text-center text-[14px] text-[#86868b] font-pretendard">
      <div className="absolute top-[calc(50%-250.86px)] left-[calc(50%-111.5px)] text-[40px] tracking-[-0.04em] leading-[120%] font-semibold text-black text-left">
        Super Lawva
      </div>

      <div className="absolute top-[125px] left-[163px]">
        <Image
          src="/lovalogo.svg"
          alt="Super Lawva Logo"
          width={66}
          height={33}
          className="object-cover"
          priority
        />
      </div>

      <div className="absolute top-[277px] left-[calc(50%-160.5px)] text-[17px] leading-[17px] font-medium text-black">
        이메일을 입력해주세요.
      </div>

      <div className="absolute top-[304px] left-[calc(50%-160.5px)] w-[321px]">
        <StyledInput
          type="email"
          placeholder="super@lvw.com"
          onChange={(e) => setemailValue(e.target.value)}
        />
      </div>

      <div className="absolute top-[351px] left-[calc(50%-160.5px)] text-[17px] leading-[17px] font-medium text-black">
        비밀번호를 입력해주세요.
      </div>

      <div className="absolute top-[379px] left-[calc(50%-160.5px)] w-[321px] relative">
        <StyledInput
          type={showPassword ? "text" : "password"}
          placeholder="대소문자, 숫자, 특수문자 포함하여 8글자 이상"
          onChange={(e) => setPasswordValue(e.target.value)}
        />
        <div className="absolute right-4 top-1/2 -translate-y-1/2 cursor-pointer" onClick={togglePasswordVisibility}>
          <PasswordVisibilityIcon width={16} height={16} isVisible={showPassword} />
        </div>
      </div>

      <div className="absolute top-[439px] left-[calc(50%-160px)] rounded-[30px] bg-[#eaeaea] w-[320px] h-[50px] cursor-pointer">
        <div className="absolute top-[15px] left-[calc(50%-23.5px)] text-[18px] leading-[120%] font-medium text-white">
          로그인
        </div>
      </div>

      <div className="absolute top-[503px] left-[calc(50%-89.5px)] text-[14px] tracking-[-0.5px] leading-[14px] text-[#0a84ff] underline">
        회원가입
      </div>
      <div className="absolute top-[503px] left-[calc(50%+41.5px)] text-[14px] tracking-[-0.5px] leading-[14px] text-[rgba(0,0,0,0.7)]">
        비밀번호 찾기
      </div>

      <div className="absolute top-[562px] left-[19px] w-[354px] h-[94px] font-noto-sans">
        <div className="absolute top-0 left-[114px] tracking-[-0.5px] leading-[29px] inline-block w-[124px] h-[24px]">
          SNS 계정으로 로그인
        </div>
        <div className="absolute top-[15.5px] left-[-0.5px] bg-[#86868b] border-t border-[#86868b] w-[110px] h-[1px]" />
        <div className="absolute top-[15.5px] left-[244.5px] bg-[#86868b] border-t border-[#86868b] w-[110px] h-[1px]" />
        
        <div className="absolute top-[44px] left-[25px]">
          <KakaoIcon />
        </div>
        <div className="absolute top-[44px] left-[109px]">
          <GoogleIcon />
        </div>
        <div className="absolute top-[44px] left-[193px]">
          <NaverIcon />
        </div>
        <div className="absolute top-[44px] left-[277px]">
          <AppleIcon />
        </div>
      </div>
    </div>
  );
}
