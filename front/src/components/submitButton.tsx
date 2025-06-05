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
  subStyle?: boolean;
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
      "subStyle",
    ].includes(prop),
})<StyledButtonProps>`
  width: ${({ width }) => width + "rem"};
  height: ${({ height }) => height + "rem"};

  background: ${({ disabled, subStyle, background }) =>
    disabled
      ? "rgba(128, 128, 128, 0.55)"
      : subStyle
      ? "#F7F9FB"
      : background || "#5046E5"};

  border: ${({ disabled, subStyle }) =>
    disabled || !subStyle ? "none" : "0.14rem solid #5046E5"};

  /* box-shadow: ${({ disabled }) =>
    disabled
      ? "none"
      : "0px 0.4rem 0.4rem rgba(0, 0, 0, 0.25), inset 0px 0.1rem 0.4rem rgba(0, 0, 0, 0.25)"}; */

  border-radius: 50px;

  color: ${({ disabled, subStyle, fontColor }) =>
    disabled ? "#ffffff" : subStyle ? "#5046E5" : fontColor || "#ffffff"};

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
  subStyle = false,
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
      subStyle={subStyle}
    >
      {icon && <span>{icon}</span>}
      {children}
    </StyledButton>
  );
}
