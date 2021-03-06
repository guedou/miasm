#! /usr/bin/env python2
import sys

from asm_test import Asm_Test_32

class Test_SCAS(Asm_Test_32):
    MYSTRING = "test string"
    TXT = '''
    main:
       LEA EDI, DWORD PTR [mystr]
       XOR  ECX, ECX
       DEC  ECX
       REPNE SCASB
       NOT ECX
       DEC ECX
       RET

    mystr:
    .string "%s"
    ''' % MYSTRING

    def check(self):
        assert(self.myjit.cpu.ECX == len(self.MYSTRING))
        mystr = self.myjit.ir_arch.symbol_pool.getby_name('mystr')
        assert(self.myjit.cpu.EDI == self.myjit.ir_arch.symbol_pool.loc_key_to_offset(mystr) + len(self.MYSTRING)+1)


class Test_MOVS(Asm_Test_32):
    MYSTRING = "test string"
    TXT = '''
    main:
       LEA ESI, DWORD PTR [mystr]
       LEA EDI, DWORD PTR [buffer]
       MOV ECX, %d
       REPE  MOVSB
       RET

    mystr:
    .string "%s"
    buffer:
    .string "%s"
    ''' % (len(MYSTRING), MYSTRING, " "*len(MYSTRING))

    def check(self):
        assert(self.myjit.cpu.ECX == 0)
        buffer = self.myjit.ir_arch.symbol_pool.getby_name('buffer')
        assert(self.myjit.cpu.EDI == self.myjit.ir_arch.symbol_pool.loc_key_to_offset(buffer) + len(self.MYSTRING))
        mystr = self.myjit.ir_arch.symbol_pool.getby_name('mystr')
        assert(self.myjit.cpu.ESI == self.myjit.ir_arch.symbol_pool.loc_key_to_offset(mystr) + len(self.MYSTRING))


if __name__ == "__main__":
    [test(*sys.argv[1:])() for test in [Test_SCAS, Test_MOVS]]
