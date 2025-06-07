"use client";

import React, { useEffect } from "react";

interface Props {
  isOpen: boolean;
  setIsOpen: (value: boolean) => void;
  children: React.ReactNode;
  isCenter?: boolean;
  clickOutsideClose?: boolean;
}

const Modal = ({
  isOpen,
  setIsOpen,
  isCenter = false,
  clickOutsideClose = true,
  children,
}: Props) => {
  useEffect(() => {
    document.body.style.overflow = isOpen ? "hidden" : "auto";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      onClick={() => clickOutsideClose && setIsOpen(false)}
      className={`fixed top-0 left-0 w-screen h-screen bg-black opacity-50 z-50 flex ${
        isCenter ? "items-center justify-center px-8" : "items-end"
      }`}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className={`
          bg-white transition-transform duration-300 ease-in-out transform animate-slide-up
          w-full ${isCenter ? "max-w-[45rem] rounded-xl" : "rounded-t-xl"}
          max-h-[80%] ${
            isCenter ? "min-h-0" : "min-h-[50%]"
          } p-8 shadow-[0_-2px_10px_rgba(0,0,0,0.2)]
          flex flex-col items-center gap-2
        `}
      >
        {!isCenter && (
          <div className="w-6 h-0.5 rounded-full bg-main-gray mb-2" />
        )}
        {children}
      </div>
    </div>
  );
};

export default Modal;
