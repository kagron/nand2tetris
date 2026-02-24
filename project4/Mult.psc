// Multiplication
// Computes the product of RAM[0] and RAM[1] and stores the
// result in RAM[2]
n = RAM[0]
ans = 0
LOOP:
  if (n == 0) goto END
  ans = ans + RAM[0]
  n = n - 1
END:
