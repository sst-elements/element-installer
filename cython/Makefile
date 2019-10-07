CC = /usr/bin/clang-9

SRC = cli.pyx
OBJ = $(SRC:%.pyx=%.c)
EXE = bin/sst-elements
LDFLAGS = -lpython3.6m -lpthread -lm -lutil -ldl
CFLAGS = -I /usr/include/python3.6m

default: compile

.PHONY: translate
translate:
	cython -3 --embed -D -o ${OBJ} ${SRC}

.PHONY: compile
compile:
	${CC} -O3 ${CFLAGS} -o ${EXE} ${OBJ} ${LDFLAGS}

clean:
	rm -rf build/ __pycache__ ${EXE}
	rm -rf *.o *.so
