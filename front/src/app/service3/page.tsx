// page.tsx
"use client";

import CheckedIcon from "@/components/icons/Checked";
import DocumentIcon from "@/components/icons/Document";
import Modal from "@/components/Modal";
import StyledDiv from "@/components/StyledDiv";
import SubmitButton from "@/components/submitButton";
import { useRouter } from "next/navigation";
import { useState } from "react";

function StartPage() {
  const router = useRouter();
  const [modalOpen, setModalOpen] = useState(false);

  const [selected, setSelected] = useState<number | null>(null);
  const handleSelect = (index: number) => {
    setSelected((prev) => (prev === index ? null : index));
  };

  const handleClick = () => {
    router.push("/login");
  };
  return (
    <>
      <main className="flex flex-col items-center h-full bg-white">
        <div className="h-52 w-full" />
        <StyledDiv
          width={15.2}
          height={3.4}
          background="rgba(50, 215, 75, 0.2)"
          fontSize={1.2}
          fontColor="#32d74b"
          fontWeight={700}
          borderColor="none "
          icon={<DocumentIcon width={1.4} height={1.4} color="#32d74b" />}
        >
          AI로 계약서 분석하기
        </StyledDiv>
        <div className="mt-8 text-center text-[2.6rem]/[3.1rem] font-bold">
          AI분석으로
          <br />
          분쟁을 미리 예방하세요
        </div>
        <img
          src="/survice2_start_icon.png"
          alt="Main Icon"
          className="w-[26.5rem] h-[26.5rem] mt-16"
        />
        <div className="mt-16 text-center text-[1.2rem] font-medium">
          당신의 계약서는 안전해야 하니까.
          <br />
          AI가 당신의 계약을 도와드릴게요
        </div>
        <SubmitButton
          width={26}
          height={5.5}
          fontSize={1.8}
          className="mt-16"
          onClick={() => setModalOpen(true)}
        >
          시작하기
        </SubmitButton>
      </main>
      <Modal
        isOpen={modalOpen}
        setIsOpen={setModalOpen}
        clickOutsideClose={true}
      >
        <div className="w-[393px] h-[463px] relative">
          <div className="absolute top-0 left-0 w-full h-full rounded-[50px_50px_0_0] bg-white border border-[#f3f4f6]" />
          <img 
            src="/model_top.svg" 
            alt="handle" 
            className="absolute top-[10px] left-[171px] w-[46px] rounded-[20px]"
          />
          <div className="absolute top-[107px] left-[53px] w-[287px] h-[95px] rounded-[20px] bg-white border-[1.5px] border-[#c6c6c8] box-border" />
          <div className="absolute top-[165px] left-[120px] text-[16px] font-medium text-black">부동산임대차계약서.pdf</div>
          <div className="absolute top-[45px] left-[80px] text-[20px] font-bold text-[#0f0f0f]">분석할 계약서를 확인해주세요</div>
          
          <div className="absolute top-[234px] left-[64px] text-[16px]">계약 유형</div>
          <div className="absolute top-[235px] left-[218px] text-[14px] text-[#5c5c5c]">부동산(전세) 계약서</div>
          
          <div className="absolute top-[284px] left-[64px] text-[16px]">계약 일자</div>
          <div className="absolute top-[285px] left-[218px] text-[14px] text-[#5c5c5c]">2018.18.28</div>
          
          <div className="absolute top-[330px] left-[64px] text-[16px]">건물 유형</div>
          <div className="absolute top-[331px] left-[218px] text-[14px] text-[#5c5c5c]">오피스텔</div>
          
          <div className="absolute top-[384px] left-[208px] w-[160px] h-[50px]">
            <div className="absolute top-0 left-0 w-[160px] h-[50px] rounded-[30px] bg-[#6000ff]" />
            <div 
              className="absolute top-[17px] left-[48px] text-[16px] leading-[100%] text-white font-medium cursor-pointer"
              onClick={() => router.push('/service2/step1')}
            >
              네,맞아요
            </div>
          </div>
          
          <div className="absolute top-[384px] left-[26px] w-[160px] h-[50px]">
            <div className="absolute top-0 left-0 w-[160px] h-[50px] rounded-[30px] bg-white border border-[#5c5c5c] box-border" />
            <div className="absolute top-[17px] left-[41px] text-[16px] leading-[100%] text-[#1e1e1e] font-medium">다시 업로드</div>
          </div>
          
          <img 
            src="/file.svg" 
            alt="icon" 
            className="absolute top-[27.65%] left-[47.84%] w-[18px] h-[20px]"
          />
        </div>
      </Modal>
    </>
  );
}
export default StartPage;

