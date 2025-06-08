import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import HomeIcon from "./icons/Home";
import ChatIcon from "./icons/Chat";
import UserIcon from "./icons/User";

interface NavBtnProps {
  to: string;
  icon: React.ElementType;
  label: string;
}

interface BottomNavProps {
  mainBackGroundColor?: string;
}

const NavBtn: React.FC<NavBtnProps> = ({ to, icon: Icon, label }) => {
  const pathname = usePathname();
  const isActive = pathname === to;
  const color = isActive ? "#5046E5" : "#717171";

  return (
    <Link href={to} className="flex flex-col items-center gap-1">
      <Icon width={2.4} height={2.4} color={color} />
      <span className={`text-[1.2rem]`} style={{ color }}>
        {label}
      </span>
    </Link>
  );
};

const BottomNav: React.FC<BottomNavProps> = ({ mainBackGroundColor }) => {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);
  if (!isClient) return null;

  return (
    <nav
      className="sticky -bottom-0 w-full h-28"
      style={{
        backgroundColor: mainBackGroundColor || "white", // ✅ 안전하게 처리
      }}
    >
      <div className="h-full border-t border-[#c6c6c8] bg-white pt-4 z-10 rounded-t-[50px]">
        <div className="flex justify-around items-center h-full">
          <NavBtn to="/main" icon={HomeIcon} label="홈" />
          <NavBtn to="/register" icon={ChatIcon} label="채팅" />
          <NavBtn to="/start" icon={UserIcon} label="내 정보" />
        </div>
      </div>
    </nav>
  );
};

export default BottomNav;
