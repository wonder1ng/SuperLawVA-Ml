import React, { useMemo, useState, useEffect } from "react";
import Link from "next/link"; // Link 컴포넌트
import { usePathname } from "next/navigation"; // usePathname 훅
import HomeIcon from "./icons/Home";
import ChatIcon from "./icons/Chat";
import UserIcon from "./icons/User";

interface NavBtnProps {
  to: string;
  icon: React.ElementType;
  label: string;
}

const NavBtn: React.FC<NavBtnProps> = ({ to, icon: Icon, label }) => {
  const pathname = usePathname(); // 현재 경로 가져오기
  const color = pathname === to ? "#0B798B" : "#717171"; // 경로와 비교하여 색상 설정

  return (
    <Link href={to} className="flex flex-col items-center gap-1">
      <Icon width={24} height={24} color={color} />
      <span className="text-[1.2rem]" style={{ color }}>
        {label}
      </span>
    </Link>
  );
};

const BottomNav = () => {
  const [isClient, setIsClient] = useState(false);

  // 클라이언트에서만 렌더링되도록 설정
  useEffect(() => {
    setIsClient(true);
  }, []);

  // 클라이언트에서만 usePathname 사용하도록 하기 위해 typeof window 체크
  useEffect(() => {
    const width = window.innerWidth;
  }, []);

  const pathname = usePathname(); // 현재 경로 정보 가져오기
  const startPathname = pathname.split("/").splice(1); // 경로를 '/'로 분리하여 배열로 변환

  const mainColor = "#0B798B";
  const darkGrayColor = "#717171";

  // const colors = useMemo(
  //   () => ({
  //     home: startPathname.includes("") ? mainColor : darkGrayColor,
  //     chat: startPathname.includes("chat") ? mainColor : darkGrayColor,
  //     mypage: startPathname.includes("mypage") ? mainColor : darkGrayColor,
  //   }),
  //   [startPathname]
  // );

  return (
    <nav className="absolute bottom-0 left-1/2 -translate-x-1/2 w-full h-20 border-t-1 border-main-bg bg-white pt-[1rem] px-[0.5rem] z-10">
      <div className="flex gap-1 justify-around items-center">
        <NavBtn to="/" icon={HomeIcon} label="홈" />
        <NavBtn to="/chat" icon={ChatIcon} label="채팅" />
        <NavBtn to="/mypage" icon={UserIcon} label="내 정보" />
      </div>
    </nav>
  );
};

export default BottomNav;
