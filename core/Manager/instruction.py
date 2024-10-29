class Instruction:
    def __init__(self, query, instruction='I have the following information. '):
        self.instructionQueue = []
        self.query = query
        self.instruction = instruction
    def pushInstruction(self, instruction):
        self.instructionQueue.append(instruction)

    def getInstruction(self):
        instruction = self.instruction
        for el in self.instructionQueue:
            instruction+=f'\n{el}\n'
        
        return instruction+self.query

# i = Instruction('What is the sum of the numbers?')
# i.pushInstruction('The first number is 10')
# i.pushInstruction('The second number is 20')
# i.pushInstruction('The third number is 30')
# print(i.getInstruction())