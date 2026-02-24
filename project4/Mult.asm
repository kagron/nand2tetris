// Multiplication
// Computes the product of RAM[0] and RAM[1] and stores the
// result in RAM[2]
@R0
D=M
@n
M=D
@R2
M=0
(LOOP)
  // if (n == 0) goto END
  @n
  D=M
  @END
  D;JEQ
  // ans = ans + RAM[1]
  @R2
  D=M
  @R1
  D=D+M
  @R2
  M=D
  // n = n - 1
  @n
  M=M-1
  // GOTO LOOP
  @LOOP
  0;JMP
(END)
  @END
  0;JMP
