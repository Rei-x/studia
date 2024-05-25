import { useState, useEffect } from "react";
import Image, { type ImageProps } from "next/image";

export const ImageFallback = ({
  src,
  fallbackSrc,
  ...rest
}: ImageProps & { fallbackSrc: ImageProps["src"] }) => {
  const [imgSrc, set_imgSrc] = useState(src);

  useEffect(() => {
    set_imgSrc(src);
  }, [src]);

  return (
    <Image
      {...rest}
      alt={rest.alt}
      src={imgSrc}
      onLoadingComplete={(result) => {
        if (result.naturalWidth === 0) {
          set_imgSrc(fallbackSrc);
        }
      }}
      onError={() => {
        set_imgSrc(fallbackSrc);
      }}
    />
  );
};
