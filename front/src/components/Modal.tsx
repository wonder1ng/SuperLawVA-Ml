import React, { useEffect } from "react";
import ReactDOM from "react-dom";

interface Props {
  isOpen: boolean;
  setIsOpen: (value: boolean) => void;
  isCenter?: boolean;
  height?: number | string;
  children: React.ReactNode;
  upperChildren?: React.ReactNode;
  clickOutsideClose?: boolean;
}

const Modal = ({
  isOpen,
  setIsOpen,
  isCenter = false,
  height,
  children,
  upperChildren,
  clickOutsideClose = true,
}: Props) => {
  useEffect(() => {
    document.body.style.overflow = isOpen ? "hidden" : "auto";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div
      className={`fixed inset-0 z-30 flex flex-wrap justify-center ${
        isCenter ? "items-center px-8" : "items-end"
      }`}
    >
      <div
        className="absolute inset-0 bg-black opacity-50"
        onClick={() => clickOutsideClose && setIsOpen(false)}
      />

      {upperChildren && (
        <div
          className="z-40 pointer-events-auto"
          onClick={(e) => e.stopPropagation()}
        >
          {upperChildren}
        </div>
      )}
      <div
        onClick={(e) => e.stopPropagation()}
        className={`
          relative z-30 bg-white transition-transform duration-300 ease-in-out transform animate-slide-up
          w-full ${isCenter ? "rounded-[50px]" : "rounded-t-[50px]"}
          max-h-[80%] shadow-[0_-2px_10px_rgba(0,0,0,0.2)]
          flex flex-col items-center`}
      >
        {!isCenter && (
          <div className="w-6 h-0.5 rounded-full bg-main-gray mb-2" />
        )}
        {children}
      </div>
    </div>,
    document.body
  );
};

export default Modal;
