SRC = src
BUILDDIR = build
all: clean createCatalogue compile copy

compile: $(SRC)/*.py
	for file in $^ ; do \
		mpy-cross $${file} ; \
	done

copy:
	cp -r keep/* ${BUILDDIR}
	mv ${SRC}/*.mpy ${BUILDDIR}

createCatalogue:
	mkdir ${BUILDDIR}

clean:
	rm -rf build

deploy: all
	mpy-sync ${BUILDDIR}/* --delay 0 --debug