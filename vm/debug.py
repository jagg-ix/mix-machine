from vm import VM
from vm_word import Word, CmdWord
from vm_command import cmdList


vm = VM()

#		Addr	Index	Fmt	Code	# Offset	Asm
mem = [	Word([	1,0,18,	0,	19,	8]),	# 0		
	Word([	1,0,17,	0,	2,	0]),	# 1		
	Word([	1,0,18,	0,	5,	0]),	# 2		
	Word([	1,0,18,	0,	19,	0]),	# 3		
	Word([	1,0,0,	0,	0,	0]),	# 4		
	
	Word([	1,0,0,	0,	0,	0]),	# 5		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 6		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 7		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 8		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 9		NOP 
	
	Word([	1,0,0,	0,	0,	0]),	# 10		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 11		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 12		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 13		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 14		NOP 
	
	Word([	1,0,19,	0,	0,	39]),	# 15		JMP 19
	Word([	1,0,0,	0,	0,	0]),	# 16		NOP 
	Word([	1,10,20,30,	40,	50]),	# 17		NOP 
	Word([	-1,1,2,	3,	4,	5]),	# 18		NOP 
	Word([	1,0,0,	0,	2,	5]),	# 19		HLT
	]

vm.context.mem.set_range(mem, 0)
for i in vm.context.mem.get_range(0, 20):
	print str(i)

while not vm.context.is_halted:
	raw_input()
	
	print "--[trace]-----------------------------------------------"
	vm.trace()
	print str(vm.context)
	word = CmdWord(vm.context.mem.get(vm.context.regs["L"].int()))
	print str(word) + ":\t" + str(cmdList.get_command(word.code(), word.fmt()))
	print "--------------------------------------------------------"