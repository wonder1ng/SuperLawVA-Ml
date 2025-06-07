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

const NavBtn: React.FC<NavBtnProps> = ({ to, icon: Icon, label }) => {
  const pathname = usePathname();
  const isActive = pathname === to;
  const color = isActive ? "#5046E5" : "#717171";

  return (
    <Link href={to} className="flex flex-col items-center gap-1">
      <Icon width={24} height={24} color={color} />
      <span className={`text-[1.2rem]`} style={{ color }}>
        {label}
      </span>
    </Link>
  );
};

const BottomNav = () => {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) return null;

  return (
    <nav className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-md h-20 border-t border-[#F7F9FB] bg-white pt-4 px-2 z-10">
      <div className="flex justify-around items-center h-full">
        <NavBtn to="/main" icon={HomeIcon} label="홈" />
        <NavBtn to="/register" icon={ChatIcon} label="채팅" />
        <NavBtn to="/start" icon={UserIcon} label="내 정보" />
      </div>
    </nav>
  );
};

export default BottomNav;
