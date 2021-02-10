all: \
    android_192.png \
    android_512.png \
    apple_114.png   \
    apple_152.png   \
    apple_180.png   \
    apple_76.png    \
    favicon_16.png  \
    favicon_32.png  \
    favicon_48.png

%.png: ../img/aleksis-icon.svg
	convert -strip -density 1200 -resize $(subst favicon_,,$(subst android_,,$(subst apple_,,$(@:.png=)))) "$<" "$@"

.PHONY: all
