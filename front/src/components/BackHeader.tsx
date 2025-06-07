import IconOptions, { LinkIconProps } from "@/app/types/IconOptions";
import ArrowLeftIcon from "./icons/ArrowLeft";

interface BackLinkProps extends LinkIconProps {
  children?: string;
}

export default function BackHeader({
  width = 3,
  height = 3,
  color = "#000000",
  to,
  children,
}: BackLinkProps) {
  return (
    <header className="grid items-end place-items-center relative">
      <ArrowLeftIcon
        width={width}
        height={height}
        color={color}
        to={to}
        className="col-start-1 row-start-1 relative -left-[16.8rem]"
      />
      {children && (
        <span className="col-start-1 row-start-1 leading-[2.9rem] font-semibold text-[2.4rem]">
          {children}
        </span>
      )}
    </header>
  );
}
