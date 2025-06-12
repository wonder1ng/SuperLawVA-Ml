import IconOptions from "@/app/types/IconOptions";

const PictureIcon = ({
  width = 2,
  height = 2,
  color = "#6000FF",
  className,
}: IconOptions) => (
  <svg
    width={typeof width == "number" ? width + "rem" : width}
    height={typeof height == "number" ? height + "rem" : height}
    color={color}
    viewBox="0 0 20 20"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M5.79688 6.1062C6.15565 5.56819 6.9124 5.5147 7.34668 5.9646L7.42969 6.06128L11.6162 11.6443C12.2408 12.477 13.4614 12.4961 14.1191 11.7341L14.2432 11.571C14.5907 11.0496 14.6022 10.3776 14.2822 9.84741L14.2139 9.74292L13.1904 8.3103C13.3578 8.28345 13.5363 8.32766 13.6729 8.45093L13.7266 8.50659L16.4629 11.698C17.5748 12.9953 16.6528 14.9995 14.9443 14.9998H3.60547C2.0581 14.9997 1.11528 13.3291 1.86328 12.0164L1.94141 11.8904L5.79688 6.1062Z"
      stroke={color}
      strokeWidth="2"
    />
    <circle
      cx="12.4001"
      cy="2.66667"
      r="1.66667"
      stroke={color}
      strokeWidth="2"
    />
  </svg>
);

export default PictureIcon;
