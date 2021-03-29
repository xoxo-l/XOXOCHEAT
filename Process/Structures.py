from ctypes import *

#4 Floats = 16 Bytes
class Vector3(Structure):
    _pack_ = 1
    _fields_ = [	('x', c_float),
                 ('y', c_float),
                 ('z', c_float)]


#3 Floats, 6 Bytes = 3 * 4 + 6 * 4 = 36 Bytes
class BoneMatrix(Structure):
    _pack_ = 1
    _fields_ = [	('x', c_float),
                 ("padding0", c_byte * 0xC),
                 ('y', c_float),
                 ("padding1", c_byte * 0xC),
                 ('z', c_float)]


class GlowObject(Structure):
    _pack_ = 1
    _fields_ = [("pBaseEntity", c_int),
                ('r', c_float),
                ('g', c_float),
                ('b', c_float),
                ('a', c_float),
                ("_0x14", c_byte * 0x10),
                ("renderOccluded", c_bool),
                ("renderWhenUnoccluded", c_bool),
                ("fullBloom", c_bool),
                ("_0x27", c_byte * 0x5),
                ("style", c_int),
                ("splitScreenSlot", c_int),
                ("nextFreeSlot", c_int)]

class THREADENTRY32(Structure):
	_fields_ = [
	('dwSize' , c_long ),
	('cntUsage' , c_long),
	('th32ThreadID' , c_long),
	('th32OwnerProcessID' , c_long),
	('tpBasePri' , c_long),
	('tpDeltaPri' , c_long),
	('dwFlags' , c_long) ]

class MODULEENTRY32(Structure):
	_fields_ = [ ( 'dwSize' , c_long ) , 
	( 'th32ModuleID' , c_long ),
	( 'th32ProcessID' , c_long ),
	( 'GlblcntUsage' , c_long ),
	( 'ProccntUsage' , c_long ) ,
	( 'modBaseAddr' , c_long ) ,
	( 'modBaseSize' , c_long ) , 
	( 'hModule' , c_void_p ) ,
	( 'szModule' , c_char * 256 ),
	( 'szExePath' , c_char * 260 ) ]

Module32First = windll.kernel32.Module32First
Module32First.argtypes = [ c_void_p , POINTER(MODULEENTRY32) ]
Module32First.rettype = c_int

Module32Next = windll.kernel32.Module32Next
Module32Next.argtypes = [ c_void_p , POINTER(MODULEENTRY32) ]
Module32Next.rettype = c_int

Thread32First = windll.kernel32.Thread32First
Thread32First.argtypes = [ c_void_p , POINTER(THREADENTRY32) ]
Thread32First.rettype = c_int

Thread32Next = windll.kernel32.Thread32Next
Thread32Next.argtypes = [ c_void_p , POINTER(THREADENTRY32) ]
Thread32Next.rettype = c_int

SetLastError = windll.kernel32.SetLastError
SetLastError.rettype = c_void_p

GetLastError = windll.kernel32.GetLastError
GetLastError.rettype = c_long

ntdll = windll.ntdll
RPM = ntdll.NtReadVirtualMemory
WPM = ntdll.NtWriteVirtualMemory

if __name__ == "__main__":

    print(dir(Vector3(10.3, 3.3, 5.8)))

    if not (sizeof(Vector3) == 12):
        raise(Exception("WRONG SIZE: Process::Structures.py::Vector3"))
    if not (sizeof(BoneMatrix) == 36):
        raise(Exception("WRONG SIZE: Process::Structures.py::BoneMatrix"))
    if not (sizeof(GlowObject) == 56):
        raise(Exception("WRONG SIZE: Process::Structures.py::GlowObject"))
