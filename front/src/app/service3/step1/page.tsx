'use client';

import { HiOutlinePencil, HiOutlineInformationCircle, HiOutlineChevronLeft, HiOutlineSparkles } from 'react-icons/hi2';

export default function Service3Step1() {
  return (
    <div className="min-h-screen bg-[#f7f7fa] flex flex-col">
      {/* 상단 헤더 */}
      <header className="flex items-center h-[80px] px-6">
        <HiOutlineChevronLeft className="w-7 h-7 mr-2" />
        <span className="text-[22px] font-semibold text-black">내용증명서</span>
      </header>

      {/* 메인 타이틀 */}
      <section className="px-6 mt-2 mb-2">
        <h1 className="text-center text-[32px] font-bold leading-tight">
          <span className="bg-gradient-to-r from-[#6000ff] to-[#e100ff] bg-clip-text text-transparent">법·판례</span>
          <span className="text-black"> 기반으로<br />당신의 내용증명서를 설득력있게</span>
        </h1>
        <p className="mt-4 text-center text-[#b0b0b0] text-[18px] font-medium">
          내용증명: 어떤 내용을 보냈는지 우체국이 공식적으로 증명해 주는 편지
        </p>
      </section>

      {/* 카드 영역 */}
      <section className="flex-1 w-full bg-white rounded-t-[40px] pt-10 px-6 mt-6">
        {/* 상황 입력 */}
        <div>
          <div className="flex items-center mb-3">
            <HiOutlinePencil className="w-6 h-6 text-[#a259ff] mr-2" />
            <span className="text-[22px] font-bold text-black">당신의 상황을 상세히 이야기 해주세요</span>
          </div>
          <div className="bg-[#f7f9fb] rounded-2xl p-5 mb-8">
            <p className="text-[#b0b0b0] text-[18px] leading-relaxed">
              ex)<br />
              계약 종료일이 다가오는데 집주인이 보증금 반환에 대해 아무런 언급이 없습니다.<br />
              연락도 잘 되지 않아서 불안한 상황입니다.
            </p>
          </div>
        </div>

        {/* 요청사항 입력 */}
        <div>
          <div className="flex items-center mb-3">
            <HiOutlineInformationCircle className="w-6 h-6 text-[#a259ff] mr-2" />
            <span className="text-[22px] font-bold text-black">
              요청사항이 있으신가요?
              <span className="text-[#b0b0b0] text-[18px] font-medium ml-1">(선택)</span>
            </span>
          </div>
          <div className="bg-[#f7f9fb] rounded-2xl p-5">
            <p className="text-[#b0b0b0] text-[18px] leading-relaxed">
              ex)<br />
              2025년 8월 18일 까지 보증금을 돌려줬으면 좋겠습니다
            </p>
          </div>
        </div>
      </section>

      {/* 하단 고정 영역 */}
      <div className="w-full px-6 pb-8 pt-6 bg-white rounded-b-[40px] flex flex-col items-center">
        <p className="text-center text-[16px] mb-4 bg-gradient-to-r from-[#6000ff] to-[#e100ff] bg-clip-text text-transparent">
          Tip: 자세히 입력할 수록 완성도 있는 내용증명서가 작성됩니다
        </p>
        <button
          className="w-full max-w-[400px] h-[70px] rounded-full bg-[#b0b0b0] flex items-center justify-center text-white text-[26px] font-semibold gap-2 shadow"
        >
          <HiOutlineSparkles className="w-7 h-7 mr-2" />
          생성하기
        </button>
      </div>
    </div>
  );
}

