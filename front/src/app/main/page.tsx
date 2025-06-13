"use client";

import { useRouter } from "next/navigation";
import Image from "next/image";
import StyledInput from "@/components/StyledInput";
import { useState } from "react";
import AlarmIcon from "@/components/icons/Alarm";
import DocumentIcon from "@/components/icons/Document";
import AnalyzeIcon from "@/components/icons/Analyze";
import InfoIcon from "@/components/icons/Info";
import UploadIcon from "@/components/icons/Upload";
import BottomNav from '@/components/BottomNav';

interface QuickButtonProps {
  bgc: string;
  icon: React.ReactNode;
  title: string;
  description: string;
}

function QuickButton({ bgc, icon, title, description }: QuickButtonProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div
        className="w-[60px] h-[60px] rounded-[20px] flex items-center justify-center"
        style={{ backgroundColor: bgc }}
      >
        {icon}
      </div>
      <div className="text-[12px] text-[#000000] font-semibold">{title}</div>
      <div className="text-[10px] text-[#4E4E4E] font-regular">{description}</div>
    </div>
  );
}

function StartPage() {
  const router = useRouter();
  const [emailValue, setEmailValue] = useState("");

  return (
    <div className="w-full relative bg-[#f2f1f6] min-h-screen overflow-hidden">
      <div className="fixed top-0 left-0 right-0 z-50 flex justify-center pt-[56px] pb-4">
        <div className="relative w-[360px] h-[60px] text-left text-[20px] font-pretendard">
          <div className="absolute top-0 left-0 rounded-[50px] bg-white border border-[#f3f4f6] box-border w-[360px] h-[60px] backdrop-blur-[4px]" />
          <div className="absolute top-[calc(50%-13px)] left-[calc(50%-160px)] w-[200px] h-[24px] flex items-center gap-3">
            <Image
              src="/lovalogo.svg"
              alt="Super Lawva Logo"
              width={24}
              height={12}
              className="object-contain"
            />
            <div className="tracking-[-0.04em] leading-[120%] font-semibold bg-gradient-to-r from-[#6000ff] to-[#e100ff] bg-clip-text text-transparent whitespace-nowrap">
              Super Lawva
            </div>
          </div>
          <div className="absolute top-[18px] left-[316px] rounded-full bg-[#6000ff] w-[24px] h-[24px]" />
          <div className="absolute top-[20px] left-[276px]">
            <AlarmIcon />
          </div>
        </div>
      </div>

      <main className="w-full flex flex-col items-center pt-[140px] h-screen overflow-y-auto">
        <div className="self-start mx-9 text-[20px] font-bold text-black mb-[30px]">
          아무개 님의 고민
          <br />'<span className="text-[#6000ff]">로바</span>'에서 도와드릴게요!
        </div>

        <div className="w-full">
          <div className="w-full h-[692px] rounded-t-[50px] bg-white/70 border border-[#f3f4f6]">
            <div className="w-full px-6 pt-6">
              <div className="relative w-[342px] h-[44px] mx-auto">
                <div className="absolute top-0 left-0 w-[342px] h-[44px] rounded-[43.5px] bg-[#f3f4f6]" />
                <div className="absolute top-[7px] left-[262px] w-[70px] h-[30px] rounded-[43.5px] bg-[#6000ff]" />
                <div className="absolute top-[16px] left-[286px] text-[12px] leading-[100%] font-medium text-white font-['Noto_Sans_KR']">
                  검색
                </div>
                <div className="absolute top-[15px] left-[32px] text-[14px] leading-[100%] font-medium text-[#9ca3af] font-pretendard">
                  무엇을 도와드릴까요?
                </div>
                <div className="absolute top-[15px] left-[12px]">
                  <Image
                    src="/search.svg"
                    alt="Search"
                    width={14}
                    height={14}
                    className="object-contain"
                  />
                </div>
              </div>

              <div className="w-full px-9 mt-[30px]">
                <div className="text-[18px] font-semibold text-black mb-[30px]">빠른 작업</div>
                <div className="relative w-[311px] h-[91px] mx-auto">
                  <div className="absolute top-0 left-[117px] w-[74px] h-[91px]">
                    <div 
                      className="absolute top-0 left-[7px] w-[60px] h-[60px] rounded-[20px] bg-[#0a84ff] flex items-center justify-center cursor-pointer"
                      onClick={() => router.push('/main/document')}
                    >
                      <AnalyzeIcon color="white" />
                    </div>
                    <div className="absolute top-[66px] left-[calc(50%-27px)] text-[12px] font-semibold text-black text-center w-[55px] leading-[110%] whitespace-nowrap">
                      계약서 분석
                    </div>
                    <div className="absolute top-[82px] left-[calc(50%-37px)] text-[8px] text-[#4e4e4e] text-center w-[74px] leading-[110%] whitespace-nowrap">
                      계약을 검토하고 싶어요
                    </div>
                  </div>
                  <div className="absolute top-0 left-[240px] w-[60px] h-[91px]">
                    <div className="absolute top-0 left-0 w-[60px] h-[60px] rounded-[20px] bg-[#ff453a] flex items-center justify-center">
                      <InfoIcon color="white" />
                    </div>
                    <div className="absolute top-[66px] left-[9px] text-[12px] font-semibold text-black text-center w-[42px] leading-[110%] whitespace-nowrap">
                      내용증명
                    </div>
                    <div className="absolute top-[82px] left-[1px] text-[8px] text-[#4e4e4e] text-center w-[58px] leading-[110%] whitespace-nowrap">
                      문제가 발생했어요
                    </div>
                  </div>
                  <div 
                    className="absolute top-0 left-0 w-[67px] h-[91px] cursor-pointer"
                    onClick={() => router.push('/contract/create')}
                  >
                    <div className="absolute top-0 left-[3px] w-[60px] h-[60px] rounded-[20px] bg-[#32d74b] flex items-center justify-center">
                      <DocumentIcon color="white" />
                    </div>
                    <div className="absolute top-[66px] left-[6px] text-[12px] font-semibold text-black text-center w-[55px] leading-[110%] whitespace-nowrap">
                      계약서 작성
                    </div>
                    <div className="absolute top-[82px] left-0 text-[8px] text-[#4e4e4e] text-center w-[67px] leading-[110%] whitespace-nowrap">
                      새로운 계약을 작성해요
                    </div>
                  </div>
                </div>
              </div>

              <div className="w-full px-9 mt-[30px]">
                <div className="text-[18px] font-semibold text-black mb-[30px]">내 계약서</div>
                <div className="relative w-[286px] h-[60px] mx-auto">
                  <div 
                    className="absolute top-0 left-0 w-full h-full rounded-[20px] bg-[#780aff] flex flex-col items-center justify-center cursor-pointer"
                    onClick={() => router.push('/main/document')}
                  >
                    <UploadIcon width={1.2} height={1.4} color="white" className="mb-1" />
                    <span className="text-[12px] font-semibold text-white whitespace-nowrap">계약서 업로드</span>
                  </div>
                </div>
                <div className="mt-4 text-center">
                  <span className="text-[10px] font-medium bg-gradient-to-r from-[#6000ff]/70 to-[#e100ff]/70 bg-clip-text text-transparent whitespace-nowrap">
                    서비스를 이용하려면 파일을 업로드해주세요!
                  </span>
                </div>
              </div>

              <div className="w-full px-9 mt-[30px]">
                <div className="text-[18px] font-semibold text-black mb-[30px]">최근 상담 내용</div>
                <div className="flex flex-col justify-center items-center gap-4">
                  <div className="flex flex-col justify-center items-center gap-4 opacity-70">
                    <Image
                      src="/chatbot.png"
                      alt="No recent consultations"
                      width={101}
                      height={101}
                      className="object-contain"
                    />
                    <span className="text-[12px] font-medium text-black">
                      최근 상담 내용이 없어요
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* 하단 네비게이션 바 */}
      <BottomNav />
    </div>
  );
}

export default StartPage;
