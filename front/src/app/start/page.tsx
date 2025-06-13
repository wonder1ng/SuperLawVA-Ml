// page.tsx
"use client";

import { useRouter } from "next/navigation";
import Image from "next/image";

export default function StartPage() {
  const router = useRouter();

  const handleClick = () => {
    router.push("/login");
  };

  return (
    <div className="w-full relative bg-white h-[852px] overflow-hidden text-left text-[40px] text-black font-pretendard">
      <div className="absolute top-[calc(50%-52px)] left-[calc(50%-111.5px)] tracking-[-0.04em] leading-[120%] font-semibold">
        Super Lawva
      </div>
      
      <div 
        className="absolute top-[722px] left-[36px] rounded-[30px] bg-[#6000ff] w-[320px] h-[50px] cursor-pointer flex items-center justify-center"
        onClick={handleClick}
      >
        <div className="text-[18px] leading-[120%] font-medium text-white whitespace-nowrap">
          시작하기
        </div>
      </div>

      <div className="absolute top-[437px] left-[calc(50%-132.5px)] text-[17px] leading-[120%] text-center">
        <p className="m-0">임대차 계약, 분쟁 대신 분석을.</p>
        <p className="m-0">쉬운 계약서 분석과 Ai 기반 명확한 분석.</p>
      </div>

      <div className="absolute top-[314px] left-[163px]">
        <Image
          src="/lovalogo.svg"
          alt="Super Lawva Logo"
          width={66}
          height={33}
          className="object-cover"
          priority
        />
      </div>
    </div>
  );
}
