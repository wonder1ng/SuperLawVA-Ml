"use client";

import React, { useEffect } from "react";

interface Props {
  isOpen: boolean;
  setIsOpen: (value: boolean) => void;
  isCenter?: boolean;
  height?: number | string;
  children: React.ReactNode;
  clickOutsideClose?: boolean;
}

const Modal = ({
  isOpen,
  setIsOpen,
  isCenter = false,
  height,
  children,
  clickOutsideClose = true,
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
      className={`fixed top-0 left-0 w-screen h-screen z-50 flex justify-center ${
        isCenter ? "items-center px-8" : "items-end"
      }`}
    >
      {/* 🔵 배경에만 opacity 적용 */}
      <div
        className="absolute top-0 left-0 w-screen h-screen bg-black opacity-50"
        onClick={() => clickOutsideClose && setIsOpen(false)}
      />

      {/* ⚪ 모달 내용은 불투명하게 */}
      <div
        onClick={(e) => e.stopPropagation()}
        className={`
        relative z-50 bg-white transition-transform duration-300 ease-in-out transform animate-slide-up
        w-full max-w-[765px] ${isCenter ? "rounded-[50px]" : "rounded-t-[50px]"}
        max-h-[80%]
        shadow-[0_-2px_10px_rgba(0,0,0,0.2)]
        flex flex-col items-center
      `}
        // ${isCenter ? "min-h-0" : "min-h-[50%]"}
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
