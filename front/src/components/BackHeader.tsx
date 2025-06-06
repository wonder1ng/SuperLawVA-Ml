import ArrowLeftIcon from "./icons/ArrowLeft";

interface BackLinkProps {
  children?: string;
}

export default function BackHeader({ children }: BackLinkProps) {
  return (
    <div className="h-24 grid items-end place-items-center relative">
      <ArrowLeftIcon
        width="3rem"
        height="3rem"
        className="col-start-1 row-start-1 relative -left-[16.8rem]"
      />
      {children && (
        <span className="col-start-1 row-start-1 leading-[2.9rem] font-semibold text-[2.4rem]">
          {children}
        </span>
      )}
    </div>
  );
}
