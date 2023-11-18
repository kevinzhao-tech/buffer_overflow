.PHONY: all compile ownership setuid clean

SOURCES = victim.c
SROP_SOURCE = srop.c
TARGET = victim
CFLAGS = -std=c99 -Wno-deprecated-declarations
NO_CANARY_TARGET = victim_no_canary
NO_NX_NO_CANARY_TARGET = victim_no_canary_no_nx
SROP_NO_NX_NO_CANARY_TARGET = srop_no_canary_no_nx
SROP_NO_CANARY_TARGET = srop_no_canary
SROP_TARGET = srop

all: compile ownership setuid

compile: $(TARGET) $(NO_CANARY_TARGET) $(NO_NX_NO_CANARY_TARGET) $(SROP_NO_NX_NO_CANARY_TARGET) $(SROP_NO_CANARY_TARGET) $(SROP_TARGET)

$(TARGET): $(SOURCES)
	gcc $(CFLAGS) -o $(TARGET) $^

$(NO_CANARY_TARGET): $(SOURCES)
	gcc $(CFLAGS) -fno-stack-protector -o $(NO_CANARY_TARGET) $^

$(NO_NX_NO_CANARY_TARGET): $(SOURCES)
	gcc $(CFLAGS) -fno-stack-protector -z execstack -o $(NO_NX_NO_CANARY_TARGET) $^

$(SROP_NO_NX_NO_CANARY_TARGET): $(SROP_SOURCE)
	gcc $(CFLAGS) -no-pie -fno-stack-protector -z execstack -o $(SROP_NO_NX_NO_CANARY_TARGET) $^

$(SROP_NO_CANARY_TARGET): $(SROP_SOURCE)
	gcc $(CFLAGS) -no-pie -fno-stack-protector -o $(SROP_NO_CANARY_TARGET) $^

$(SROP_TARGET): $(SROP_SOURCE)
	gcc $(CFLAGS) -no-pie -o $(SROP_TARGET) $^

ownership: compile
	@for file in $(TARGET) $(NO_CANARY_TARGET) $(NO_NX_NO_CANARY_TARGET) $(SROP_NO_NX_NO_CANARY_TARGET)  $(SROP_NO_CANARY_TARGET) $(SROP_TARGET); do \
		sudo chown root:root $$file; \
	done

setuid: ownership
	@for file in $(TARGET) $(NO_CANARY_TARGET) $(NO_NX_NO_CANARY_TARGET) $(SROP_NO_NX_NO_CANARY_TARGET)  $(SROP_NO_CANARY_TARGET) $(SROP_TARGET); do \
		sudo chmod u+s $$file; \
	done

clean:
	rm -f $(TARGET) $(NO_CANARY_TARGET) $(NO_NX_NO_CANARY_TARGET) $(SROP_NO_NX_NO_CANARY_TARGET)  $(SROP_NO_CANARY_TARGET) $(SROP_TARGET)