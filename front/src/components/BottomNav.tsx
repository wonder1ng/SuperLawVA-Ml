'use client';

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function BottomNav() {
  const pathname = usePathname();

  return (
    <div className="fixed bottom-0 left-0 right-0 h-[52px] flex justify-center items-center">
      <div className="relative w-[393px] h-[52px]">
        <div className="absolute top-0 left-0 w-full h-full backdrop-blur-[4px] rounded-[41px] bg-white/20" />
        <div className="absolute top-[6px] left-[46px] w-[301px] h-[40px] flex justify-between items-center">
          {/* 홈 */}
          <Link href="/main" className="relative w-[16px] h-[40px]">
            <Image
              src="/home.svg"
              alt="Home"
              width={16}
              height={18}
              className="absolute top-0 left-0"
            />
            <div className={`absolute top-[30px] left-[4px] text-[10px] font-semibold leading-[10px] ${pathname === '/' ? 'bg-gradient-to-r from-[#6000ff]/70 to-[#e100ff]/70 bg-clip-text text-transparent' : 'text-[#9ca3af]'}`}>
              홈
            </div>
          </Link>

          {/* 채팅 */}
          <Link href="/chat" className="relative w-[19px] h-[40px]">
            <Image
              src="/chat.svg"
              alt="Chat"
              width={19}
              height={18}
              className="absolute top-0 left-[calc(50%-9.5px)]"
            />
            <div className={`absolute top-[30px] left-0 text-[10px] font-semibold leading-[10px] ${pathname === '/chat' ? 'bg-gradient-to-r from-[#6000ff]/70 to-[#e100ff]/70 bg-clip-text text-transparent' : 'text-[#9ca3af]'}`}>
              채팅
            </div>
          </Link>

          {/* 더보기 */}
          <Link href="/more" className="relative w-[26px] h-[40px]">
            <Image
              src="/more.svg"
              alt="More"
              width={16}
              height={2}
              className="absolute top-0 left-[19.23%]"
            />
            <div className={`absolute top-[30px] left-0 text-[10px] font-semibold leading-[10px] whitespace-nowrap ${pathname === '/more' ? 'bg-gradient-to-r from-[#6000ff]/70 to-[#e100ff]/70 bg-clip-text text-transparent' : 'text-[#9ca3af]'}`}>
              더보기
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
