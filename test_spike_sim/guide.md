Использование симулятора Spike Risc-v ISA Simulator

# Установка
Установка делится на 2 этапа, сначала RISC-V gcc toolchain, потом SPIKE - the RISC-V ISA Simulator.

## RISC-V gcc toolchain
Update System and install pre-requisites

<pre>sudo apt update
sudo apt install autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev</pre>

Clone Toolchain Repository

<pre>mkdir RISCV
cd RISCV
git clone --recursive https://github.com/riscv/riscv-gnu-toolchain
cd riscv-gnu-toolchain</pre>

Configure and Build for rv64gcv

<pre>mkdir build
cd build 
../configure --prefix=/opt/riscv --with-arch=rv64gcv --with-abi=lp64d
sudo make -j$(nproc)</pre>

Add the RISC-V toolchain to the PATH

<pre>export PATH=/opt/riscv/bin:$PATH</pre>

Cross-Compile Your Code

<pre>riscv64-unknown-elf-gcc -o example example.c</pre>
Для .s файлов:
<pre>
riscv64-unknown-elf-as -o example.o example.s
riscv64-unknown-elf-ld -o example.elf example.o
</pre>


## SPIKE - the RISC-V ISA Simulator
Spike setup

First install the pre-requisites.

<pre>sudo apt-get update  
sudo apt-get install device-tree-compiler  
sudo apt-get install libboost-all-dev</pre>

Clone the SPIKE Repository

This should be set up in the RISCV directory you created when setting up the RISC-V GCC Toolchain.

<pre>cd RISCV
git clone https://github.com/riscv-software-src/riscv-isa-sim.git  
git clone https://github.com/riscv/riscv-pk.git</pre>  

Configure and Build SPIKE

If you are using an ARM CPU computer, change x86_64-linux-gnu to aarch64-linux-gnu in the --with-boost-libdir= option.

<pre>cd riscv-isa-sim   
mkdir build   
cd build  
sudo ../configure --prefix=$RISCV --host=riscv64-unknown-elf --with-boost-libdir=/usr/lib/x86_64-linux-gnu/
make -j$(nproc)
sudo make install</pre>

Configure and Build RISCV-PK

RISCV-PK is the Proxy Kernal used by the SPIKE ISA Simulator.

<pre>cd ../../riscv-pk
mkdir build
cd build
../configure --prefix=$RISCV --host=riscv64-unknown-elf 
make -j$(nproc)
sudo make install</pre>

Измените на свой путь
<pre>export PATH=/home/user/RISCV/riscv-pk/build:$PATH</pre>

Test the Install

Go to a directory where you have compiled a RISC-V executable using the RISC-V GCC Toolchain and run it using the command line below. In this example we have assumed that your executable is called main.

<pre>spike pk main</pre>


Для отладки использовался флаг -d для spike без pk. Предварительно необходимо узнать адрес входной функции.
<pre>riscv64-unknown-elf-objdump -D main.elf
spike -m0x100e8:0xFFF -d main.elf</pre>

Внутри "(spike) until pc 0 100e8" и можно пошагово выполнять.

Почти всё работает, кроме прерываний, с ними никак не получилось.
