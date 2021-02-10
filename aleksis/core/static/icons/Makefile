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

android_%.png: ../img/aleksis-icon.svg
	convert -strip -density 1200 -resize $(subst android_,,$(@:.png=)) "$<" "$@"

apple_%.png: ../img/aleksis-icon.svg
	convert -strip -density 1200 -resize $(subst apple_,,$(@:.png=)) "$<" "$@"

favicon_%.png: ../img/aleksis-icon.svg
	convert -strip -density 1200 -resize $(subst favicon_,,$(@:.png=)) "$<" "$@"

.PHONY: all
