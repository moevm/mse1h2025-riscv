ENTRY(_start)

MEMORY {
    FLASH (rx) : ORIGIN = 0x80000000, LENGTH = 128K
    RAM (rwx) : ORIGIN = 0x80020000, LENGTH = 64K
}

SECTIONS {
    .text : {
        *(.text .text.*)
    } > FLASH

    .rodata : {
        *(.rodata .rodata.*)
    } > FLASH

    .data : {
        _data_start = .;
        *(.data .data.*)
        _data_end = .;
    } > RAM AT> FLASH

    .bss : {
        _bss_start = .;
        *(.bss .bss.*)
        *(COMMON)
        _bss_end = .;
    } > RAM

    /DISCARD/ : {
        *(.comment)
    }
}