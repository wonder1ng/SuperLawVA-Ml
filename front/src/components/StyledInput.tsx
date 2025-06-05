// StyledInput.tsx
"use client";

import styled from "styled-components";

interface StyledInputProps {
  width?: number | string;
  height?: number | string;
  fontWeight?: number;
  fontSize?: number | string;
  type: string;
  className?: string;
  placeholder?: string;
  value?: string | number;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const InputContainer = styled.div<{
  width: number | string;
  fontWeight: number;
  fontSize: number | string;
}>`
  display: flex;
  flex-direction: column;
  justify-content: start;

  input {
    width: ${({ width }) => width};
    font-weight: ${({ fontWeight }) => fontWeight};
    font-size: ${({ fontSize }) => fontSize};
    padding: 0 1rem;
    line-height: 2rem;
    border: none;
    background: transparent;

    &::placeholder {
      color: #9ca3af;
      font-size: ${({ fontSize }) => fontSize};
    }
  }

  .line {
    width: ${({ width }) => width};
    border: 0.15rem solid rgba(187, 187, 187, 0.4);
    margin-top: 0.2rem;
  }
`;

export default function StyledInput({
  width = "32rem",
  fontWeight = 400,
  fontSize = "1.4rem",
  type = "text",
  className,
  placeholder,
  value,
  onChange,
}: StyledInputProps) {
  return (
    <InputContainer
      width={width}
      fontSize={fontSize}
      className={className}
      fontWeight={fontWeight}
    >
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
      <div className="line" />
    </InputContainer>
  );
}
