import IconOptions from "@/app/types/IconOptions";

const UploadIcon = ({
  width = 1.4,
  height = 1.6,
  color = "#6000FF",
  className,
}: IconOptions) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 14 16"
    width={typeof width == "number" ? width + "rem" : width}
    height={typeof height == "number" ? height + "rem" : height}
    color={color}
    fill={"none"}
  >
    <path
      d="M1 9.5V15H13V9.5M3.5 7L7 10M7 10L10.5 7M7 10V1"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
    />
  </svg>
);

export default UploadIcon;
