from fst import *

# here are some predefined character sets that might come in handy.
# you can define your own
AZ = set("abcdefghijklmnopqrstuvwxyz")
VOWS = set("aeiou")
CONS = AZ-VOWS
E = set("e")
UCONS = CONS.copy()
UCONS.add("u")
I = set("i")
N = set("n")
T = set("t")
R = set("r")
P = set("p")


# Implement your solution here
def buildFST():
    print("Your task is to implement a better FST in the buildFST() function, using the methods described here")
    print("You may define additional methods in this module (hw1_fst.py) as desired")
    #
    # The states (you need to add more)
    # ---------------------------------------
    # 
    f = FST("q0") # q0 is the initial (non-accepting) state
    f.addState("q_ing") # a non-accepting state
    f.addState("q_EOW", True) # an accepting state (you shouldn't need any additional accepting states)
    f.addState("q_u/con")
    f.addState("q_not_u/con")
    f.addState("q_rm_e")
    f.addState("q_interm_e")
    f.addState("q_e")
    f.addState("q_i")
    f.addState("q_ie")
    f.addState("q_vow")
    f.addState("q_n")
    f.addState("q_p")
    f.addState("q_t")
    f.addState("q_r")

    #
    # The transitions (you need to add more):
    # ---------------------------------------
    # transduce every element in this set to itself: 
    f.addSetTransition("q0", AZ, "q0")

    f.addSetTransition("q0", UCONS, "q_u/con")
    # f.addSetTransition("q_u/con", E, "q_rm_e")
    f.addTransition("q_u/con", "e", "", "q_ing")
    f.addSetTransition("q_u/con", AZ - E, "q_ing")

    f.addSetTransition("q0", AZ - UCONS - I, "q_interm_e")
    f.addSetTransition("q_interm_e", E, "q_ing")

    # f.addSetTransition("q0", I, "q_i")
    # f.addSetTransition("q_i", E, "q_ie")
    f.addTransition("q0", "i", "", "q_i")
    f.addTransition("q_i", "e", "y", "q_ing")

    f.addSetTransition("q0", VOWS, "q_vow")
    # f.addSetTransition("q_vow1", VOWS, "q_vow2")
    f.addSetTransition("q_vow", N, "q_n")
    f.addSetTransition("q_vow", T, "q_t")
    f.addSetTransition("q_vow", P, "q_p")
    f.addSetTransition("q_vow", R, "q_r")
    f.addSetTransition("q_vow", AZ - N - T - R - P, "q_ing")
    f.addTransition("q_r", "", "r", "q_ing")
    f.addTransition("q_t", "", "t", "q_ing")
    f.addTransition("q_p", "", "p", "q_ing")
    f.addTransition("q_n", "", "n", "q_ing")

    # map the empty string to ing: 
    f.addTransition("q_ing", "", "ing", "q_EOW")

    # Return your completed FST
    return f
    

if __name__ == "__main__":
    # Pass in the input file as an argument
    if len(sys.argv) < 2:
        print("This script must be given the name of a file containing verbs as an argument")
        quit()
    else:
        file = sys.argv[1]
    #endif

    # Construct an FST for translating verb forms 
    # (Currently constructs a rudimentary, buggy FST; your task is to implement a better one.
    f = buildFST()
    # Print out the FST translations of the input file
    f.parseInputFile(file)
