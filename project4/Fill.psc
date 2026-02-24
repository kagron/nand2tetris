// Fill
// Listens to Keyboard and writes black in every pixel
// if key is pressed

n = 0
LOOP:
  // Check KBD
  D = @KBD
  if (D != 0) FILL
  else jmp LOOP

FILL:
  for(n in [0..31])
    @SCREEN+n*16
    M = -1
