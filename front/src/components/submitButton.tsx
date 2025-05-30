import styled from "styled-components";

interface StyledButtonProps {
  width?: number;
  height?: number;
  fontColor?: string;
  fontSize?: number;
  fontWeight?: number;
  gap?: number;
  background?: string;
  children?: React.ReactNode;
  disabled?: boolean;
  icon?: React.ReactNode;
  className?: string;
}

const StyledButton = styled.button.withConfig({
  shouldForwardProp: (prop) =>
    ![
      "width",
      "height",
      "fontColor",
      "fontSize",
      "fontWeight",
      "gap",
      "background",
    ].includes(prop),
})<StyledButtonProps>`
  width: ${({ width }) => width + "rem"};
  height: ${({ height }) => height + "rem"};
  background: ${({ disabled, background }) =>
    disabled
      ? "#9ca3af"
      : background || "linear-gradient(180deg, #5046E5 50%, #9134EB 143.75%)"};
  box-shadow: ${({ disabled }) =>
    disabled
      ? "none"
      : "0px 0.4rem 0.4rem rgba(0, 0, 0, 0.25), inset 0px 0.1rem 0.4rem rgba(0, 0, 0, 0.25)"};
  border-radius: 3rem;

  color: ${({ fontColor }) => fontColor};
  font-weight: ${({ fontWeight }) => fontWeight};
  font-size: ${({ fontSize }) => fontSize + "rem"};
  line-height: 2.6rem;

  display: flex;
  justify-content: center;
  align-items: center;

  cursor: ${({ disabled }) => (disabled ? "not-allowed" : "pointer")};
  pointer-events: ${({ disabled }) => (disabled ? "none" : "auto")};
  opacity: ${({ disabled }) => (disabled ? 0.6 : 1)};
  gap: ${({ gap }) => gap + "rem"};
`;

export default function SubmitButton({
  width = 20,
  height = 5.5,
  fontColor = "#ffffff",
  fontWeight = 700,
  fontSize = 2.2,
  gap = 0.8,
  background,
  disabled = false,
  children,
  icon,
  className,
}: StyledButtonProps) {
  return (
    <StyledButton
      width={width}
      height={height}
      background={background}
      fontColor={fontColor}
      fontSize={fontSize}
      fontWeight={fontWeight}
      disabled={disabled}
      gap={gap}
      className={className}
    >
      {icon && <span>{icon}</span>}
      {children}
    </StyledButton>
  );
}
