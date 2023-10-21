.PHONY = all
SOURCES = victim.c
TARGET = victim
CFLAGS = -Wl,-z,norelro -no-pie
NO_CANARY_TARGET = victim_no_canary
NO_NX_NO_CANARY_TARGET = victim_no_canary_no_nx

all: compile ownership setuid

compile: $(TARGET) $(NO_CANARY_TARGET) $(NO_NX_NO_CANARY_TARGET)

$(TARGET): $(SOURCES)
	gcc -std=c99 -Wno-deprecated-declarations $(CFLAGS) -o $(TARGET) $^

$(NO_CANARY_TARGET): $(SOURCES)
	gcc -std=c99 -Wno-deprecated-declarations -fno-stack-protector $(CFLAGS) -o $(NO_CANARY_TARGET) $^

$(NO_NX_NO_CANARY_TARGET): $(SOURCES)
	gcc -std=c99 -Wno-deprecated-declarations -fno-stack-protector -z execstack $(CFLAGS) -o $(NO_NX_NO_CANARY_TARGET) $^

ownership: $(TARGET) $(NO_CANARY_TARGET) $(NO_NX_NO_CANARY_TARGET)
	@for file in $^; do \
		sudo chown root.root $$file; \
	done

setuid: $(TARGET) $(NO_CANARY_TARGET) $(NO_NX_NO_CANARY_TARGET)
	@for file in $^; do \
		sudo chmod u+s $$file; \
	done

clean:
	rm -f $(TARGET)
