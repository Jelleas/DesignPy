import sys
import printer
import advice as a

def main():
	if len(sys.argv) != 2:
		printer.displayError("Wrong number of arguments provided to check, usage: check <pyfile>")
		return
		
	fileName = sys.argv[1] if sys.argv[1].endswith(".py") else sys.argv[1] + ".py"
	printer.display(a.Advice(a.AdviceLevel.GOOD, "hello world!"))
	printer.display(a.Advice(a.AdviceLevel.MIXED, "hello world!"))
	printer.display(a.Advice(a.AdviceLevel.BAD, "hello world!"))

main()